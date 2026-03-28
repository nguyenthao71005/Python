import time
_namsinh = int(input("Nhập vào năm sinh: "))
_x = time.localtime().tm_year
_tuoi = _x - _namsinh
if _tuoi < 0:
    print("Năm sinh không hợp lệ")
else:
    print("Tuổi của bạn là:", _tuoi)