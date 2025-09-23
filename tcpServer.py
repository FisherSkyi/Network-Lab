import socket
# by default: socket.AF_INET for IPv4, socket.SOCK_STREAM for TCP
s = socket.socket()
# uncomment the line below to bind to all interfaces on port 50154
s.bind(('', 50154))

# put the socket into listening mode, backlog argument specifies max number of queued connections
# as long as you're accepting connections as soon as they come in, the length of your listen backlog is irrelevant. You can have as many active connections as you need; the listen backlog only affects connections which haven't been fully established.
# https://stackoverflow.com/questions/10002868/what-value-of-backlog-should-i-use
s.listen(10)
# get the socket name (address, port) tuple
# the port is assigned by the OS if not specified in socket()
print(f"Server listening on {s.getsockname()}")

# Accept incoming connections
print("Waiting for connections...")
conn, addr = s.accept()
print(f"Connected by {addr}")

# You can now communicate with the client
# For example, receive data:
data = conn.recv(1024) # receive up to 1024 bytes
print(f"Received: {data.decode()}")

# Send a response:
conn.send(b"Hello from server!")

# Close the connection
conn.close()
s.close()
