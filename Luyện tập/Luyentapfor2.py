n = int(input("Nhap vao so nguyen n: "))

if n > 10:
    print("So nhap vao phai be hon 10.")
else:
    for i in range(2, n + 1, 2):
        print(i)
