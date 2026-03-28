_a = int(input("Nhap vao so a: "))
_b = int(input("Nhap vao so b: "))
_c = int(input("Nhap vao so c: "))

if _a > 0 and _b > 0 and _c > 0 and _a + _b > _c and _a + _c > _b and _b + _c > _a:
    print("Do dai ba canh tam giac")
else:
    print("Day khong phai do dai ba canh tam giac")
