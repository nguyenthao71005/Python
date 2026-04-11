"""Lop QuanLy ke thua tu NhanVien."""

from models.employee import NhanVien


class QuanLy(NhanVien):
    """Nhan vien quan ly co phu cap va quan ly so luong thanh vien."""

    def __init__(
        self,
        ma_nhan_vien: str,
        ho_ten: str,
        tuoi: int,
        email: str,
        phong_ban: str,
        luong_co_ban: float,
        so_luong_nhom: int,
        phu_cap: float = 3000.0,
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
        # Thong tin rieng cho vi tri quan ly.
        self.so_luong_nhom = so_luong_nhom
        self.phu_cap = phu_cap

    @property
    def loai_nhan_vien(self) -> str:
        return "QuanLy"

    def tinh_luong(self) -> float:
        """Luong QuanLy = luong co ban + phu cap + thuong theo nhom."""
        return self.luong_co_ban + self.phu_cap + (self.so_luong_nhom * 200)

    def lay_mo_ta_rieng(self) -> str:
        """Mo ta ngan gon cho vi tri quan ly."""
        return f"Quan ly {self.so_luong_nhom} nhan vien"
