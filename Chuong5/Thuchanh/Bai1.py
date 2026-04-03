filePath = r"D:\NguyenPhuongThao\Chuong5\file\Bai1.txt"
n = int(input("Nhập số dòng cần đọc: "))
with open(filePath, "r", encoding="utf-8") as file:
    for i in range(n):
        line = file.readline()
        if not line:
            break
        print(line, end="")