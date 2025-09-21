# This script requires root privileges to create raw sockets
# Run with: sudo python3 traceroute.py

import socket
import struct
import time

def traceroute(host, max_hops=30, timeout=2):
    dest_addr = socket.gethostbyname(host)
    port = 33434  # UDP port used by traceroute
    print(f"Tracing route to {host} [{dest_addr}]")

    for ttl in range(1, max_hops + 1):
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        
        send_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        recv_sock.settimeout(timeout)
        recv_sock.bind(("", port))
        
        start_time = time.time()
        send_sock.sendto(b"", (dest_addr, port))
        
        curr_addr = None
        try:
            data, addr = recv_sock.recvfrom(512)
            curr_addr = addr[0]
            rtt = (time.time() - start_time) * 1000
            print(f"{ttl}\t{curr_addr}\t{round(rtt, 2)} ms")
        except socket.timeout:
            print(f"{ttl}\t*")
        finally:
            recv_sock.close()
            send_sock.close()
        
        if curr_addr == dest_addr:
            break

# Example usage
traceroute("google.com")
