import socket
import time

client = socket.socket()
client.connect(('localhost', 50154))  # Connect to your server
print(f"Client connected to {client.getsockname()}")
print(f"My address and port: {client.getsockname()}")

try:
    # Send multiple HTTP requests over the same persistent connection
    requests = [
        b"GET /page1 HTTP/1.1\r\nHost: localhost\r\n\r\n",
        b"GET /page2 HTTP/1.1\r\nHost: localhost\r\n\r\n",
        b"POST /data HTTP/1.1\r\nHost: localhost\r\nContent-Length: 11\r\n\r\nHello World"
    ]
    
    for i, request in enumerate(requests, 1):
        # start counter by 1 for readability
        print(f"\n--- Sending request {i} ---")
        client.send(request)
        
        # Receive response
        response = client.recv(1024)
        if len(response) == 0:
            print("Server closed connection")
            break
            
        print(f"Received from server: {response.decode()}")
        
        # Small delay between requests to simulate real usage
        time.sleep(1)
    
    print("\n--- Keeping connection alive for 5 seconds ---")
    time.sleep(5)  # Keep connection open to test server's timeout handling
    # in server code, timeout is set to 30 seconds
    
    print("--- Sending final request ---")
    client.send(b"GET /final HTTP/1.1\r\nHost: localhost\r\n\r\n")
    response = client.recv(1024)
    if len(response) > 0:
        print(f"Final response: {response.decode()}")
    else:
        print("Server closed connection")

except socket.timeout:
    print("Client timed out")
except ConnectionResetError:
    print("Server closed connection unexpectedly")
except Exception as e:
    print(f"Client error: {e}")
finally:
    # Client closes connection (server should detect this)
    print("\n--- Client closing connection ---")
    client.close()
