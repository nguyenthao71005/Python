def tong(_x, _y):
    return _x + _y


def tongn(_z, *args):
    return _z + sum(args)


def kiemtrasonguyento(_n):
    if _n < 2:
        return False
    for i in range(2, int(_n ** 0.5) + 1):
        if _n % i == 0:
            return False
    return True


def timcacsonguyentotrongkhoang(a, b):
    if a > b:
        a, b = b, a
    primes = []
    for num in range(a, b + 1):
        if kiemtrasonguyento(num):
            primes.append(num)
    return primes


def kiemtrasohoanhao(_n):
    if _n < 1:
        return False
    tong_uoc = sum(i for i in range(1, _n) if _n % i == 0)
    return tong_uoc == _n


def timcacsohoanhaotrongkhoang(a, b):
    if a > b:
        a, b = b, a
    perfect_numbers = []
    for num in range(a, b + 1):
        if kiemtrasohoanhao(num):
            perfect_numbers.append(num)
    return perfect_numbers


while True:
    print("\n===== MENU CHỌN HÀM =====")
    print("1. Tính tổng 2 số")
    print("2. Tính tổng nhiều số")
    print("3. Kiểm tra số nguyên tố")
    print("4. Tìm các số nguyên tố trong khoảng")
    print("5. Kiểm tra số hoàn hảo")
    print("6. Tìm các số hoàn hảo trong khoảng")
    print("0. Thoát")

    chon = input("Nhập lựa chọn của bạn: ")

    if chon == "1":
        x = int(input("Nhập x: "))
        y = int(input("Nhập y: "))
        print("Tổng của x và y là:", tong(x, y))

    elif chon == "2":
        z = int(input("Nhập z: "))
        n = int(input("Nhập số lượng số muốn cộng thêm: "))
        args = []
        for i in range(n):
            so = int(input(f"Nhập số thứ {i+1}: "))
            args.append(so)
        print("Tổng của z và các số khác là:", tongn(z, *args))

    elif chon == "3":
        n = int(input("Nhập n: "))
        if kiemtrasonguyento(n):
            print(f"{n} là số nguyên tố")
        else:
            print(f"{n} không phải là số nguyên tố")

    elif chon == "4":
        a = int(input("Nhập a: "))
        b = int(input("Nhập b: "))
        ket_qua = timcacsonguyentotrongkhoang(a, b)
        print(f"Các số nguyên tố trong khoảng [{min(a, b)}, {max(a, b)}] là: {ket_qua}")

    elif chon == "5":
        n = int(input("Nhập n: "))
        if kiemtrasohoanhao(n):
            print(f"{n} là số hoàn hảo")
        else:
            print(f"{n} không phải là số hoàn hảo")

    elif chon == "6":
        a = int(input("Nhập a: "))
        b = int(input("Nhập b: "))
        ket_qua = timcacsohoanhaotrongkhoang(a, b)
        print(f"Các số hoàn hảo trong khoảng [{min(a, b)}, {max(a, b)}] là: {ket_qua}")

    elif chon == "0":
        print("Thoát chương trình.")
        break

    else:
        print("Lựa chọn không hợp lệ, vui lòng nhập lại!")