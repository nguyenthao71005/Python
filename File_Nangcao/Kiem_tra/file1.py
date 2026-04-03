n = int(input("Nhập một số nguyên dương: "))
giaithua = 1
while n > 0:
    giaithua *= n
    n -= 1
print("Giai thừa là:", giaithua)