"""Lop co so cho moi nhan vien trong he thong."""

from __future__ import annotations

from abc import ABC, abstractmethod

from exceptions.employee_exceptions import LoiLuongKhongHopLe, LoiTuoiKhongHopLe


class NhanVien(ABC):
    """Lop nen chua thong tin va hanh vi chung cua nhan vien."""

    def __init__(
        self,
        ma_nhan_vien: str,
        ho_ten: str,
        tuoi: int,
        email: str,
        phong_ban: str,
        luong_co_ban: float,
        diem_hieu_suat: float = 0.0,
    ) -> None:
        # Thong tin co ban cua nhan vien.
        self.ma_nhan_vien = ma_nhan_vien
        self.ho_ten = ho_ten
        self.tuoi = self._kiem_tra_tuoi(tuoi)
        self.email = email
        self.phong_ban = phong_ban
        self.luong_co_ban = self._kiem_tra_luong(luong_co_ban)
        self.diem_hieu_suat = diem_hieu_suat
        self.du_an: list[str] = []

    @staticmethod
    def _kiem_tra_tuoi(tuoi: int) -> int:
        """Kiem tra tuoi nhan vien phai nam trong khoang 18-65."""
        if tuoi < 18 or tuoi > 65:
            raise LoiTuoiKhongHopLe("Tuoi phai nam trong khoang 18 den 65.")
        return tuoi

    @staticmethod
    def _kiem_tra_luong(luong_co_ban: float) -> float:
        """Kiem tra luong co ban phai lon hon 0."""
        if luong_co_ban <= 0:
            raise LoiLuongKhongHopLe("Luong co ban phai lon hon 0.")
        return luong_co_ban

    def them_du_an(self, ten_du_an: str) -> None:
        """Them du an moi cho nhan vien neu du an chua ton tai."""
        if ten_du_an not in self.du_an:
            self.du_an.append(ten_du_an)

    def xoa_du_an(self, ten_du_an: str) -> None:
        """Xoa du an khoi danh sach du an cua nhan vien."""
        if ten_du_an in self.du_an:
            self.du_an.remove(ten_du_an)

    def cap_nhat_hieu_suat(self, diem_so: float) -> None:
        """Cap nhat diem hieu suat trong khoang 0-10."""
        if diem_so < 0 or diem_so > 10:
            raise ValueError("Diem hieu suat phai nam trong khoang 0 den 10.")
        self.diem_hieu_suat = diem_so

    @property
    @abstractmethod
    def loai_nhan_vien(self) -> str:
        """Tra ve ten loai nhan vien."""

    @abstractmethod
    def tinh_luong(self) -> float:
        """Tinh luong theo tung loai nhan vien."""

    @abstractmethod
    def lay_mo_ta_rieng(self) -> str:
        """Tra ve thong tin rieng cua tung vai tro."""
