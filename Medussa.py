import os
import struct
import socket
import sys





					#SHRIRAM'S MODULE FOR PROTOCOL IMPLEMENTION
					#MODULE FOR ALL PROTOCOLS
					#NOW TWO PROTOCOLS ARE IMPLEMENTED           DATE:11/10/2020
					#YOU CAN UPGRADE IT !!!!!


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

def tcp_packet(dstpo):
	tcp_header=()
	tcp_source=5895
	tcp_dst=dstpo
	tcp_seq=454
	tcp_ack_seq=0
	tcp_doff=5     #4 bits allowed for tcp_heaer 4*5 =20 bytes
	tcp_fin=0
	tcp_syn=1
	tcp_rst=0
	tcp_psh=0
	tcp_ack=0
	tcp_urg=0
	tcp_window=socket.htons(5840)
	tcp_check=0
	tcp_urgptr=0
	tcp_offset_res=(tcp_doff <<4) +0
	tcp_flag=tcp_fin + (tcp_syn <<1) +(tcp_rst <<2) +(tcp_psh <<3) +(tcp_ack << 4) +(tcp_urg <<5)
	tcp_check=chksum(tcp_header)	
	
	tcp_header=struct.pack('!HHLLBBHHH',tcp_source,tcp_dst,tcp_seq,tcp_ack_seq,tcp_offset_res,tcp_flag,tcp_window,tcp_check,tcp_urgptr)


	return tcp_header

