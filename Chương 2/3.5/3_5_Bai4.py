_n = int(input("Nhập một số nguyên dương: "))

if _n > 0:
    if _n % 2 == 0:
        if _n % 3 == 0:
            print(_n, "chia hết cho cả 2 và 3")
        else:
            print(_n, "chia hết cho 2")
    else:
        if _n % 3 == 0:
            print(_n, "chia hết cho 3")
        else:
            print(_n, "không chia hết cho 2 hoặc 3")
else:
    print("Vui lòng nhập số nguyên dương.")
