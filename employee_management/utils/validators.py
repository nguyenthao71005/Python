"""Ham kiem tra va nhap lieu an toan."""

import re


def kiem_tra_email(email: str) -> str:
    """Kiem tra email co dung dinh dang co ban hay khong."""
    if "@" not in email or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise ValueError("Email khong dung dinh dang.")
    return email


def nhap_chuoi(prompt: str, cho_phep_rong: bool = False) -> str:
    """Nhap chuoi, co the bat buoc hoac cho phep rong tuy truong hop."""
    while True:
        value = input(prompt).strip()
        if value or cho_phep_rong:
            return value
        print("Gia tri khong duoc de trong. Vui long nhap lai.")


def nhap_so_nguyen(prompt: str, min_value: int | None = None, max_value: int | None = None) -> int:
    """Nhap so nguyen va kiem tra gioi han neu co."""
    while True:
        try:
            value = int(input(prompt).strip())
            if min_value is not None and value < min_value:
                raise ValueError
            if max_value is not None and value > max_value:
                raise ValueError
            return value
        except ValueError:
            print("Gia tri khong hop le. Vui long nhap so nguyen dung yeu cau.")


def nhap_so_thuc(prompt: str, min_value: float | None = None, max_value: float | None = None) -> float:
    """Nhap so thuc va kiem tra gioi han neu co."""
    while True:
        try:
            value = float(input(prompt).strip())
            if min_value is not None and value < min_value:
                raise ValueError
            if max_value is not None and value > max_value:
                raise ValueError
            return value
        except ValueError:
            print("Gia tri khong hop le. Vui long nhap so dung yeu cau.")


def nhap_email(prompt: str) -> str:
    """Nhap email va kiem tra den khi hop le."""
    while True:
        try:
            return kiem_tra_email(input(prompt).strip())
        except ValueError as error:
            print(error)
