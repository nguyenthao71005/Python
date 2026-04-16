from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.uic import loadUi
from database import connect_db
from pathlib import Path
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = Path(__file__).resolve().parent / "nhansu.ui"
        loadUi(str(ui_path), self)

        self.cbGioiTinh.clear()
        self.cbGioiTinh.addItems(["Nam", "Nu"])

        self.tableNhanSu.setColumnCount(5)
        self.tableNhanSu.setHorizontalHeaderLabels(
            ["So CCCD", "Ho ten", "Ngay sinh", "Gioi tinh", "Dia chi thuong tru"]
        )

        self.btnThem.clicked.connect(self.them)
        self.btnSua.clicked.connect(self.sua)
        self.btnXoa.clicked.connect(self.xoa)
        self.btnTim.clicked.connect(self.tim)
        self.tableNhanSu.cellClicked.connect(self.hien_len_form)

        self.load_data()

    def lay_du_lieu_form(self):
        socccd = self.txtCCCD.toPlainText().strip()
        hoten = self.txtHoTen.toPlainText().strip()
        ngaysinh = self.dateNgaySinh.date().toString("yyyy-MM-dd")
        gioitinh = self.cbGioiTinh.currentText().strip()
        dctt = self.txtDiaChi.toPlainText().strip()

        if not socccd or not hoten or not dctt:
            raise ValueError("Vui long nhap day du So CCCD, Ho ten va Dia chi thuong tru.")

        if not socccd.isdigit() or len(socccd) != 12:
            raise ValueError("So CCCD phai gom dung 12 chu so.")

        return socccd, hoten, ngaysinh, gioitinh, dctt

    def do_du_lieu_len_bang(self, data):
        self.tableNhanSu.setRowCount(0)

        for row_idx, row_data in enumerate(data):
            self.tableNhanSu.insertRow(row_idx)
            for col_idx, col_data in enumerate(row_data):
                self.tableNhanSu.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def load_data(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT SOCCCD, HOTEN, NGAYSINH, GIOITINH, DCTT
                FROM NHANSU
                ORDER BY HOTEN, SOCCCD
                """
            )
            data = cursor.fetchall()
            conn.close()

            self.do_du_lieu_len_bang(data)
        except Exception as e:
            QMessageBox.warning(self, "Loi load", str(e))

    def them(self):
        try:
            values = self.lay_du_lieu_form()

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM NHANSU WHERE SOCCCD = ?", (values[0],))

            if cursor.fetchone():
                conn.close()
                QMessageBox.warning(self, "Loi", "So CCCD da ton tai.")
                return

            cursor.execute(
                """
                INSERT INTO NHANSU (SOCCCD, HOTEN, NGAYSINH, GIOITINH, DCTT)
                VALUES (?, ?, ?, ?, ?)
                """,
                values,
            )
            conn.commit()
            conn.close()

            QMessageBox.information(self, "OK", "Them moi nhan su thanh cong.")
            self.load_data()
        except Exception as e:
            QMessageBox.warning(self, "Loi", str(e))

    def sua(self):
        try:
            socccd, hoten, ngaysinh, gioitinh, dctt = self.lay_du_lieu_form()

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE NHANSU
                SET HOTEN = ?, NGAYSINH = ?, GIOITINH = ?, DCTT = ?
                WHERE SOCCCD = ?
                """,
                (hoten, ngaysinh, gioitinh, dctt, socccd),
            )

            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Loi", "Khong tim thay nhan su theo So CCCD.")
            else:
                QMessageBox.information(self, "OK", "Cap nhat thong tin nhan su thanh cong.")

            conn.commit()
            conn.close()
            self.load_data()
        except Exception as e:
            QMessageBox.warning(self, "Loi", str(e))

    def xoa(self):
        try:
            socccd = self.txtCCCD.toPlainText().strip()
            if not socccd:
                QMessageBox.warning(self, "Loi", "Vui long nhap So CCCD can xoa.")
                return

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM NHANSU WHERE SOCCCD = ?", (socccd,))

            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Loi", "Khong tim thay nhan su theo So CCCD.")
            else:
                QMessageBox.information(self, "OK", "Xoa nhan su thanh cong.")

            conn.commit()
            conn.close()
            self.load_data()
        except Exception as e:
            QMessageBox.warning(self, "Loi", str(e))

    def tim(self):
        try:
            keyword = self.txtTim.toPlainText().strip()

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT SOCCCD, HOTEN, NGAYSINH, GIOITINH, DCTT
                FROM NHANSU
                WHERE SOCCCD LIKE ? OR HOTEN LIKE ? OR DCTT LIKE ?
                ORDER BY HOTEN, SOCCCD
                """,
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
            )
            data = cursor.fetchall()
            conn.close()

            self.do_du_lieu_len_bang(data)
        except Exception as e:
            QMessageBox.warning(self, "Loi tim kiem", str(e))

    def hien_len_form(self, row, column):
        del column

        self.txtCCCD.setPlainText(self.tableNhanSu.item(row, 0).text())
        self.txtHoTen.setPlainText(self.tableNhanSu.item(row, 1).text())

        date_str = self.tableNhanSu.item(row, 2).text()
        self.dateNgaySinh.setDate(QDate.fromString(date_str, "yyyy-MM-dd"))

        self.cbGioiTinh.setCurrentText(self.tableNhanSu.item(row, 3).text())
        self.txtDiaChi.setPlainText(self.tableNhanSu.item(row, 4).text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
