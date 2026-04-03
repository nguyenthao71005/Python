filePath = r"D:\NguyenPhuongThao\Chuong5\file\setInfo.txt"

# Nhập thông tin cá nhân
ten = input("Nhập tên: ")
tuoi = input("Nhập tuổi: ")
email = input("Nhập email: ")
skype = input("Nhập skype: ")
dia_chi = input("Nhập địa chỉ: ")
noi_lam_viec = input("Nhập nơi làm việc: ")

# a) Lưu thông tin vào file
with open(filePath, "w", encoding="utf-8") as file:
    file.write("Tên: " + ten + "\n")
    file.write("Tuổi: " + tuoi + "\n")
    file.write("Email: " + email + "\n")
    file.write("Skype: " + skype + "\n")
    file.write("Địa chỉ: " + dia_chi + "\n")
    file.write("Nơi làm việc: " + noi_lam_viec + "\n")

print("\nĐã lưu thông tin vào file setInfo.txt")

# b) Đọc thông tin từ file và hiển thị ra màn hình
with open(filePath, "r", encoding="utf-8") as file:
    content = file.read()

print("\nThông tin đọc từ file:")
print(content)