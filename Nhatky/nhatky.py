from __future__ import annotations

import json
import random
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any

from PyQt6 import uic
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
)


BASE_DIR = Path(__file__).resolve().parent
UI_FILE = BASE_DIR / "nhatky.ui"
DATA_FILE = BASE_DIR / "nhatky_data.json"


def quarter_for_month(month: int) -> int:
    return ((month - 1) // 3) + 1


def parse_entry_date(entry: dict[str, Any]) -> date:
    return date.fromisoformat(entry["date"])


def count_words(text: str) -> int:
    return len([word for word in text.split() if word.strip()])


class DiaryWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi(str(UI_FILE), self)

        self.entries: list[dict[str, Any]] = []
        self.current_entry_id: str | None = None

        today = QDate.currentDate()
        self.dateEditEntry.setDate(today)
        self.spinRecallYear.setValue(today.year())
        self.spinRecallMonth.setValue(today.month())
        self.spinRecallYear.setMaximum(today.year())

        self.setup_tables()
        self.connect_signals()
        self.load_entries()
        self.refresh_all()

    def setup_tables(self) -> None:
        self.tableQuarterStats.setColumnCount(4)
        self.tableQuarterStats.setHorizontalHeaderLabels(
            ["Quý", "Số bài", "Số từ", "Tâm trạng phổ biến"]
        )
        self.tableQuarterStats.setRowCount(4)

        self.tableMonthStats.setColumnCount(3)
        self.tableMonthStats.setHorizontalHeaderLabels(["Tháng", "Số bài", "Số từ"])
        self.tableMonthStats.setRowCount(12)

        self.tableMoodStats.setColumnCount(2)
        self.tableMoodStats.setHorizontalHeaderLabels(["Tâm trạng", "Số bài"])

        for table in (self.tableQuarterStats, self.tableMonthStats, self.tableMoodStats):
            table.verticalHeader().setVisible(False)
            table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            table.horizontalHeader().setStretchLastSection(True)

    def connect_signals(self) -> None:
        self.btnNewEntry.clicked.connect(lambda _checked=False: self.clear_editor())
        self.btnSaveEntry.clicked.connect(lambda _checked=False: self.save_entry())
        self.btnDeleteEntry.clicked.connect(lambda _checked=False: self.delete_entry())
        self.listEntries.currentItemChanged.connect(self.load_selected_entry)

        self.lineSearch.textChanged.connect(lambda _text: self.refresh_entry_list())
        self.comboFilterYear.currentIndexChanged.connect(
            lambda _index: self.refresh_entry_list()
        )
        self.comboFilterQuarter.currentIndexChanged.connect(
            lambda _index: self.refresh_entry_list()
        )

        self.comboStatsYear.currentIndexChanged.connect(lambda _index: self.refresh_stats())
        self.btnRefreshStats.clicked.connect(lambda _checked=False: self.refresh_stats())

        self.comboRecallMode.currentIndexChanged.connect(
            lambda _index: self.update_recall_controls()
        )
        self.btnFindRecall.clicked.connect(lambda _checked=False: self.find_recall())
        self.btnRandomRecall.clicked.connect(lambda _checked=False: self.random_recall())
        self.listRecall.currentItemChanged.connect(self.show_recall_detail)

    def load_entries(self) -> None:
        if not DATA_FILE.exists():
            self.entries = []
            return

        try:
            raw_data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            QMessageBox.warning(
                self,
                "Lỗi dữ liệu",
                "Không đọc được file dữ liệu nhật ký. Ứng dụng sẽ mở với danh sách trống.",
            )
            self.entries = []
            return

        self.entries = [entry for entry in raw_data if self.is_valid_entry(entry)]

    def save_entries_to_file(self) -> None:
        DATA_FILE.write_text(
            json.dumps(self.entries, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def is_valid_entry(self, entry: Any) -> bool:
        if not isinstance(entry, dict):
            return False
        required_keys = {"id", "date", "title", "mood", "tags", "content"}
        if not required_keys.issubset(entry):
            return False
        try:
            date.fromisoformat(entry["date"])
        except (TypeError, ValueError):
            return False
        return True

    def refresh_all(self) -> None:
        self.refresh_year_filters()
        self.refresh_entry_list()
        self.refresh_stats()
        self.update_recall_controls()
        self.find_recall()

    def refresh_year_filters(self) -> None:
        years = sorted({parse_entry_date(entry).year for entry in self.entries}, reverse=True)
        current_year = QDate.currentDate().year()
        if current_year not in years:
            years.insert(0, current_year)
        min_year = min(years) if years else current_year
        max_year = max(years) if years else current_year

        selected_filter_year = self.comboFilterYear.currentText()
        selected_stats_year = self.comboStatsYear.currentText()
        selected_recall_year = self.spinRecallYear.value()

        self.comboFilterYear.blockSignals(True)
        self.comboFilterYear.clear()
        self.comboFilterYear.addItem("Tất cả năm")
        for year in years:
            self.comboFilterYear.addItem(str(year))
        index = self.comboFilterYear.findText(selected_filter_year)
        self.comboFilterYear.setCurrentIndex(index if index >= 0 else 0)
        self.comboFilterYear.blockSignals(False)

        self.comboStatsYear.blockSignals(True)
        self.comboStatsYear.clear()
        for year in years:
            self.comboStatsYear.addItem(str(year))
        stats_index = self.comboStatsYear.findText(selected_stats_year)
        self.comboStatsYear.setCurrentIndex(stats_index if stats_index >= 0 else 0)
        self.comboStatsYear.blockSignals(False)

        self.spinRecallYear.setMinimum(min(1900, min_year))
        self.spinRecallYear.setMaximum(max(current_year, max_year))
        bounded_recall_year = min(
            max(selected_recall_year, self.spinRecallYear.minimum()),
            self.spinRecallYear.maximum(),
        )
        self.spinRecallYear.setValue(bounded_recall_year)

    def refresh_entry_list(self) -> None:
        keyword = self.lineSearch.text().strip().lower()
        year_text = self.comboFilterYear.currentText()
        quarter_index = self.comboFilterQuarter.currentIndex()
        selected_id = self.current_entry_id

        self.listEntries.blockSignals(True)
        self.listEntries.clear()

        for entry in self.filtered_entries(keyword, year_text, quarter_index):
            entry_date = parse_entry_date(entry)
            title = entry["title"] or "Không có tiêu đề"
            item = QListWidgetItem(f"{entry_date.strftime('%d/%m/%Y')} - {title}")
            item.setData(Qt.ItemDataRole.UserRole, entry["id"])
            item.setToolTip(entry.get("content", "")[:300])
            self.listEntries.addItem(item)

            if entry["id"] == selected_id:
                self.listEntries.setCurrentItem(item)

        self.listEntries.blockSignals(False)

    def filtered_entries(
        self,
        keyword: str = "",
        year_text: str = "Tất cả năm",
        quarter_index: int = 0,
    ) -> list[dict[str, Any]]:
        filtered: list[dict[str, Any]] = []

        for entry in self.sorted_entries():
            entry_date = parse_entry_date(entry)
            if year_text != "Tất cả năm" and entry_date.year != int(year_text):
                continue
            if quarter_index > 0 and quarter_for_month(entry_date.month) != quarter_index:
                continue

            searchable = " ".join(
                [
                    entry.get("title", ""),
                    entry.get("mood", ""),
                    entry.get("tags", ""),
                    entry.get("content", ""),
                ]
            ).lower()
            if keyword and keyword not in searchable:
                continue

            filtered.append(entry)

        return filtered

    def sorted_entries(self) -> list[dict[str, Any]]:
        return sorted(
            self.entries,
            key=lambda entry: (entry["date"], entry.get("updated_at", "")),
            reverse=True,
        )

    def load_selected_entry(
        self,
        current: QListWidgetItem | None,
        _previous: QListWidgetItem | None,
    ) -> None:
        if current is None:
            return

        entry = self.find_entry_by_id(current.data(Qt.ItemDataRole.UserRole))
        if entry is None:
            return

        self.current_entry_id = entry["id"]
        entry_date = parse_entry_date(entry)
        self.dateEditEntry.setDate(QDate(entry_date.year, entry_date.month, entry_date.day))
        self.lineTitle.setText(entry.get("title", ""))
        self.comboMood.setCurrentText(entry.get("mood", "Bình thường"))
        self.lineTags.setText(entry.get("tags", ""))
        self.textEditContent.setPlainText(entry.get("content", ""))
        self.statusbar.showMessage("Đang chỉnh sửa bài nhật ký đã chọn.", 3000)

    def save_entry(self) -> None:
        title = self.lineTitle.text().strip()
        content = self.textEditContent.toPlainText().strip()
        tags = self.lineTags.text().strip()

        if not title and not content:
            QMessageBox.warning(
                self,
                "Thiếu nội dung",
                "Hãy nhập tiêu đề hoặc nội dung trước khi lưu nhật ký.",
            )
            return

        now = datetime.now().isoformat(timespec="seconds")
        entry_date = self.dateEditEntry.date().toPyDate().isoformat()

        if self.current_entry_id:
            entry = self.find_entry_by_id(self.current_entry_id)
            if entry is None:
                self.current_entry_id = None
                self.save_entry()
                return

            entry.update(
                {
                    "date": entry_date,
                    "title": title,
                    "mood": self.comboMood.currentText(),
                    "tags": tags,
                    "content": content,
                    "updated_at": now,
                }
            )
            message = "Đã cập nhật bài nhật ký."
        else:
            entry = {
                "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                "date": entry_date,
                "title": title,
                "mood": self.comboMood.currentText(),
                "tags": tags,
                "content": content,
                "created_at": now,
                "updated_at": now,
            }
            self.entries.append(entry)
            self.current_entry_id = entry["id"]
            message = "Đã lưu bài nhật ký mới."

        self.save_entries_to_file()
        self.refresh_all()
        self.statusbar.showMessage(message, 4000)

    def clear_editor(self) -> None:
        self.current_entry_id = None
        self.dateEditEntry.setDate(QDate.currentDate())
        self.lineTitle.clear()
        self.comboMood.setCurrentIndex(0)
        self.lineTags.clear()
        self.textEditContent.clear()
        self.listEntries.clearSelection()
        self.statusbar.showMessage("Sẵn sàng viết bài nhật ký mới.", 3000)

    def delete_entry(self) -> None:
        if not self.current_entry_id:
            QMessageBox.information(
                self,
                "Chưa chọn bài",
                "Hãy chọn một bài nhật ký trong danh sách trước khi xóa.",
            )
            return

        answer = QMessageBox.question(
            self,
            "Xóa nhật ký",
            "Bạn có chắc muốn xóa bài nhật ký đang chọn không?",
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        self.entries = [
            entry for entry in self.entries if entry["id"] != self.current_entry_id
        ]
        self.save_entries_to_file()
        self.clear_editor()
        self.refresh_all()
        self.statusbar.showMessage("Đã xóa bài nhật ký.", 4000)

    def find_entry_by_id(self, entry_id: str | None) -> dict[str, Any] | None:
        if entry_id is None:
            return None
        return next((entry for entry in self.entries if entry["id"] == entry_id), None)

    def refresh_stats(self) -> None:
        today = date.today()
        current_quarter = quarter_for_month(today.month)
        selected_year = self.selected_stats_year()
        entries_in_selected_year = [
            entry for entry in self.entries if parse_entry_date(entry).year == selected_year
        ]

        self.lblTotalEntries.setText(str(len(self.entries)))
        self.lblTotalWords.setText(
            str(sum(count_words(entry.get("content", "")) for entry in self.entries))
        )
        self.lblCurrentYearEntries.setText(
            str(sum(1 for entry in self.entries if parse_entry_date(entry).year == today.year))
        )
        self.lblCurrentQuarterEntries.setText(
            str(
                sum(
                    1
                    for entry in self.entries
                    if parse_entry_date(entry).year == today.year
                    and quarter_for_month(parse_entry_date(entry).month) == current_quarter
                )
            )
        )
        self.lblDaysWritten.setText(
            str(len({entry["date"] for entry in self.entries}))
        )
        self.lblLastWritten.setText(self.last_written_text())
        self.lblMostActiveMonth.setText(self.most_active_month_text())

        self.fill_quarter_stats(selected_year, entries_in_selected_year)
        self.fill_month_stats(selected_year, entries_in_selected_year)
        self.fill_mood_stats(entries_in_selected_year)

    def selected_stats_year(self) -> int:
        text = self.comboStatsYear.currentText()
        return int(text) if text else date.today().year

    def fill_quarter_stats(
        self,
        selected_year: int,
        entries_in_year: list[dict[str, Any]],
    ) -> None:
        by_quarter: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for entry in entries_in_year:
            by_quarter[quarter_for_month(parse_entry_date(entry).month)].append(entry)

        for quarter in range(1, 5):
            entries = by_quarter[quarter]
            mood = self.common_mood(entries)
            words = sum(count_words(entry.get("content", "")) for entry in entries)
            row = quarter - 1
            self.tableQuarterStats.setItem(row, 0, QTableWidgetItem(f"Quý {quarter}/{selected_year}"))
            self.tableQuarterStats.setItem(row, 1, QTableWidgetItem(str(len(entries))))
            self.tableQuarterStats.setItem(row, 2, QTableWidgetItem(str(words)))
            self.tableQuarterStats.setItem(row, 3, QTableWidgetItem(mood))

    def fill_month_stats(
        self,
        selected_year: int,
        entries_in_year: list[dict[str, Any]],
    ) -> None:
        month_counts: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for entry in entries_in_year:
            month_counts[parse_entry_date(entry).month].append(entry)

        for month in range(1, 13):
            entries = month_counts[month]
            words = sum(count_words(entry.get("content", "")) for entry in entries)
            row = month - 1
            self.tableMonthStats.setItem(row, 0, QTableWidgetItem(f"Tháng {month:02d}/{selected_year}"))
            self.tableMonthStats.setItem(row, 1, QTableWidgetItem(str(len(entries))))
            self.tableMonthStats.setItem(row, 2, QTableWidgetItem(str(words)))

    def fill_mood_stats(self, entries_in_year: list[dict[str, Any]]) -> None:
        mood_counts = Counter(entry.get("mood", "Bình thường") for entry in entries_in_year)
        self.tableMoodStats.setRowCount(max(len(mood_counts), 1))

        if not mood_counts:
            self.tableMoodStats.setItem(0, 0, QTableWidgetItem("Chưa có dữ liệu"))
            self.tableMoodStats.setItem(0, 1, QTableWidgetItem("0"))
            return

        for row, (mood, amount) in enumerate(mood_counts.most_common()):
            self.tableMoodStats.setItem(row, 0, QTableWidgetItem(mood))
            self.tableMoodStats.setItem(row, 1, QTableWidgetItem(str(amount)))

    def common_mood(self, entries: list[dict[str, Any]]) -> str:
        if not entries:
            return "Chưa có dữ liệu"
        return Counter(entry.get("mood", "Bình thường") for entry in entries).most_common(1)[0][0]

    def last_written_text(self) -> str:
        if not self.entries:
            return "Chưa có dữ liệu"
        latest = max(parse_entry_date(entry) for entry in self.entries)
        return latest.strftime("%d/%m/%Y")

    def most_active_month_text(self) -> str:
        if not self.entries:
            return "Chưa có dữ liệu"

        month_counter = Counter(
            (parse_entry_date(entry).year, parse_entry_date(entry).month)
            for entry in self.entries
        )
        (year, month), amount = month_counter.most_common(1)[0]
        return f"Tháng {month:02d}/{year}: {amount} bài"

    def update_recall_controls(self) -> None:
        mode = self.comboRecallMode.currentText()
        use_year = mode in {"Theo năm", "Theo quý", "Theo tháng"}
        use_quarter = mode == "Theo quý"
        use_month = mode == "Theo tháng"

        self.spinRecallYear.setEnabled(use_year)
        self.comboRecallQuarter.setEnabled(use_quarter)
        self.spinRecallMonth.setEnabled(use_month)

    def find_recall(self) -> None:
        recall_entries = self.entries_for_recall()
        self.listRecall.blockSignals(True)
        self.listRecall.clear()
        self.textRecallDetail.clear()

        for entry in sorted(recall_entries, key=lambda item: item["date"], reverse=True):
            entry_date = parse_entry_date(entry)
            title = entry["title"] or "Không có tiêu đề"
            item = QListWidgetItem(f"{entry_date.strftime('%d/%m/%Y')} - {title}")
            item.setData(Qt.ItemDataRole.UserRole, entry["id"])
            item.setToolTip(entry.get("content", "")[:300])
            self.listRecall.addItem(item)

        self.listRecall.blockSignals(False)
        if self.listRecall.count() > 0:
            self.listRecall.setCurrentRow(0)
            self.show_recall_detail(self.listRecall.currentItem(), None)
        else:
            self.textRecallDetail.setPlainText("Không có kỷ niệm phù hợp với bộ lọc hiện tại.")

    def entries_for_recall(self) -> list[dict[str, Any]]:
        mode = self.comboRecallMode.currentText()
        today = date.today()

        if mode == "Cùng ngày các năm trước":
            return [
                entry
                for entry in self.entries
                if parse_entry_date(entry).month == today.month
                and parse_entry_date(entry).day == today.day
                and parse_entry_date(entry).year < today.year
            ]

        year = self.spinRecallYear.value()
        quarter = self.comboRecallQuarter.currentIndex() + 1
        month = self.spinRecallMonth.value()
        results = []

        for entry in self.entries:
            entry_date = parse_entry_date(entry)
            if entry_date.year != year:
                continue
            if mode == "Theo quý" and quarter_for_month(entry_date.month) != quarter:
                continue
            if mode == "Theo tháng" and entry_date.month != month:
                continue
            results.append(entry)

        return results

    def random_recall(self) -> None:
        source_entries = self.entries_for_recall() or self.entries
        if not source_entries:
            QMessageBox.information(
                self,
                "Chưa có nhật ký",
                "Hãy viết ít nhất một bài nhật ký trước khi dùng chức năng nhắc lại.",
            )
            return

        entry = random.choice(source_entries)
        self.show_entry_in_recall(entry)
        self.statusbar.showMessage("Đã chọn một kỷ niệm ngẫu nhiên.", 4000)

    def show_recall_detail(
        self,
        current: QListWidgetItem | None,
        _previous: QListWidgetItem | None,
    ) -> None:
        if current is None:
            return
        entry = self.find_entry_by_id(current.data(Qt.ItemDataRole.UserRole))
        if entry:
            self.show_entry_in_recall(entry)

    def show_entry_in_recall(self, entry: dict[str, Any]) -> None:
        entry_date = parse_entry_date(entry)
        detail = "\n".join(
            [
                f"Ngày: {entry_date.strftime('%d/%m/%Y')}",
                f"Tiêu đề: {entry.get('title') or 'Không có tiêu đề'}",
                f"Tâm trạng: {entry.get('mood', 'Bình thường')}",
                f"Từ khóa: {entry.get('tags') or 'Không có'}",
                "",
                entry.get("content", ""),
            ]
        )
        self.textRecallDetail.setPlainText(detail)


def main() -> None:
    app = QApplication(sys.argv)
    window = DiaryWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
