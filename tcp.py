import socket
# by default: socket.AF_INET for IPv4, socket.SOCK_STREAM for TCP
s = socket.socket()
# s.bind(('', 50154))  # bind to all interfaces on port 50154
# put the socket into listening mode, backlog argument specifies max number of queued connections
s.listen(10)
# get the socket name (address, port) tuple
# the port is assigned by the OS if not specified in socket()
print(s.getsockname())
# ('0.0.0.0', 50025)
