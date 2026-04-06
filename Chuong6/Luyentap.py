code = {'a':'!', 'b':'@', 'c':'#', 'd':'$'}

# tạo bảng giải mã
decode = {v:k for k,v in code.items()}

text = input("Nhập chuỗi: ")

# mã hóa
encoded = ""
for i in text:
    if i in code:
        encoded += code[i]
    else:
        encoded += i

print("Chuỗi mã hóa:", encoded)

# giải mã
decoded = ""
for i in encoded:
    if i in decode:
        decoded += decode[i]
    else:
        decoded += i

print("Chuỗi giải mã:", decoded)