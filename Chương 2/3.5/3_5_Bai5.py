import math

_a = float(input("Nhập a: "))
_b = float(input("Nhập b: "))
_c = float(input("Nhập c: "))
_delta = _b**2 - 4 * _a * _c

if _a == 0:
    print("a phải khác 0")
else:
    if _delta < 0:
        print("Phương trình vô nghiệm")
    else:
        if _delta == 0:
            x = -_b / (2 * _a)
            print("Phương trình có nghiệm kép: x =", x)
        else:
            x1 = (-_b + math.sqrt(_delta)) / (2 * _a)
            x2 = (-_b - math.sqrt(_delta)) / (2 * _a)
            print("Phương trình có hai nghiệm phân biệt: x1 =", x1, "và x2 =", x2)
