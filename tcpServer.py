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
print(f"Server listening on {s.getsockname()}") # ('0.0.0.0', 50154)

# Accept incoming connections
print("Waiting for connections...")
conn, addr = s.accept()
print(f"Connected by {addr}")

# Set timeout to detect stalled connections
conn.settimeout(30.0)  # 30 second timeout

# Handle persistent connection with reliable disconnection detection
try:
    while True:
        # Receive data from client
        data = conn.recv(1024)
        
        # Check for disconnection: empty bytes means connection closed
        if len(data) == 0:
            print("Client disconnected (connection closed)")
            break
            
        print(f"Received: {data.decode()}")
        
        # Send response back to client
        response = b"HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello client!"
        conn.send(response)
        print("Response sent")
        
        # For HTTP 1.1 persistent connections, keep the connection open
        # and continue listening for more requests
        
except socket.timeout:
    print("Connection timed out - closing")
except ConnectionResetError:
    print("Client forcefully closed connection")
except Exception as e:
    print(f"Connection error: {e}")
finally:
    # Always close the connection when done
    conn.close()
    print("Connection closed")

s.close()
