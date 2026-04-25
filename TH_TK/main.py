"""Ứng dụng PyQt6 hiển thị các biểu đồ thống kê doanh thu từ file CSV."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
try:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
except ImportError:  # pragma: no cover
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QFrame, QLabel, QMainWindow, QMessageBox, QVBoxLayout


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "sales-data-sample.csv"
UI_FILE = BASE_DIR / "statistics_dashboard.ui"

MAU_CHU_DAM = "#102a43"
MAU_LUOI = "#d9e2ec"
MAU_NEN_TRUC = "#ffffff"
MAU_DUONG = "#2563eb"
MAU_XANH = "#16a34a"
MAU_CAM = "#f59e0b"
MAU_DO = "#dc2626"
MAU_TIM = "#7c3aed"
MAU_XANH_NGOC = "#0f766e"
MAU_NAU = "#8b5e34"


def doc_du_lieu(file_path: Path) -> pd.DataFrame:
    """Đọc file CSV và chuẩn hóa các cột phục vụ thống kê."""
    du_lieu = pd.read_csv(file_path)
    du_lieu["OrderDate"] = pd.to_datetime(du_lieu["OrderDate"], errors="coerce")
    du_lieu["Sales"] = pd.to_numeric(du_lieu["Sales"], errors="coerce")
    du_lieu["Profit"] = pd.to_numeric(du_lieu["Profit"], errors="coerce")
    du_lieu["Discount"] = pd.to_numeric(du_lieu["Discount"], errors="coerce")
    du_lieu["Quantity"] = pd.to_numeric(du_lieu["Quantity"], errors="coerce")
    du_lieu["DaystoShipActual"] = pd.to_numeric(du_lieu["DaystoShipActual"], errors="coerce")
    du_lieu["DaystoShipScheduled"] = pd.to_numeric(du_lieu["DaystoShipScheduled"], errors="coerce")
    du_lieu = du_lieu.dropna(subset=["OrderDate", "Sales"]).copy()

    du_lieu["Nam"] = du_lieu["OrderDate"].dt.year
    du_lieu["Thang"] = du_lieu["OrderDate"].dt.strftime("%Y-%m")
    du_lieu["Quy"] = (
        du_lieu["OrderDate"].dt.year.astype(str)
        + "-Q"
        + du_lieu["OrderDate"].dt.quarter.astype(str)
    )
    du_lieu["NhanCoLai"] = du_lieu["Profit"].fillna(0) > 0
    return du_lieu


class BieuDoCanvas(FigureCanvasQTAgg):
    """Canvas matplotlib dùng để nhúng biểu đồ vào giao diện PyQt6."""

    def __init__(self) -> None:
        self.figure = Figure(figsize=(8, 5), tight_layout=True)
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setStyleSheet("background: transparent;")


class CuaSoThongKe(QMainWindow):
    """Cửa sổ chính của chương trình thống kê doanh thu."""

    def __init__(self) -> None:
        super().__init__()
        uic.loadUi(UI_FILE, self)

        self.du_lieu = doc_du_lieu(DATA_FILE)
        self.canvas_theo_khung: dict[str, BieuDoCanvas] = {}
        self.placeholder_theo_khung: dict[str, str] = {
            "chartMonthFrame": "chartMonthPlaceholder",
            "chartYearFrame": "chartYearPlaceholder",
            "chartQuarterFrame": "chartQuarterPlaceholder",
            "chartCategoryFrame": "chartCategoryPlaceholder",
            "chartLocationFrame": "chartLocationPlaceholder",
            "chartProfitMonthFrame": "chartProfitMonthPlaceholder",
            "chartTopProductsFrame": "chartTopProductsPlaceholder",
            "chartSegmentFrame": "chartSegmentPlaceholder",
            "chartRegionProfitFrame": "chartRegionProfitPlaceholder",
            "chartDiscountProfitFrame": "chartDiscountProfitPlaceholder",
            "chartShippingStatusFrame": "chartShippingStatusPlaceholder",
        }

        self._khoi_tao_canvas()
        self._cap_nhat_thong_tin_tong_quan()
        self._ve_tat_ca_bieu_do()

    def _khoi_tao_canvas(self) -> None:
        """Tạo canvas biểu đồ cho từng khung trong giao diện."""
        for ten_khung, ten_placeholder in self.placeholder_theo_khung.items():
            khung = self.findChild(QFrame, ten_khung)
            placeholder = self.findChild(QLabel, ten_placeholder)

            if khung is None:
                continue

            layout = khung.layout()
            if layout is None:
                layout = QVBoxLayout(khung)
                layout.setContentsMargins(0, 0, 0, 0)

            canvas = BieuDoCanvas()
            self.canvas_theo_khung[ten_khung] = canvas
            canvas.figure.patch.set_facecolor("#ffffff")
            layout.addWidget(canvas)

            if placeholder is not None:
                placeholder.hide()

    def _cap_nhat_thong_tin_tong_quan(self) -> None:
        """Hiển thị mô tả ngắn về tập dữ liệu trên giao diện."""
        tong_doanh_thu = self.du_lieu["Sales"].sum()
        ngay_bat_dau = self.du_lieu["OrderDate"].min().date()
        ngay_ket_thuc = self.du_lieu["OrderDate"].max().date()
        self.menuHintLabel.setText(
            f"Dữ liệu gồm {len(self.du_lieu):,} dòng, từ {ngay_bat_dau} đến {ngay_ket_thuc}.\n"
            f"Tổng doanh thu: {tong_doanh_thu:,.2f}."
        )

    def _dinh_dang_truc(
        self,
        ax,
        tieu_de: str,
        nhan_x: str,
        nhan_y: str,
        xoay_nhan_x: int = 0,
        luoi_truc: str = "y",
    ) -> None:
        """Áp dụng giao diện thống nhất cho một biểu đồ."""
        ax.set_title(tieu_de, fontsize=15, fontweight="bold", color=MAU_CHU_DAM, pad=14)
        ax.set_xlabel(nhan_x, fontsize=11, color="#486581", labelpad=10)
        ax.set_ylabel(nhan_y, fontsize=11, color="#486581", labelpad=10)
        ax.set_facecolor(MAU_NEN_TRUC)
        for canh in ("top", "right"):
            ax.spines[canh].set_visible(False)
        ax.spines["left"].set_color("#bcccdc")
        ax.spines["bottom"].set_color("#bcccdc")
        ax.tick_params(axis="x", colors="#334e68", rotation=xoay_nhan_x)
        ax.tick_params(axis="y", colors="#334e68")
        ax.grid(True, axis=luoi_truc, color=MAU_LUOI, linestyle="--", linewidth=0.8, alpha=0.8)

    def _dinh_dang_hinh(self, canvas: BieuDoCanvas) -> None:
        """Thiết lập nền và khoảng đệm cho figure."""
        canvas.figure.set_facecolor("#ffffff")
        canvas.figure.subplots_adjust(left=0.08, right=0.98, top=0.90, bottom=0.18)

    def _ve_tat_ca_bieu_do(self) -> None:
        """Vẽ toàn bộ biểu đồ vào các trang tương ứng."""
        self._ve_doanh_thu_theo_thang()
        self._ve_doanh_thu_theo_nam()
        self._ve_doanh_thu_theo_quy()
        self._ve_doanh_thu_theo_loai_mat_hang()
        self._ve_doanh_thu_theo_vi_tri_dia_ly()
        self._ve_loi_nhuan_theo_thang()
        self._ve_top_san_pham_theo_doanh_thu()
        self._ve_doanh_thu_theo_phan_khuc()
        self._ve_doanh_thu_loi_nhuan_theo_khu_vuc()
        self._ve_anh_huong_giam_gia_den_loi_nhuan()
        self._ve_thong_ke_trang_thai_giao_hang()

    def _lay_canvas(self, ten_khung: str) -> BieuDoCanvas:
        """Lấy canvas theo tên khung."""
        return self.canvas_theo_khung[ten_khung]

    def _ve_doanh_thu_theo_thang(self) -> None:
        """Vẽ biểu đồ doanh thu theo tháng."""
        doanh_thu = self.du_lieu.groupby("Thang", as_index=False)["Sales"].sum()
        canvas = self._lay_canvas("chartMonthFrame")
        ax = canvas.axes
        ax.clear()
        vi_tri_x = list(range(len(doanh_thu)))
        ax.plot(vi_tri_x, doanh_thu["Sales"], marker="o", markersize=6, color=MAU_DUONG, linewidth=2.8)
        ax.fill_between(vi_tri_x, doanh_thu["Sales"], color=MAU_DUONG, alpha=0.10)
        ax.set_xticks(vi_tri_x)
        ax.set_xticklabels(doanh_thu["Thang"])
        self._dinh_dang_truc(ax, "Doanh thu theo tháng", "Tháng", "Doanh thu", xoay_nhan_x=45, luoi_truc="y")
        self._dinh_dang_hinh(canvas)
        canvas.draw()

    def _ve_doanh_thu_theo_nam(self) -> None:
        """Vẽ biểu đồ doanh thu theo năm."""
        doanh_thu = self.du_lieu.groupby("Nam", as_index=False)["Sales"].sum()
        canvas = self._lay_canvas("chartYearFrame")
        ax = canvas.axes
        ax.clear()
        ax.bar(doanh_thu["Nam"].astype(str), doanh_thu["Sales"], color="#22c55e", width=0.58)
        self._dinh_dang_truc(ax, "Doanh thu theo năm", "Năm", "Doanh thu", luoi_truc="y")
        self._dinh_dang_hinh(canvas)
        canvas.draw()

    def _ve_doanh_thu_theo_quy(self) -> None:
        """Vẽ biểu đồ doanh thu theo quý."""
        doanh_thu = self.du_lieu.groupby("Quy", as_index=False)["Sales"].sum()
        canvas = self._lay_canvas("chartQuarterFrame")
        ax = canvas.axes
        ax.clear()
        ax.bar(doanh_thu["Quy"], doanh_thu["Sales"], color=MAU_CAM, width=0.58)
        self._dinh_dang_truc(ax, "Doanh thu theo quý", "Quý", "Doanh thu", xoay_nhan_x=20, luoi_truc="y")
        self._dinh_dang_hinh(canvas)
        canvas.draw()

    def _ve_doanh_thu_theo_loai_mat_hang(self) -> None:
        """Vẽ biểu đồ doanh thu theo loại mặt hàng."""
        doanh_thu = self.du_lieu.groupby("Category")["Sales"].sum().sort_values(ascending=False)
        canvas = self._lay_canvas("chartCategoryFrame")
        ax = canvas.axes
        ax.clear()
        ax.pie(
            doanh_thu.values,
            labels=doanh_thu.index,
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.8,
            wedgeprops={"linewidth": 2, "edgecolor": "white"},
            textprops={"color": MAU_CHU_DAM, "fontsize": 10},
            colors=["#2563eb", "#14b8a6", "#f59e0b", "#7c3aed", "#ef4444"],
        )
        ax.set_title("Doanh thu các loại mặt hàng", fontsize=15, fontweight="bold", color=MAU_CHU_DAM, pad=14)
        canvas.figure.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.08)
        canvas.draw()

    def _ve_doanh_thu_theo_vi_tri_dia_ly(self) -> None:
        """Vẽ biểu đồ doanh thu theo vị trí địa lý."""
        cot_dia_ly = "State" if "State" in self.du_lieu.columns else "Country"
        doanh_thu = (
            self.du_lieu.groupby(cot_dia_ly)["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )
        canvas = self._lay_canvas("chartLocationFrame")
        ax = canvas.axes
        ax.clear()
        ax.barh(doanh_thu.index, doanh_thu.values, color=MAU_TIM, height=0.65)
        ax.invert_yaxis()
        self._dinh_dang_truc(ax, f"Top 10 doanh thu theo vị trí địa lý ({cot_dia_ly})", "Doanh thu", cot_dia_ly, luoi_truc="x")
        self._dinh_dang_hinh(canvas)
        canvas.draw()

    def _ve_loi_nhuan_theo_thang(self) -> None:
        """Vẽ biểu đồ lợi nhuận theo tháng."""
        du_lieu = self.du_lieu.dropna(subset=["Profit"])
        loi_nhuan = du_lieu.groupby("Thang", as_index=False)["Profit"].sum()
        canvas = self._lay_canvas("chartProfitMonthFrame")
        ax = canvas.axes
        ax.clear()
        mau = ["#2ca02c" if gia_tri >= 0 else "#d62728" for gia_tri in loi_nhuan["Profit"]]
        ax.bar(loi_nhuan["Thang"], loi_nhuan["Profit"], color=mau, width=0.62)
        ax.axhline(0, color="black", linewidth=1)
        self._dinh_dang_truc(ax, "Lợi nhuận theo tháng", "Tháng", "Lợi nhuận", xoay_nhan_x=45, luoi_truc="y")
        self._dinh_dang_hinh(canvas)
        canvas.draw()

    def _ve_top_san_pham_theo_doanh_thu(self) -> None:
        """Vẽ biểu đồ top 10 sản phẩm có doanh thu cao nhất."""
        doanh_thu = (
            self.du_lieu.groupby("ProductName")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .sort_values(ascending=True)
        )
        canvas = self._lay_canvas("chartTopProductsFrame")
        ax = canvas.axes
        ax.clear()
        ax.barh(doanh_thu.index, doanh_thu.values, color=MAU_XANH_NGOC, height=0.66)
        self._dinh_dang_truc(ax, "Top 10 sản phẩm theo doanh thu", "Doanh thu", "Sản phẩm", luoi_truc="x")
        self._dinh_dang_hinh(canvas)
        canvas.draw()

    def _ve_doanh_thu_theo_phan_khuc(self) -> None:
        """Vẽ biểu đồ doanh thu theo phân khúc khách hàng."""
        doanh_thu = self.du_lieu.groupby("Segment")["Sales"].sum().sort_values(ascending=False)
        canvas = self._lay_canvas("chartSegmentFrame")
        ax = canvas.axes
        ax.clear()
        mau_sac = plt.cm.Set2(range(len(doanh_thu)))
        ax.bar(doanh_thu.index, doanh_thu.values, color=mau_sac, width=0.58)
        self._dinh_dang_truc(ax, "Doanh thu theo phân khúc khách hàng", "Phân khúc", "Doanh thu", luoi_truc="y")
        self._dinh_dang_hinh(canvas)
        canvas.draw()

    def _ve_doanh_thu_loi_nhuan_theo_khu_vuc(self) -> None:
        """Vẽ biểu đồ so sánh doanh thu và lợi nhuận theo khu vực."""
        khu_vuc = (
            self.du_lieu.groupby("Region")[["Sales", "Profit"]]
            .sum()
            .sort_values("Sales", ascending=False)
        )
        canvas = self._lay_canvas("chartRegionProfitFrame")
        ax = canvas.axes
        ax.clear()
        vi_tri = range(len(khu_vuc))
        do_rong = 0.38
        ax.bar([i - do_rong / 2 for i in vi_tri], khu_vuc["Sales"], width=do_rong, label="Doanh thu", color=MAU_DUONG)
        ax.bar([i + do_rong / 2 for i in vi_tri], khu_vuc["Profit"], width=do_rong, label="Lợi nhuận", color=MAU_CAM)
        ax.set_xticks(list(vi_tri))
        ax.set_xticklabels(khu_vuc.index)
        self._dinh_dang_truc(ax, "Doanh thu và lợi nhuận theo khu vực", "Khu vực", "Giá trị", luoi_truc="y")
        ax.legend(frameon=False)
        self._dinh_dang_hinh(canvas)
        canvas.draw()

    def _ve_anh_huong_giam_gia_den_loi_nhuan(self) -> None:
        """Vẽ biểu đồ thể hiện lợi nhuận trung bình theo các mức giảm giá."""
        du_lieu = self.du_lieu.dropna(subset=["Discount", "Profit"]).copy()
        khoang = [-0.01, 0.0, 0.1, 0.2, 0.3, 0.5, 0.8]
        nhan = ["0%", "0-10%", "10-20%", "20-30%", "30-50%", "50-80%"]
        du_lieu["NhomGiamGia"] = pd.cut(du_lieu["Discount"], bins=khoang, labels=nhan)
        thong_ke = du_lieu.groupby("NhomGiamGia", observed=False)["Profit"].mean().fillna(0)
        canvas = self._lay_canvas("chartDiscountProfitFrame")
        ax = canvas.axes
        ax.clear()
        mau = ["#2ca02c" if gia_tri >= 0 else "#d62728" for gia_tri in thong_ke.values]
        ax.bar(thong_ke.index.astype(str), thong_ke.values, color=mau, width=0.62)
        ax.axhline(0, color="black", linewidth=1)
        self._dinh_dang_truc(ax, "Ảnh hưởng giảm giá đến lợi nhuận trung bình", "Nhóm giảm giá", "Lợi nhuận trung bình", luoi_truc="y")
        self._dinh_dang_hinh(canvas)
        canvas.draw()

    def _ve_thong_ke_trang_thai_giao_hang(self) -> None:
        """Vẽ biểu đồ trạng thái giao hàng kết hợp thời gian giao trung bình."""
        thong_ke = (
            self.du_lieu.groupby("ShipStatus")
            .agg(SoDon=("OrderID", "count"), NgayGiaoTB=("DaystoShipActual", "mean"))
            .sort_values("SoDon", ascending=False)
        )
        canvas = self._lay_canvas("chartShippingStatusFrame")
        fig = canvas.figure
        fig.clear()
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        ax1.bar(thong_ke.index, thong_ke["SoDon"], color=MAU_NAU, width=0.58)
        self._dinh_dang_truc(ax1, "Số đơn theo trạng thái giao hàng", "Trạng thái", "Số đơn", xoay_nhan_x=20, luoi_truc="y")

        ax2.bar(thong_ke.index, thong_ke["NgayGiaoTB"], color="#84cc16", width=0.58)
        self._dinh_dang_truc(ax2, "Số ngày giao trung bình", "Trạng thái", "Số ngày", xoay_nhan_x=20, luoi_truc="y")

        fig.patch.set_facecolor("#ffffff")
        fig.subplots_adjust(left=0.06, right=0.98, top=0.88, bottom=0.20, wspace=0.28)
        canvas.draw()


def main() -> None:
    """Khởi chạy ứng dụng PyQt6."""
    app = QApplication(sys.argv)

    try:
        cua_so = CuaSoThongKe()
    except Exception as loi:  # pragma: no cover
        QMessageBox.critical(None, "Lỗi", f"Không thể khởi tạo ứng dụng:\n{loi}")
        raise

    cua_so.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
