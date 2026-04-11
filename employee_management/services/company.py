"""Lop CongTy chua toan bo nghiep vu quan ly nhan vien."""

from __future__ import annotations

from exceptions.employee_exceptions import (
    LoiKhongTimThayNhanVien,
    LoiPhanCongDuAn,
    LoiTrungMaNhanVien,
)
from models.developer import LapTrinhVien
from models.intern import ThucTapSinh
from models.manager import QuanLy
from services.payroll import lay_top_luong_cao, thong_ke_luong_theo_phong, tinh_tong_luong


class CongTy:
    """Quan ly danh sach nhan vien va xu ly cac nghiep vu nhan su."""

    def __init__(self, ten_cong_ty: str) -> None:
        # Danh sach nhan vien duoc luu truc tiep trong bo nho.
        self.ten_cong_ty = ten_cong_ty
        self.danh_sach_nhan_vien: list = []
        self.bo_dem_ma = 1

    def tao_ma_nhan_vien(self, tien_to: str = "EMP") -> str:
        """Tu dong tao ma nhan vien moi theo tien to vai tro."""
        ma_nhan_vien = f"{tien_to}{self.bo_dem_ma:03d}"
        self.bo_dem_ma += 1
        return ma_nhan_vien

    def _kiem_tra_trung_ma(self, ma_nhan_vien: str) -> None:
        """Bao loi neu ma nhan vien da ton tai trong danh sach."""
        if any(nhan_vien.ma_nhan_vien.lower() == ma_nhan_vien.lower() for nhan_vien in self.danh_sach_nhan_vien):
            raise LoiTrungMaNhanVien(f"Trung ID {ma_nhan_vien}")

    def them_nhan_vien(self, nhan_vien) -> None:
        """Them nhan vien vao cong ty, neu trung ma thi sinh ma moi."""
        try:
            self._kiem_tra_trung_ma(nhan_vien.ma_nhan_vien)
        except LoiTrungMaNhanVien:
            # Tach phan chu trong ma cu de giu dung tien to vai tro khi sinh ma moi.
            tien_to = "".join(ky_tu for ky_tu in nhan_vien.ma_nhan_vien if ky_tu.isalpha()) or "EMP"
            nhan_vien.ma_nhan_vien = self.tao_ma_nhan_vien(tien_to)
        self.danh_sach_nhan_vien.append(nhan_vien)

    def tao_quan_ly(self, **du_lieu) -> QuanLy:
        """Khoi tao va them mot nhan vien quan ly."""
        nhan_vien = QuanLy(**du_lieu)
        self.them_nhan_vien(nhan_vien)
        return nhan_vien

    def tao_lap_trinh_vien(self, **du_lieu) -> LapTrinhVien:
        """Khoi tao va them mot lap trinh vien."""
        nhan_vien = LapTrinhVien(**du_lieu)
        self.them_nhan_vien(nhan_vien)
        return nhan_vien

    def tao_thuc_tap_sinh(self, **du_lieu) -> ThucTapSinh:
        """Khoi tao va them mot thuc tap sinh."""
        nhan_vien = ThucTapSinh(**du_lieu)
        self.them_nhan_vien(nhan_vien)
        return nhan_vien

    def lay_tat_ca_nhan_vien(self) -> list:
        """Tra ve toan bo danh sach nhan vien hien co."""
        return self.danh_sach_nhan_vien

    def kiem_tra_co_du_lieu(self) -> None:
        """Bao loi neu danh sach nhan vien dang rong."""
        if not self.danh_sach_nhan_vien:
            raise IndexError("Chua co du lieu.")

    def tim_theo_ma(self, ma_nhan_vien: str):
        """Tim va tra ve nhan vien theo ma."""
        for nhan_vien in self.danh_sach_nhan_vien:
            if nhan_vien.ma_nhan_vien.lower() == ma_nhan_vien.lower():
                return nhan_vien
        raise LoiKhongTimThayNhanVien(ma_nhan_vien)

    def tim_theo_ten(self, tu_khoa: str) -> list:
        """Tim nhan vien theo mot phan ho ten."""
        return [nhan_vien for nhan_vien in self.danh_sach_nhan_vien if tu_khoa.lower() in nhan_vien.ho_ten.lower()]

    def tim_lap_trinh_vien_theo_ngon_ngu(self, ngon_ngu: str) -> list:
        """Loc danh sach lap trinh vien theo ngon ngu lap trinh."""
        return [
            nhan_vien
            for nhan_vien in self.danh_sach_nhan_vien
            # Chi lay dung lap trinh vien va so sanh ngon ngu khong phan biet hoa thuong.
            if nhan_vien.loai_nhan_vien == "LapTrinhVien"
            and nhan_vien.ngon_ngu_lap_trinh.lower() == ngon_ngu.lower()
        ]

    def loc_theo_loai(self, loai_nhan_vien: str) -> list:
        """Loc danh sach nhan vien theo ten loai."""
        return [
            nhan_vien
            for nhan_vien in self.danh_sach_nhan_vien
            if nhan_vien.loai_nhan_vien.lower() == loai_nhan_vien.lower()
        ]

    def sap_xep_theo_hieu_suat(self) -> list:
        """Sap xep nhan vien theo diem hieu suat giam dan."""
        # reverse=True de nhan vien diem cao xuat hien truoc.
        return sorted(self.danh_sach_nhan_vien, key=lambda nhan_vien: nhan_vien.diem_hieu_suat, reverse=True)

    def phan_cong_du_an(self, ma_nhan_vien: str, ten_du_an: str) -> None:
        """Gan mot du an cho nhan vien, toi da 5 du an."""
        nhan_vien = self.tim_theo_ma(ma_nhan_vien)
        # Moi nhan vien chi duoc tham gia toi da 5 du an.
        if len(nhan_vien.du_an) >= 5:
            raise LoiPhanCongDuAn("Nhan vien da co toi da 5 du an.")
        nhan_vien.them_du_an(ten_du_an)

    def xoa_khoi_du_an(self, ma_nhan_vien: str, ten_du_an: str) -> None:
        """Xoa nhan vien khoi mot du an cu the."""
        nhan_vien = self.tim_theo_ma(ma_nhan_vien)
        nhan_vien.xoa_du_an(ten_du_an)

    def lay_du_an_cua_nhan_vien(self, ma_nhan_vien: str) -> list[str]:
        """Tra ve danh sach du an cua mot nhan vien."""
        return self.tim_theo_ma(ma_nhan_vien).du_an

    def lay_top_nhieu_du_an_nhat(self, so_luong: int = 10) -> list:
        """Lay danh sach nhan vien tham gia nhieu du an nhat."""
        # Sap xep giam dan theo so du an, neu bang nhau thi uu tien ten de hien thi on dinh.
        return sorted(
            self.danh_sach_nhan_vien,
            key=lambda nhan_vien: (-len(nhan_vien.du_an), nhan_vien.ho_ten.lower()),
        )[:so_luong]

    def lay_top_it_du_an_nhat(self, so_luong: int = 10) -> list:
        """Lay danh sach nhan vien tham gia it du an nhat."""
        return sorted(
            self.danh_sach_nhan_vien,
            key=lambda nhan_vien: (len(nhan_vien.du_an), nhan_vien.ho_ten.lower()),
        )[:so_luong]

    def lay_thanh_vien_theo_du_an(self, ten_du_an: str) -> list:
        """Lay danh sach nhan vien dang tham gia mot du an cu the."""
        return [
            nhan_vien
            for nhan_vien in self.danh_sach_nhan_vien
            if ten_du_an.lower() in (du_an.lower() for du_an in nhan_vien.du_an)
        ]

    def cap_nhat_hieu_suat(self, ma_nhan_vien: str, diem_so: float) -> None:
        """Cap nhat diem hieu suat cho nhan vien theo ma."""
        nhan_vien = self.tim_theo_ma(ma_nhan_vien)
        nhan_vien.cap_nhat_hieu_suat(diem_so)

    def lay_nhan_vien_xuat_sac(self) -> list:
        """Lay danh sach nhan vien co diem hieu suat tren 8."""
        return [nhan_vien for nhan_vien in self.danh_sach_nhan_vien if nhan_vien.diem_hieu_suat > 8]

    def lay_nhan_vien_can_cai_thien(self) -> list:
        """Lay danh sach nhan vien co diem hieu suat duoi 5."""
        return [nhan_vien for nhan_vien in self.danh_sach_nhan_vien if nhan_vien.diem_hieu_suat < 5]

    def xoa_nhan_vien(self, ma_nhan_vien: str) -> None:
        """Xoa nhan vien ra khoi danh sach cong ty."""
        nhan_vien = self.tim_theo_ma(ma_nhan_vien)
        self.danh_sach_nhan_vien.remove(nhan_vien)

    def cat_giam_nhan_su(self, so_luong: int) -> list:
        """Cho nghi viec mot nhom nhan vien co hieu suat thap nhat."""
        if so_luong <= 0:
            raise ValueError("So luong cat giam phai lon hon 0.")
        if so_luong > len(self.danh_sach_nhan_vien):
            raise ValueError("So luong cat giam vuot qua tong so nhan vien hien co.")

        # Mac dinh cat giam nhom co diem hieu suat thap nhat de de thao tac nhanh.
        danh_sach_cat_giam = sorted(
            self.danh_sach_nhan_vien,
            key=lambda nhan_vien: (nhan_vien.diem_hieu_suat, len(nhan_vien.du_an)),
        )[:so_luong]

        for nhan_vien in danh_sach_cat_giam:
            self.danh_sach_nhan_vien.remove(nhan_vien)

        return danh_sach_cat_giam

    def tang_luong_co_ban(self, ma_nhan_vien: str, so_tien: float) -> None:
        """Cong them luong co ban cho mot nhan vien."""
        nhan_vien = self.tim_theo_ma(ma_nhan_vien)
        nhan_vien.luong_co_ban += so_tien

    def thang_chuc_nhan_vien(self, ma_nhan_vien: str):
        """Thang chuc ThucTapSinh -> LapTrinhVien -> QuanLy."""
        nhan_vien = self.tim_theo_ma(ma_nhan_vien)

        if nhan_vien.loai_nhan_vien == "ThucTapSinh":
            # Khi len LapTrinhVien, gan mac dinh ngon ngu va muc luong toi thieu moi.
            nhan_vien_moi = LapTrinhVien(
                ma_nhan_vien=nhan_vien.ma_nhan_vien,
                ho_ten=nhan_vien.ho_ten,
                tuoi=nhan_vien.tuoi,
                email=nhan_vien.email,
                phong_ban=nhan_vien.phong_ban,
                luong_co_ban=max(nhan_vien.luong_co_ban * 1.5, 5000000),
                ngon_ngu_lap_trinh="Python",
                gio_tang_ca=0,
                diem_hieu_suat=nhan_vien.diem_hieu_suat,
            )
        elif nhan_vien.loai_nhan_vien == "LapTrinhVien":
            # Neu chua co du an nao thi van cho mot quy mo nhom toi thieu la 3.
            nhan_vien_moi = QuanLy(
                ma_nhan_vien=nhan_vien.ma_nhan_vien,
                ho_ten=nhan_vien.ho_ten,
                tuoi=nhan_vien.tuoi,
                email=nhan_vien.email,
                phong_ban=nhan_vien.phong_ban,
                luong_co_ban=max(nhan_vien.luong_co_ban * 1.7, 8000000),
                so_luong_nhom=max(len(nhan_vien.du_an), 3),
                phu_cap=3000000,
                diem_hieu_suat=nhan_vien.diem_hieu_suat,
            )
        else:
            raise ValueError("Quan ly khong the thang chuc them trong chuong trinh nay.")

        # Giu nguyen danh sach du an cu khi doi doi tuong nhan vien moi.
        nhan_vien_moi.du_an = nhan_vien.du_an.copy()
        vi_tri = self.danh_sach_nhan_vien.index(nhan_vien)
        self.danh_sach_nhan_vien[vi_tri] = nhan_vien_moi
        return nhan_vien_moi

    def dem_theo_loai(self) -> dict[str, int]:
        """Dem so luong nhan vien cua tung loai."""
        ket_qua = {"QuanLy": 0, "LapTrinhVien": 0, "ThucTapSinh": 0}
        for nhan_vien in self.danh_sach_nhan_vien:
            ket_qua[nhan_vien.loai_nhan_vien] += 1
        return ket_qua

    def trung_binh_du_an(self) -> float:
        """Tinh so du an trung binh tren moi nhan vien."""
        if not self.danh_sach_nhan_vien:
            return 0.0
        # Tong so du an chia cho tong so nhan vien de lay gia tri trung binh.
        tong_du_an = sum(len(nhan_vien.du_an) for nhan_vien in self.danh_sach_nhan_vien)
        return tong_du_an / len(self.danh_sach_nhan_vien)

    def tinh_tong_luong_cong_ty(self) -> float:
        """Tinh tong luong cua toan cong ty."""
        return tinh_tong_luong(self.danh_sach_nhan_vien)

    def lay_top_3_luong_cao(self) -> list:
        """Lay 3 nhan vien co luong cao nhat."""
        return lay_top_luong_cao(self.danh_sach_nhan_vien, so_luong=3)

    def thong_ke_luong_tung_phong(self) -> dict[str, float]:
        """Thong ke tong luong cua tung phong ban."""
        return thong_ke_luong_theo_phong(self.danh_sach_nhan_vien)
