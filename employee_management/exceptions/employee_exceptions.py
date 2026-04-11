"""Cac exception rieng cho he thong quan ly nhan vien."""


class LoiNhanVien(Exception):
    """Lop loi goc cho cac loi lien quan den nhan vien."""


class LoiKhongTimThayNhanVien(LoiNhanVien):
    """Bao loi khi tim nhan vien theo ID nhung khong ton tai."""

    def __init__(self, ma_nhan_vien: str) -> None:
        self.ma_nhan_vien = ma_nhan_vien
        super().__init__(f"Khong tim thay nhan vien co ID: {ma_nhan_vien}")


class LoiLuongKhongHopLe(LoiNhanVien):
    """Bao loi khi luong nhap vao nho hon hoac bang 0."""


class LoiTuoiKhongHopLe(LoiNhanVien):
    """Bao loi khi tuoi nam ngoai khoang cho phep."""


class LoiPhanCongDuAn(LoiNhanVien):
    """Bao loi khi phan cong du an vuot gioi han."""


class LoiTrungMaNhanVien(LoiNhanVien):
    """Bao loi khi ma nhan vien bi trung."""


EmployeeException = LoiNhanVien
EmployeeNotFoundError = LoiKhongTimThayNhanVien
InvalidSalaryError = LoiLuongKhongHopLe
InvalidAgeError = LoiTuoiKhongHopLe
ProjectAllocationError = LoiPhanCongDuAn
DuplicateEmployeeError = LoiTrungMaNhanVien
