filePath = "D:\\NguyenPhuongThao\\Chuong5\\file\\test.txt"
file = open(filePath, "r+")
content = file.read()
print(content)
file.close()