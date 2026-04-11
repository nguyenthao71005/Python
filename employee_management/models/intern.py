"""Lop ThucTapSinh ke thua tu NhanVien."""

from models.employee import NhanVien


class ThucTapSinh(NhanVien):
    """Thuc tap sinh co thong tin truong hoc va thoi gian thuc tap."""

    def __init__(
        self,
        ma_nhan_vien: str,
        ho_ten: str,
        tuoi: int,
        email: str,
        phong_ban: str,
        luong_co_ban: float,
        ten_truong: str,
        so_thang_thuc_tap: int,
        diem_hieu_suat: float = 0.0,
    ) -> None:
        super().__init__(
            ma_nhan_vien,
            ho_ten,
            tuoi,
            email,
            phong_ban,
            luong_co_ban,
            diem_hieu_suat,
        )
        # Thong tin bo sung danh cho thuc tap sinh.
        self.ten_truong = ten_truong
        self.so_thang_thuc_tap = so_thang_thuc_tap

    @property
    def loai_nhan_vien(self) -> str:
        return "ThucTapSinh"

    def tinh_luong(self) -> float:
        """Luong ThucTapSinh = 85% luong co ban."""
        return self.luong_co_ban * 0.85

    def lay_mo_ta_rieng(self) -> str:
        """Mo ta ngan gon cho thuc tap sinh."""
        return f"Truong: {self.ten_truong}, Thuc tap: {self.so_thang_thuc_tap} thang"
