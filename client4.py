import socket
import numpy
import scapy
import select as sel
import sys
import struct
import os
import Medussa as M

#make to understand right format struct.pack's BB..... liike that is very imporrtant 
SOCKET_LIST = [sys.stdin]
RECEIVE_BUFF = 4096

def chksum(msg):
        s = 0       # Binary Sum

        # loop taking 2 characters at a time
        for i in range(0, len(msg), 2):
            if (i+1) < len(msg):
                a = ord(msg[i]) 
                b = ord(msg[i+1])
                s = s + (a+(b << 8))
            elif (i+1)==len(msg):
                s += ord(msg[i])
            else:
                raise "Something Wrong here"


        # One's Complement
        s = s + (s >> 16)
        s = ~s & 0xffff

        return s  
def IPPacket(src,dst):
    global ipheader
    ipheader=[]+[]
    
    ip_vhl=5
    ip_ver1=4
    ip_ver=ip_ver1 + ip_vhl
    ip_dfc=0
    ip_tol=socket.htons(len(ipheader))
    ip_idf=socket.htons(9999)
    ip_frag_offset=0
    ip_ttl=64
    ip_proto=socket.IPPROTO_TCP	#[*ip_daddr,*ip_chk]]
    ip_chk=0
    ip_saddr=socket.inet_aton(src)     #"192.168.43.98"
    ip_daddr=socket.inet_aton(dst)    #"192.168.43.160"
    #ipheader=struct.pack('!BBHHHBBH4s4s',ip_ver, ip_vhl,ip_dfc,ip_tol, ip_idf,ip_frag_offset ,ip_ttl,ip_proto, ip_chk,  ip_saddr,ip_daddr)
    ip_chk=chksum(ipheader)
    #ip_chk=bytes(str(ip_chk,'utf-8'))
    ##ip_chk=ip_chk.to_bytes(1,'big')
	
    ipheader=struct.pack('!BBHHHBBH4s4s',ip_ver,ip_dfc,ip_tol,ip_idf,ip_frag_offset,ip_ttl,ip_proto,ip_chk,ip_saddr,ip_daddr)     #right format mind this 
    #ipheader=struct.pack('!BBHHHBBH4s4s',ip_daddr,ip_chk)   
    return ipheader

def chat_client():
	if len(sys.argv) < 4:
		print("Usage: python3 {} hostname port".format(sys.argv[0]))
		
	host = sys.argv[1]
	port = int(sys.argv[2])
	srcc=sys.argv[3]
	#sourceip=sys.argv[3]
	#srci=socket.inet_aton('192.168.43.98')
	#dsti=socket.inet_aton('192.168.43.160')
	
	
	
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW,socket.IPPROTO_RAW)
	s.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
	packets=IPPacket(srcc,host)+M.tcp_packet(port)
	
	s.sendto(packets,(host,port))
           
	#	sys.exit(-1)
	
		
	s.settimeout(5)
	
	
	#Amma varanga
	try:
		s.connect((host, port))
		#try:
			#s.send(ipheader)
			#print("[+] packet sent successfully")
		#except:
			#print("[-]error in packet ")
			#sys.exit(-1)
	except:
		print("Cannot reach the {}:{}...".format(host, port))
		sys.exit(-2)
		
	print("Connected to remote host. You can start sending messages...")
	sys.stdout.write("> ")
	sys.stdout.flush()
	
	while True:
		read_ready, write_ready, error = sel.select(SOCKET_LIST, [], [])
		#Block until connection is made
		for sock in read_ready:
			if sock == s:
				data = data.recv(RECEIVE_BUFF)
				if not data:
					print("Chat disconnected.")
					sys.exit()
				else:
					sys.stdout.write(data)
					sys.stdout.write("> ")
					sys.stdout.flush()
			else:
				msg = sys.stdin.readline()
				s.send(msg.encode())
				sys.stdout.write("> ")
				sys.stdout.flush()
		
if __name__ == "__main__":
	sys.exit(chat_client())
	
