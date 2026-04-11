"""Ham format de hien thi thong tin dep hon."""


def in_tieu_de(tieu_de: str) -> None:
    """In tieu de lon de tach ro tung khu vuc menu."""
    print("\n" + "=" * 70)
    print(tieu_de.center(70))
    print("=" * 70)


def in_thong_bao(thong_bao: str) -> None:
    """In thong bao ngan gon cho nguoi dung."""
    print(f">>> {thong_bao}")


def dinh_dang_tien(so_tien: float) -> str:
    """Dinh dang tien theo kieu co dau phay ngan cach hang nghin."""
    return f"{so_tien:,.0f} VND"


def in_bang_nhan_vien(danh_sach_nhan_vien: list) -> None:
    """Hien thi danh sach nhan vien duoi dang bang don gian."""
    if not danh_sach_nhan_vien:
        in_thong_bao("Chua co du lieu.")
        return

    header = (
        f"{'ID':<10}{'Ten':<20}{'Loai':<12}{'Phong ban':<15}"
        f"{'Luong':<15}{'Hieu suat':<10}"
    )
    print(header)
    print("-" * len(header))
    for nhan_vien in danh_sach_nhan_vien:
        print(
            f"{nhan_vien.ma_nhan_vien:<10}{nhan_vien.ho_ten:<20}{nhan_vien.loai_nhan_vien:<12}"
            f"{nhan_vien.phong_ban:<15}{dinh_dang_tien(nhan_vien.tinh_luong()):<15}"
            f"{nhan_vien.diem_hieu_suat:<10.1f}"
        )


def in_danh_sach_du_an(danh_sach_du_an: list[str]) -> None:
    """Hien thi danh sach du an cua mot nhan vien."""
    if not danh_sach_du_an:
        in_thong_bao("Nhan vien chua tham gia du an nao.")
        return

    for chi_so, du_an in enumerate(danh_sach_du_an, start=1):
        print(f"{chi_so}. {du_an}")


def in_bang_xep_hang_du_an(danh_sach_nhan_vien: list) -> None:
    """In bang xep hang theo so du an ma nhan vien dang tham gia."""
    if not danh_sach_nhan_vien:
        in_thong_bao("Chua co du lieu.")
        return

    header = f"{'ID':<10}{'Ten':<20}{'Loai':<16}{'So du an':<10}"
    print(header)
    print("-" * len(header))
    for nhan_vien in danh_sach_nhan_vien:
        print(
            f"{nhan_vien.ma_nhan_vien:<10}{nhan_vien.ho_ten:<20}"
            f"{nhan_vien.loai_nhan_vien:<16}{len(nhan_vien.du_an):<10}"
        )


def in_thanh_vien_du_an(ten_du_an: str, danh_sach_nhan_vien: list) -> None:
    """In danh sach thanh vien tham gia mot du an va chuc vu cua ho."""
    if not danh_sach_nhan_vien:
        in_thong_bao(f"Khong co thanh vien nao trong du an {ten_du_an}.")
        return

    print(f"Du an: {ten_du_an}")
    header = f"{'ID':<10}{'Ten':<20}{'Chuc vu':<16}{'Phong ban':<15}"
    print(header)
    print("-" * len(header))
    for nhan_vien in danh_sach_nhan_vien:
        print(
            f"{nhan_vien.ma_nhan_vien:<10}{nhan_vien.ho_ten:<20}"
            f"{nhan_vien.loai_nhan_vien:<16}{nhan_vien.phong_ban:<15}"
        )
