#! /usr/bin/python
# a simple tcp server
import socket

HOST = "0.0.0.0"
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

print(f"Start listening on {HOST}:{PORT}")
while True:
    try:
        connection, address = sock.accept()
        buf = connection.recv(1024)
        print(f"Received message - len = {len(buf)}")
        connection.send(buf)
        connection.close()
    except KeyboardInterrupt as e:
        exit(1)
