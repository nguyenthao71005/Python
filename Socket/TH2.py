import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    data = input("Nhập dữ liệu: ")
    s.sendto(data.encode("utf-8"), ("26.203.147.138", 6666))
    data, addr = s.recvfrom(1024)
    print(data.decode("utf-8"))
s.close()