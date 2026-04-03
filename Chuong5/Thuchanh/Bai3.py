filePath = r"D:\NguyenPhuongThao\Chuong5\file\demo_file1.txt"
with open(filePath, "r", encoding="utf-8") as file:
    content = file.read()
    print("Nội dung file trên một dòng:")
    print(content.replace("\n", " "))
with open(filePath, "r", encoding="utf-8") as file:
    print("Nội dung file theo từng dòng:")
    for line in file:
        print(line.strip())