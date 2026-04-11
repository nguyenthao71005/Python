"""Chuong trinh chinh cua he thong quan ly nhan vien."""

from exceptions.employee_exceptions import (
    LoiKhongTimThayNhanVien,
    LoiLuongKhongHopLe,
    LoiPhanCongDuAn,
    LoiTuoiKhongHopLe,
)
from services.company import CongTy
from utils.formatters import (
    dinh_dang_tien,
    in_bang_nhan_vien,
    in_bang_xep_hang_du_an,
    in_danh_sach_du_an,
    in_thanh_vien_du_an,
    in_thong_bao,
    in_tieu_de,
)
from utils.validators import nhap_chuoi, nhap_email, nhap_so_nguyen, nhap_so_thuc


def tao_du_lieu_mau(cong_ty: CongTy) -> None:
    """Them san mot vai nhan vien de de kiem tra menu."""
    quan_ly = cong_ty.tao_quan_ly(
        ma_nhan_vien=cong_ty.tao_ma_nhan_vien("QL01"),
        ho_ten="Nguyen Van An",
        tuoi=20,
        email="an.manager@gmail.com",
        phong_ban="Management",
        luong_co_ban=18000000,
        so_luong_nhom=10,
        phu_cap=5000000,
        diem_hieu_suat=8,
    )
    lap_trinh_vien = cong_ty.tao_lap_trinh_vien(
        ma_nhan_vien=cong_ty.tao_ma_nhan_vien("LTV01"),
        ho_ten="Nguyen Phuong Thao",
        tuoi=27,
        email="thao.dev@gmail.com",
        phong_ban="IT",
        luong_co_ban=12000000,
        ngon_ngu_lap_trinh="Python",
        gio_tang_ca=10,
        diem_hieu_suat=7,
    )
    thuc_tap_sinh = cong_ty.tao_thuc_tap_sinh(
        ma_nhan_vien=cong_ty.tao_ma_nhan_vien("TTS01"),
        ho_ten="Nguyen Mai Phuong",
        tuoi=21,
        email="phuong.intern@gmail.com",
        phong_ban="IT",
        luong_co_ban=5000000,
        ten_truong="HCMUT",
        so_thang_thuc_tap=3,
        diem_hieu_suat=9,
    )

    # Gan san du an de nguoi dung co the xem ngay cac chuc nang moi.
    quan_ly.them_du_an("ERP")
    quan_ly.them_du_an("CRM")
    lap_trinh_vien.them_du_an("ERP")
    lap_trinh_vien.them_du_an("Website")
    lap_trinh_vien.them_du_an("Mobile App")
    thuc_tap_sinh.them_du_an("Website")


def tam_dung() -> None:
    """Tam dung de nguoi dung doc ket qua truoc khi quay lai menu."""
    input("\nNhan Enter de tiep tuc...")


def chon_menu_con(tieu_de: str, danh_sach_lua_chon: list[str]) -> int:
    """In menu con va tra ve lua chon hop le."""
    in_tieu_de(tieu_de)
    for lua_chon in danh_sach_lua_chon:
        print(lua_chon)
    return nhap_so_nguyen("Lua chon cua ban: ", 1, len(danh_sach_lua_chon))


def nhap_du_lieu_chung(cong_ty: CongTy, tien_to: str) -> dict:
    """Nhap cac truong thong tin chung duoc dung cho moi loai nhan vien."""
    ma_nhan_vien = nhap_chuoi("Nhap ID nhan vien (Enter de tu sinh): ", cho_phep_rong=True)
    if not ma_nhan_vien:
        # Neu bo trong ID, he thong tu sinh ma theo vai tro dang duoc them.
        ma_nhan_vien = cong_ty.tao_ma_nhan_vien(tien_to)

    return {
        "ma_nhan_vien": ma_nhan_vien,
        "ho_ten": nhap_chuoi("Nhap ho ten: "),
        "tuoi": nhap_so_nguyen("Nhap tuoi: "),
        "email": nhap_email("Nhap email: "),
        "phong_ban": nhap_chuoi("Nhap phong ban: "),
        "luong_co_ban": nhap_so_thuc("Nhap luong co ban: ", min_value=0.01),
    }


def menu_them_nhan_vien(cong_ty: CongTy) -> None:
    """Xu ly chuc nang them moi nhan vien theo tung loai."""
    lua_chon = chon_menu_con(
        "THEM NHAN VIEN MOI",
        ["1.1. Them Quan ly", "1.2. Them Lap trinh vien", "1.3. Them Thuc tap sinh"],
    )

    try:
        if lua_chon == 1:
            du_lieu = nhap_du_lieu_chung(cong_ty, "QL")
            du_lieu["so_luong_nhom"] = nhap_so_nguyen("Nhap so luong thanh vien nhom: ", 0)
            du_lieu["phu_cap"] = nhap_so_thuc("Nhap phu cap quan ly: ", min_value=0)
            nhan_vien = cong_ty.tao_quan_ly(**du_lieu)
        elif lua_chon == 2:
            du_lieu = nhap_du_lieu_chung(cong_ty, "LTV")
            du_lieu["ngon_ngu_lap_trinh"] = nhap_chuoi("Nhap ngon ngu lap trinh: ")
            du_lieu["gio_tang_ca"] = nhap_so_nguyen("Nhap so gio OT: ", 0)
            nhan_vien = cong_ty.tao_lap_trinh_vien(**du_lieu)
        else:
            du_lieu = nhap_du_lieu_chung(cong_ty, "TTS")
            du_lieu["ten_truong"] = nhap_chuoi("Nhap ten truong: ")
            du_lieu["so_thang_thuc_tap"] = nhap_so_nguyen("Nhap so thang thuc tap: ", 1)
            nhan_vien = cong_ty.tao_thuc_tap_sinh(**du_lieu)

        in_thong_bao(f"Them nhan vien thanh cong: {nhan_vien.ho_ten} - {nhan_vien.ma_nhan_vien}")
    except LoiTuoiKhongHopLe as loi:
        in_thong_bao(str(loi))
    except LoiLuongKhongHopLe as loi:
        in_thong_bao(str(loi))
    except ValueError as loi:
        in_thong_bao(str(loi))


def menu_hien_thi_nhan_vien(cong_ty: CongTy) -> None:
    """Hien thi danh sach nhan vien theo nhieu cach sap xep, loc."""
    try:
        # Chan thao tac tren danh sach rong de thong bao ro rang hon cho nguoi dung.
        cong_ty.kiem_tra_co_du_lieu()
        lua_chon = chon_menu_con(
            "HIEN THI DANH SACH NHAN VIEN",
            [
                "2.1. Tat ca nhan vien",
                "2.2. Theo loai (QuanLy/LapTrinhVien/ThucTapSinh)",
                "2.3. Theo hieu suat (tu cao den thap)",
            ],
        )

        if lua_chon == 1:
            in_bang_nhan_vien(cong_ty.lay_tat_ca_nhan_vien())
        elif lua_chon == 2:
            loai_nhan_vien = nhap_chuoi("Nhap loai nhan vien: ")
            in_bang_nhan_vien(cong_ty.loc_theo_loai(loai_nhan_vien))
        else:
            in_bang_nhan_vien(cong_ty.sap_xep_theo_hieu_suat())
    except IndexError:
        in_thong_bao("Chua co du lieu.")


def menu_tim_kiem_nhan_vien(cong_ty: CongTy) -> None:
    """Tim nhan vien theo ma, ten hoac ngon ngu lap trinh."""
    try:
        cong_ty.kiem_tra_co_du_lieu()
        lua_chon = chon_menu_con(
            "TIM KIEM NHAN VIEN",
            ["3.1. Theo ID", "3.2. Theo ten", "3.3. Theo ngon ngu lap trinh"],
        )

        if lua_chon == 1:
            nhan_vien = cong_ty.tim_theo_ma(nhap_chuoi("Nhap ID can tim: "))
            in_bang_nhan_vien([nhan_vien])
        elif lua_chon == 2:
            danh_sach = cong_ty.tim_theo_ten(nhap_chuoi("Nhap ten can tim: "))
            in_bang_nhan_vien(danh_sach)
        else:
            # Chi tim theo ngon ngu trong nhom lap trinh vien.
            danh_sach = cong_ty.tim_lap_trinh_vien_theo_ngon_ngu(nhap_chuoi("Nhap ngon ngu lap trinh: "))
            in_bang_nhan_vien(danh_sach)
    except LoiKhongTimThayNhanVien as loi:
        in_thong_bao(str(loi))
    except IndexError:
        in_thong_bao("Chua co du lieu.")


def menu_quan_ly_luong(cong_ty: CongTy) -> None:
    """Xem luong tung nhan vien, tong luong va top luong cao."""
    try:
        cong_ty.kiem_tra_co_du_lieu()
        lua_chon = chon_menu_con(
            "QUAN LY LUONG",
            [
                "4.1. Tinh luong cho tung nhan vien",
                "4.2. Tinh tong luong cong ty",
                "4.3. Top 3 nhan vien luong cao nhat",
            ],
        )

        if lua_chon == 1:
            in_bang_nhan_vien(cong_ty.lay_tat_ca_nhan_vien())
        elif lua_chon == 2:
            in_thong_bao(f"Tong luong cong ty: {dinh_dang_tien(cong_ty.tinh_tong_luong_cong_ty())}")
        else:
            in_bang_nhan_vien(cong_ty.lay_top_3_luong_cao())
    except IndexError:
        in_thong_bao("Chua co du lieu.")


def menu_quan_ly_du_an(cong_ty: CongTy) -> None:
    """Phan cong, xoa va xem du an cua nhan vien."""
    try:
        cong_ty.kiem_tra_co_du_lieu()
        lua_chon = chon_menu_con(
            "QUAN LY DU AN",
            [
                "5.1. Phan cong nhan vien vao du an",
                "5.2. Xoa nhan vien khoi du an",
                "5.3. Hien thi du an cua 1 nhan vien",
                "5.4. Top 10 nhan vien tham gia nhieu du an nhat",
                "5.5. Top 10 nhan vien tham gia it du an nhat",
                "5.6. Danh sach thanh vien cua 1 du an va chuc vu",
            ],
        )

        if lua_chon == 1:
            ma_nhan_vien = nhap_chuoi("Nhap ID nhan vien: ")
            cong_ty.phan_cong_du_an(ma_nhan_vien, nhap_chuoi("Nhap ten du an: "))
            in_thong_bao("Phan cong du an thanh cong.")
        elif lua_chon == 2:
            ma_nhan_vien = nhap_chuoi("Nhap ID nhan vien: ")
            cong_ty.xoa_khoi_du_an(ma_nhan_vien, nhap_chuoi("Nhap ten du an can xoa: "))
            in_thong_bao("Da xoa nhan vien khoi du an.")
        elif lua_chon == 3:
            ma_nhan_vien = nhap_chuoi("Nhap ID nhan vien: ")
            in_danh_sach_du_an(cong_ty.lay_du_an_cua_nhan_vien(ma_nhan_vien))
        elif lua_chon == 4:
            in_bang_xep_hang_du_an(cong_ty.lay_top_nhieu_du_an_nhat())
        elif lua_chon == 5:
            in_bang_xep_hang_du_an(cong_ty.lay_top_it_du_an_nhat())
        else:
            ten_du_an = nhap_chuoi("Nhap ten du an can xem: ")
            in_thanh_vien_du_an(ten_du_an, cong_ty.lay_thanh_vien_theo_du_an(ten_du_an))
    except LoiKhongTimThayNhanVien as loi:
        in_thong_bao(str(loi))
    except LoiPhanCongDuAn as loi:
        in_thong_bao(str(loi))
    except IndexError:
        in_thong_bao("Chua co du lieu.")


def menu_danh_gia_hieu_suat(cong_ty: CongTy) -> None:
    """Cap nhat va xem danh sach nhan vien theo muc hieu suat."""
    try:
        cong_ty.kiem_tra_co_du_lieu()
        lua_chon = chon_menu_con(
            "DANH GIA HIEU SUAT",
            [
                "6.1. Cap nhat diem hieu suat cho nhan vien",
                "6.2. Hien thi nhan vien xuat sac (diem > 8)",
                "6.3. Hien thi nhan vien can cai thien (diem < 5)",
            ],
        )

        if lua_chon == 1:
            ma_nhan_vien = nhap_chuoi("Nhap ID nhan vien: ")
            # Validator nay dong vai tro chan diem nam ngoai khoang 0-10.
            diem_so = nhap_so_thuc("Nhap diem hieu suat (0-10): ", min_value=0, max_value=10)
            cong_ty.cap_nhat_hieu_suat(ma_nhan_vien, diem_so)
            in_thong_bao("Cap nhat diem hieu suat thanh cong.")
        elif lua_chon == 2:
            in_bang_nhan_vien(cong_ty.lay_nhan_vien_xuat_sac())
        else:
            in_bang_nhan_vien(cong_ty.lay_nhan_vien_can_cai_thien())
    except LoiKhongTimThayNhanVien as loi:
        in_thong_bao(str(loi))
    except ValueError as loi:
        in_thong_bao(str(loi))
    except IndexError:
        in_thong_bao("Chua co du lieu.")


def menu_quan_ly_nhan_su(cong_ty: CongTy) -> None:
    """Xu ly xoa nhan vien, tang luong va thang chuc."""
    try:
        cong_ty.kiem_tra_co_du_lieu()
        lua_chon = chon_menu_con(
            "QUAN LY NHAN SU",
            [
                "7.1. Xoa nhan vien (nghi viec)",
                "7.2. Tang luong co ban cho nhan vien",
                "7.3. Thang chuc (ThucTapSinh -> LapTrinhVien -> QuanLy)",
                "7.4. Cat giam nhan su",
            ],
        )

        if lua_chon == 1:
            ma_nhan_vien = nhap_chuoi("Nhap ID nhan vien: ")
            cong_ty.xoa_nhan_vien(ma_nhan_vien)
            in_thong_bao("Da xoa nhan vien khoi danh sach.")
        elif lua_chon == 2:
            ma_nhan_vien = nhap_chuoi("Nhap ID nhan vien: ")
            so_tien = nhap_so_thuc("Nhap so tien tang them: ", min_value=0.01)
            cong_ty.tang_luong_co_ban(ma_nhan_vien, so_tien)
            in_thong_bao("Tang luong co ban thanh cong.")
        elif lua_chon == 3:
            ma_nhan_vien = nhap_chuoi("Nhap ID nhan vien: ")
            nhan_vien_moi = cong_ty.thang_chuc_nhan_vien(ma_nhan_vien)
            in_thong_bao(f"Thang chuc thanh cong. Vai tro moi: {nhan_vien_moi.loai_nhan_vien}")
        else:
            so_luong = nhap_so_nguyen("Nhap so luong nhan vien can cat giam: ", 1)
            danh_sach_cat_giam = cong_ty.cat_giam_nhan_su(so_luong)
            in_thong_bao("Da cat giam cac nhan vien sau:")
            in_bang_nhan_vien(danh_sach_cat_giam)
    except LoiKhongTimThayNhanVien as loi:
        in_thong_bao(str(loi))
    except ValueError as loi:
        in_thong_bao(str(loi))
    except IndexError:
        in_thong_bao("Chua co du lieu.")


def menu_thong_ke_bao_cao(cong_ty: CongTy) -> None:
    """In cac thong ke tong hop cua cong ty."""
    lua_chon = chon_menu_con(
        "THONG KE BAO CAO",
        [
            "8.1. So luong nhan vien theo loai",
            "8.2. Tong luong theo phong ban",
            "8.3. So du an trung binh tren moi nhan vien",
        ],
    )

    if lua_chon == 1:
        ket_qua = cong_ty.dem_theo_loai()
        for loai_nhan_vien, tong_so in ket_qua.items():
            print(f"{loai_nhan_vien}: {tong_so}")
    elif lua_chon == 2:
        ket_qua = cong_ty.thong_ke_luong_tung_phong()
        # Neu dict rong, chuong trinh se chuyen sang thong bao "Chua co du lieu".
        if not ket_qua:
            raise IndexError
        for phong_ban, tong_luong in ket_qua.items():
            print(f"{phong_ban}: {dinh_dang_tien(tong_luong)}")
    else:
        print(f"So du an trung binh: {cong_ty.trung_binh_du_an():.2f}")


def in_menu_chinh() -> None:
    """In menu chinh cua chuong trinh de nguoi dung chon thao tac."""
    in_tieu_de("HE THONG QUAN LY NHAN VIEN CONG TY ABC")
    print("1. Them nhan vien moi")
    print("2. Hien thi danh sach nhan vien")
    print("3. Tim kiem nhan vien")
    print("4. Quan ly luong")
    print("5. Quan ly du an")
    print("6. Danh gia hieu suat")
    print("7. Quan ly nhan su")
    print("8. Thong ke bao cao")
    print("9. Thoat")


def chuong_trinh_chinh() -> None:
    """Ham dieu khien vong lap menu chinh cua ung dung."""
    cong_ty = CongTy("Cong ty ABC")
    tao_du_lieu_mau(cong_ty)

    while True:
        try:
            in_menu_chinh()
            lua_chon = nhap_so_nguyen("Nhap lua chon cua ban: ", 1, 9)

            if lua_chon == 1:
                menu_them_nhan_vien(cong_ty)
            elif lua_chon == 2:
                menu_hien_thi_nhan_vien(cong_ty)
            elif lua_chon == 3:
                menu_tim_kiem_nhan_vien(cong_ty)
            elif lua_chon == 4:
                menu_quan_ly_luong(cong_ty)
            elif lua_chon == 5:
                menu_quan_ly_du_an(cong_ty)
            elif lua_chon == 6:
                menu_danh_gia_hieu_suat(cong_ty)
            elif lua_chon == 7:
                menu_quan_ly_nhan_su(cong_ty)
            elif lua_chon == 8:
                try:
                    menu_thong_ke_bao_cao(cong_ty)
                except IndexError:
                    in_thong_bao("Chua co du lieu.")
            else:
                in_thong_bao("Cam on ban da su dung chuong trinh.")
                break

            tam_dung()
        except ValueError:
            in_thong_bao("Du lieu nhap khong hop le. Vui long thu lai.")


if __name__ == "__main__":
    chuong_trinh_chinh()
