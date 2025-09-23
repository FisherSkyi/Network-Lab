import socket

client = socket.socket()
client.connect(('localhost', 50154))  # Connect to your server
client.send(b"Hello server!")
response = client.recv(1024)
print(f"Received from server: {response.decode()}")
client.close()