filePath = r"D:\NguyenPhuongThao\Chuong5\file\Bai2.txt"
vanban = input("Nhập đoạn văn bản: ")
with open(filePath, "w", encoding="utf-8") as file:
    file.write(vanban)
with open(filePath, "r", encoding="utf-8") as file:
    noidung = file.read()
print(noidung)