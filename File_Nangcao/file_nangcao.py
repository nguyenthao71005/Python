import os
import re
import ast
import difflib


# Loại bỏ khoảng trắng và comment để việc so sánh văn bản chính xác hơn.
def normalize(code):
    return re.sub(r"\s+", "", re.sub(r"#.*", "", code))


# Tính mức độ giống nhau giữa hai chuỗi dưới dạng phần trăm.
def similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio() * 100


# So sánh cấu trúc cú pháp của hai đoạn code bằng cây AST.
def ast_similarity(code1, code2):
    try:
        return similarity(ast.dump(ast.parse(code1)), ast.dump(ast.parse(code2)))
    except:
        return 0


# Thư mục chứa các file Python cần mang ra so sánh.
thu_muc = r"File_nangcao\Kiem_tra"
files = [f for f in os.listdir(thu_muc) if f.endswith(".py")]

print("Danh sách file:")
# In danh sách file để người dùng chọn theo số thứ tự.
for i, f in enumerate(files, 1):
    print(f"{i}. {f}")

# Nhận hai lựa chọn file từ người dùng.
chon1 = int(input("Chọn file thứ nhất: "))
chon2 = int(input("Chọn file thứ hai: "))

# Tạo đường dẫn đầy đủ đến hai file đã chọn.
file1 = os.path.join(thu_muc, files[chon1 - 1])
file2 = os.path.join(thu_muc, files[chon2 - 1])

with open(file1, "r", encoding="utf-8") as f:
    code1 = f.read()

with open(file2, "r", encoding="utf-8") as f:
    code2 = f.read()

# So sánh theo nội dung văn bản và theo cấu trúc xử lý.
text_sim = similarity(normalize(code1), normalize(code2))
logic_sim = ast_similarity(code1, code2)

print("\n===== KẾT QUẢ =====")
print("File 1:", files[chon1 - 1])
print("File 2:", files[chon2 - 1])
print(f"Độ trùng lặp code: {text_sim:.2f}%")
print(f"Độ giống nhau về cách giải quyết: {logic_sim:.2f}%")
