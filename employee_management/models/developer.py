"""Lop LapTrinhVien ke thua tu NhanVien."""

from models.employee import NhanVien


class LapTrinhVien(NhanVien):
    """Nhan vien lap trinh co ngon ngu chinh va so gio tang ca."""

    def __init__(
        self,
        ma_nhan_vien: str,
        ho_ten: str,
        tuoi: int,
        email: str,
        phong_ban: str,
        luong_co_ban: float,
        ngon_ngu_lap_trinh: str,
        gio_tang_ca: int = 0,
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
        # Thong tin rieng cho lap trinh vien.
        self.ngon_ngu_lap_trinh = ngon_ngu_lap_trinh
        self.gio_tang_ca = gio_tang_ca

    @property
    def loai_nhan_vien(self) -> str:
        return "LapTrinhVien"

    def tinh_luong(self) -> float:
        """Luong LapTrinhVien = luong co ban + tien tang ca."""
        return self.luong_co_ban + (self.gio_tang_ca * 150)

    def lay_mo_ta_rieng(self) -> str:
        """Mo ta ngan gon cho lap trinh vien."""
        return f"Ngon ngu: {self.ngon_ngu_lap_trinh}, OT: {self.gio_tang_ca} gio"
