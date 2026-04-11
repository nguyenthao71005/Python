"""Ham xu ly tinh luong va thong ke luong."""


def tinh_tong_luong(danh_sach_nhan_vien: list) -> float:
    """Tinh tong luong cua toan cong ty."""
    # Cong don luong thuc nhan cua tung nhan vien.
    return sum(nhan_vien.tinh_luong() for nhan_vien in danh_sach_nhan_vien)


def lay_top_luong_cao(danh_sach_nhan_vien: list, so_luong: int = 3) -> list:
    """Lay top nhan vien co muc luong cao nhat."""
    # Sap xep giam dan theo luong roi cat lay so luong can hien thi.
    return sorted(danh_sach_nhan_vien, key=lambda nhan_vien: nhan_vien.tinh_luong(), reverse=True)[:so_luong]


def thong_ke_luong_theo_phong(danh_sach_nhan_vien: list) -> dict[str, float]:
    """Thong ke tong luong cua tung phong ban."""
    tong_luong_theo_phong: dict[str, float] = {}
    for nhan_vien in danh_sach_nhan_vien:
        # setdefault tranh phai kiem tra phong ban da ton tai trong dict hay chua.
        tong_luong_theo_phong.setdefault(nhan_vien.phong_ban, 0)
        tong_luong_theo_phong[nhan_vien.phong_ban] += nhan_vien.tinh_luong()
    return tong_luong_theo_phong
