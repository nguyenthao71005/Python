n = int(input("Nhập vào n: "))
if n < 20:
    for i in range(1, n):
        if i % 5 == 0 or i % 7 == 0:
            print(i)
else:
    print("Số nhập vào phải nhỏ hơn 20.")
