# client.py
# https://pythonspot.com/python-network-sockets-programming-tutorial/
# https://docs.python.org/3.4/howto/sockets.html

#!/usr/bin/env python
 
import socket
 
 
TCP_IP = '127.0.0.1'
TCP_PORT = 62
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(str.encode(MESSAGE))
data = s.recv(BUFFER_SIZE)
s.close()
 
print("received data:", data)
