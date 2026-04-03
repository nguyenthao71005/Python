import os
import ast
import io
import math
import tokenize
import difflib
from collections import Counter


def lay_danh_sach_file_py(thu_muc):
    # Lấy danh sách các file Python trong thư mục và sắp xếp tăng dần.
    ds = []
    for file in os.listdir(thu_muc):
        duong_dan = os.path.join(thu_muc, file)
        if os.path.isfile(duong_dan) and file.endswith(".py"):
            ds.append(file)
    return sorted(ds)


def doc_file(file_path):
    # Đọc toàn bộ nội dung của một file.
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def chuan_hoa_code(text):
    # Chuẩn hóa code thành chuỗi token để việc so sánh ổn định hơn.
    # Tên biến sẽ được đổi thành IDENT, chuỗi thành STRING, số thành NUMBER.
    tokens = []
    stream = io.StringIO(text)

    try:
        for tok in tokenize.generate_tokens(stream.readline):
            tok_type = tok.type
            tok_string = tok.string

            # Bỏ qua các thành phần không ảnh hưởng nhiều đến logic chương trình.
            if tok_type in {
                tokenize.COMMENT,
                tokenize.NL,
                tokenize.NEWLINE,
                tokenize.INDENT,
                tokenize.DEDENT,
                tokenize.ENDMARKER,
                tokenize.ENCODING,
            }:
                continue

            if tok_type == tokenize.NAME:
                # Giữ nguyên từ khóa Python, còn tên biến/hàm sẽ chuẩn hóa về IDENT.
                if tok_string in {
                    "def", "class", "if", "elif", "else", "for", "while", "try",
                    "except", "finally", "with", "return", "import", "from",
                    "as", "pass", "break", "continue", "lambda", "yield",
                    "True", "False", "None", "and", "or", "not", "in", "is"
                }:
                    tokens.append(tok_string)
                else:
                    tokens.append("IDENT")
            elif tok_type == tokenize.STRING:
                tokens.append("STRING")
            elif tok_type == tokenize.NUMBER:
                tokens.append("NUMBER")
            else:
                tokens.append(tok_string)

    except tokenize.TokenError:
        # Nếu tokenize lỗi, tạm quay về so sánh bằng văn bản đã rút gọn khoảng trắng.
        return " ".join(text.split())

    return " ".join(tokens)


def do_trung_lap_code(text1, text2):
    # Tính phần trăm trùng lặp mã nguồn sau khi chuẩn hóa.
    norm1 = chuan_hoa_code(text1)
    norm2 = chuan_hoa_code(text2)
    return difflib.SequenceMatcher(None, norm1, norm2).ratio() * 100


class ASTFeatureExtractor(ast.NodeVisitor):
    def __init__(self):
        # Lưu số lần xuất hiện của từng loại node trong AST.
        self.features = Counter()

    def generic_visit(self, node):
        # Duyệt toàn bộ node và tăng bộ đếm tương ứng.
        self.features[type(node).__name__] += 1
        super().generic_visit(node)


def lay_dac_trung_ast(text):
    # Chuyển code sang AST và rút trích đặc trưng cấu trúc.
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return Counter()

    extractor = ASTFeatureExtractor()
    extractor.visit(tree)
    return extractor.features


def cosine_similarity(counter1, counter2):
    # Tính độ tương đồng cosine giữa hai vector đặc trưng.
    keys = set(counter1.keys()) | set(counter2.keys())
    if not keys:
        return 0.0

    dot = sum(counter1[k] * counter2[k] for k in keys)
    norm1 = math.sqrt(sum(counter1[k] ** 2 for k in keys))
    norm2 = math.sqrt(sum(counter2[k] ** 2 for k in keys))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot / (norm1 * norm2)


def do_giong_nhau_cach_giai_quyet(text1, text2):
    # So sánh mức độ giống nhau về cách tổ chức lời giải.
    f1 = lay_dac_trung_ast(text1)
    f2 = lay_dac_trung_ast(text2)
    return cosine_similarity(f1, f2) * 100


def xep_loai(diem):
    # Phân loại mức độ tương đồng theo thang điểm.
    if diem >= 85:
        return "Rất cao"
    elif diem >= 70:
        return "Cao"
    elif diem >= 50:
        return "Trung bình"
    elif diem >= 30:
        return "Thấp"
    else:
        return "Rất thấp"


def main():
    # Thư mục chứa các file cần so sánh.
    thu_muc = r"File_nangcao\Kiem_tra"

    # Kiểm tra xem thư mục đầu vào có tồn tại không.
    if not os.path.isdir(thu_muc):
        print("Không tìm thấy thư mục:", thu_muc)
        return

    # Lấy danh sách file .py trong thư mục.
    ds_file = lay_danh_sach_file_py(thu_muc)

    # Chương trình chỉ chạy khi có ít nhất 2 file.
    if len(ds_file) < 2:
        print("Cần ít nhất 2 file .py trong thư mục để so sánh.")
        return

    # Hiển thị các file để người dùng chọn.
    print("Danh sách file trong thư mục Kiem_tra:")
    for i, file in enumerate(ds_file, start=1):
        print(f"{i}. {file}")

    try:
        # Nhập vị trí của 2 file cần mang ra so sánh.
        chon1 = int(input("Chọn file thứ nhất: "))
        chon2 = int(input("Chọn file thứ hai: "))

        # Kiểm tra lựa chọn có hợp lệ không.
        if chon1 < 1 or chon1 > len(ds_file) or chon2 < 1 or chon2 > len(ds_file):
            print("Lựa chọn không hợp lệ.")
            return

        # Không cho phép chọn trùng một file.
        if chon1 == chon2:
            print("Phải chọn 2 file khác nhau.")
            return

        # Tạo đường dẫn đầy đủ đến 2 file được chọn.
        file1 = os.path.join(thu_muc, ds_file[chon1 - 1])
        file2 = os.path.join(thu_muc, ds_file[chon2 - 1])

        # Đọc nội dung 2 file để phân tích.
        text1 = doc_file(file1)
        text2 = doc_file(file2)

        # Tính các chỉ số tương đồng và điểm tổng hợp.
        trung_lap_code = do_trung_lap_code(text1, text2)
        giong_cach_lam = do_giong_nhau_cach_giai_quyet(text1, text2)
        diem_tong = 0.6 * trung_lap_code + 0.4 * giong_cach_lam

        # In ra kết quả cuối cùng cho người dùng.
        print("\n---------- KẾT QUẢ ----------")
        print("File 1:", ds_file[chon1 - 1])
        print("File 2:", ds_file[chon2 - 1])
        print(f"Mức độ trùng lặp code: {trung_lap_code:.2f}%")
        print(f"Mức độ giống nhau về cách giải quyết: {giong_cach_lam:.2f}%")
        print(f"Điểm tổng hợp: {diem_tong:.2f}%")
        print("Đánh giá:", xep_loai(diem_tong))

    except ValueError:
        # Báo lỗi nếu người dùng nhập không phải số nguyên.
        print("Vui lòng nhập số nguyên hợp lệ.")


if __name__ == "__main__":
    main()
