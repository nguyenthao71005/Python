"""Package exceptions."""

from exceptions.employee_exceptions import (
    DuplicateEmployeeError,
    EmployeeException,
    EmployeeNotFoundError,
    InvalidAgeError,
    InvalidSalaryError,
    LoiKhongTimThayNhanVien,
    LoiLuongKhongHopLe,
    LoiNhanVien,
    LoiPhanCongDuAn,
    LoiTrungMaNhanVien,
    LoiTuoiKhongHopLe,
    ProjectAllocationError,
)

__all__ = [
    "LoiNhanVien",
    "LoiKhongTimThayNhanVien",
    "LoiLuongKhongHopLe",
    "LoiTuoiKhongHopLe",
    "LoiPhanCongDuAn",
    "LoiTrungMaNhanVien",
    "EmployeeException",
    "EmployeeNotFoundError",
    "InvalidSalaryError",
    "InvalidAgeError",
    "ProjectAllocationError",
    "DuplicateEmployeeError",
]
