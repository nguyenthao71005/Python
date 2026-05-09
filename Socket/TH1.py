import socket

SERVER_IP = "26.203.147.138"
SERVER_PORT = 6666

s = socket.socket()
s.connect((SERVER_IP, SERVER_PORT))
s.sendall("Nguyễn Phương Thảo".encode("utf-8"))
s.close()
