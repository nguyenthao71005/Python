class HocVien:
    def __init__(self,hoten,ngaysinh,email,dienthoai,diachi,lop):
        self.hoten = hoten
        self.ngaysinh = ngaysinh
        self.email = email
        self.dienthoai = dienthoai
        self.diachi = diachi
        self.lop = lop
    def show_info(self):
        print("Họ tên: ", self.hoten)
        print("Ngày sinh: ", self.ngaysinh)
        print("Email: ", self.email)
        print("Điện thoại: ", self.dienthoai)
        print("Địa chỉ: ", self.diachi)
        print("Lớp: ", self.lop)
    def change_infor(self, diachi = "HN",lop = "IT14.2"):
        self.diachi = diachi
        self.lop = lop
class Main:
    sv1 = HocVien("Nguyen Phuong Thao", "07/10/2005", "nguyenphuongthao@gmail.com", "0123456789", "Ha Noi", "IT14.2")
    sv1.show_info()
    sv1.change_infor()
    print("Sau khi thay đổi thông tin: ")
    sv1.show_info()