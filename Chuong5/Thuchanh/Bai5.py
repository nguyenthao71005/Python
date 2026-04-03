filePath = r"D:\NguyenPhuongThao\Chuong5\file\demo_file2.txt"
with open(filePath, "r", encoding="utf-8") as file:
    content = file.read()
# Tach tu
words = content.split()
# dem so lan xuat hien cua moi tu
wordcount = {}
for word in words:
    if word in wordcount:
        wordcount[word] += 1
    else:
        wordcount[word] = 1
print(wordcount)