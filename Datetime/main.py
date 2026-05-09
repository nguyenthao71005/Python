import json
import sys
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from uuid import uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError, available_timezones

from PyQt6 import uic
from PyQt6.QtCore import QDate, QDateTime, QSize, Qt, QTimer
from PyQt6.QtGui import QColor, QTextCharFormat
from PyQt6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QHeaderView,
    QMainWindow,
    QMessageBox,
    QStyle,
    QTableWidgetItem,
)

try:
    from PyQt6.QtCore import QCalendar
except ImportError:  # Older PyQt6 builds may not expose QCalendar.
    QCalendar = None


BASE_DIR = Path(__file__).resolve().parent
UI_PATH = BASE_DIR / "main.ui"
EVENTS_PATH = BASE_DIR / "events.json"

DEFAULT_LOCAL_ZONE = "Asia/Ho_Chi_Minh"
FALLBACK_TIMEZONES = [
    "UTC",
    "Asia/Ho_Chi_Minh",
    "Asia/Tokyo",
    "Asia/Seoul",
    "Asia/Shanghai",
    "Asia/Singapore",
    "Europe/London",
    "Europe/Paris",
    "America/New_York",
    "America/Los_Angeles",
    "Australia/Sydney",
]
FIXED_TIMEZONES = {
    "UTC": timezone.utc,
    "Asia/Ho_Chi_Minh": timezone(timedelta(hours=7), "ICT"),
    "Asia/Tokyo": timezone(timedelta(hours=9), "JST"),
    "Asia/Seoul": timezone(timedelta(hours=9), "KST"),
    "Asia/Shanghai": timezone(timedelta(hours=8), "CST"),
    "Asia/Singapore": timezone(timedelta(hours=8), "SGT"),
    "Europe/London": timezone(timedelta(hours=0), "GMT"),
    "Europe/Paris": timezone(timedelta(hours=1), "CET"),
    "America/New_York": timezone(timedelta(hours=-5), "EST"),
    "America/Los_Angeles": timezone(timedelta(hours=-8), "PST"),
    "Australia/Sydney": timezone(timedelta(hours=10), "AEST"),
}
WEEKDAY_NAMES = [
    "Thứ hai",
    "Thứ ba",
    "Thứ tư",
    "Thứ năm",
    "Thứ sáu",
    "Thứ bảy",
    "Chủ nhật",
]


def load_timezones():
    try:
        zones = sorted(available_timezones())
    except Exception:
        zones = FALLBACK_TIMEZONES[:]

    for zone_name in FALLBACK_TIMEZONES:
        if zone_name not in zones:
            zones.insert(0, zone_name)
    return zones


def timezone_for(zone_name: str):
    try:
        return ZoneInfo(zone_name)
    except (ZoneInfoNotFoundError, ValueError):
        return FIXED_TIMEZONES.get(zone_name, timezone.utc)


def offset_text(value: datetime) -> str:
    offset = value.utcoffset()
    if offset is None:
        return "UTC"

    total_minutes = int(offset.total_seconds() // 60)
    sign = "+" if total_minutes >= 0 else "-"
    total_minutes = abs(total_minutes)
    hours, minutes = divmod(total_minutes, 60)
    return f"UTC{sign}{hours:02d}:{minutes:02d}"


def qdate_from_date(value):
    return QDate(value.year, value.month, value.day)


class DateTimeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI_PATH), self)

        self.timezones = load_timezones()
        self.local_zone_name = self.resolve_local_zone()
        self.events = []
        self.marked_dates = []

        self.setup_style()
        self.setup_menu_icons()
        self.setup_clock_tab()
        self.setup_calendar_tab()
        self.setup_event_tab()
        self.setup_option_tab()
        self.load_events()

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_time_labels)
        self.clock_timer.start(1000)

        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_due_events)
        self.reminder_timer.start(1000)

        self.update_time_labels()
        self.update_calendar_details()
        self.refresh_event_table()
        self.statusLabel.setText("Sẵn sàng")

    def setup_style(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background: #f6f7fb;
                color: #172033;
                font-family: Segoe UI, Arial;
                font-size: 10.5pt;
            }
            QLabel#appTitleLabel {
                font-size: 22pt;
                font-weight: 700;
                color: #111827;
            }
            QLabel#appSubtitleLabel {
                color: #5f6b7a;
            }
            QLabel#localTimeLabel,
            QLabel#selectedTimeLabel {
                font-size: 34pt;
                font-weight: 700;
                color: #0f172a;
            }
            QLabel#localDateLabel,
            QLabel#selectedDateLabel,
            QLabel#calendarSelectedLabel {
                font-size: 12pt;
                color: #334155;
            }
            QGroupBox {
                border: 1px solid #d7dce5;
                border-radius: 8px;
                margin-top: 12px;
                padding: 14px 10px 10px 10px;
                background: #ffffff;
                font-weight: 600;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
            }
            QPushButton {
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #1d4ed8;
            }
            QPushButton#deleteEventButton,
            QPushButton#completeEventButton {
                background: #475569;
            }
            QPushButton#deleteEventButton:hover,
            QPushButton#completeEventButton:hover {
                background: #334155;
            }
            QLineEdit,
            QTextEdit,
            QComboBox,
            QDateTimeEdit {
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 6px;
                background: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #d8e0ec;
                border-radius: 10px;
                top: -1px;
                background: #ffffff;
            }
            QTabWidget::tab-bar {
                alignment: left;
                left: 12px;
            }
            QTabBar {
                background: #eaf0f8;
                border: 1px solid #d8e0ec;
                border-radius: 10px;
                padding: 4px;
            }
            QTabBar::tab {
                background: transparent;
                color: #526070;
                border: 1px solid transparent;
                border-radius: 8px;
                padding: 9px 18px;
                margin: 0 2px;
                min-width: 108px;
                font-weight: 600;
            }
            QTabBar::tab:hover {
                background: #ffffff;
                color: #1d4ed8;
                border-color: #c7d2fe;
            }
            QTabBar::tab:selected {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #3b82f6,
                    stop: 1 #2563eb
                );
                color: #ffffff;
                border-color: #1d4ed8;
                font-weight: 700;
            }
            QTabBar::tab:selected:hover {
                color: #ffffff;
            }
            QTabBar::tab:!selected {
                margin-top: 2px;
                margin-bottom: 2px;
            }
            """
        )

    def setup_menu_icons(self):
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setIconSize(QSize(18, 18))
        self.tabWidget.tabBar().setCursor(Qt.CursorShape.PointingHandCursor)

        tab_icons = {
            0: "SP_ComputerIcon",
            1: "SP_FileDialogDetailedView",
            2: "SP_MessageBoxInformation",
            3: "SP_FileDialogContentsView",
        }
        for index, icon_name in tab_icons.items():
            standard_pixmap = getattr(QStyle.StandardPixmap, icon_name, None)
            if standard_pixmap is not None and index < self.tabWidget.count():
                self.tabWidget.setTabIcon(index, self.style().standardIcon(standard_pixmap))

    def setup_clock_tab(self):
        self.timezoneCombo.addItems(self.timezones)
        self.eventZoneCombo.addItems(self.timezones)
        self.set_combo_value(self.timezoneCombo, self.local_zone_name)
        self.set_combo_value(self.eventZoneCombo, self.local_zone_name)

        self.zoneSearchEdit.setPlaceholderText("Lọc múi giờ, ví dụ: Tokyo, London, New_York")
        self.zoneSearchEdit.textChanged.connect(self.filter_timezones)
        self.timezoneCombo.currentTextChanged.connect(lambda: self.update_time_labels())
        self.copyLocalToZoneButton.clicked.connect(
            lambda: self.set_combo_value(self.timezoneCombo, self.local_zone_name)
        )

    def setup_calendar_tab(self):
        self.setup_calendar_systems()

        first_days = [
            ("Thứ hai", Qt.DayOfWeek.Monday),
            ("Chủ nhật", Qt.DayOfWeek.Sunday),
            ("Thứ bảy", Qt.DayOfWeek.Saturday),
        ]
        for label, value in first_days:
            self.firstDayCombo.addItem(label, value)
        self.firstDayCombo.setCurrentIndex(0)

        self.gridCheckBox.setChecked(True)
        self.navigationCheckBox.setChecked(True)
        self.calendarWidget.setGridVisible(True)
        self.calendarWidget.setNavigationBarVisible(True)

        self.calendarTypeCombo.currentIndexChanged.connect(lambda: self.change_calendar_system())
        self.firstDayCombo.currentIndexChanged.connect(lambda: self.change_first_day())
        self.gridCheckBox.toggled.connect(self.calendarWidget.setGridVisible)
        self.navigationCheckBox.toggled.connect(self.calendarWidget.setNavigationBarVisible)
        self.calendarWidget.selectionChanged.connect(self.update_calendar_details)
        self.calendarWidget.currentPageChanged.connect(lambda: self.update_calendar_details())
        self.todayButton.clicked.connect(self.select_today)

        self.select_today()

    def setup_calendar_systems(self):
        self.calendarTypeCombo.clear()
        if QCalendar is None:
            self.calendarTypeCombo.addItem("Dương lịch (Gregorian)")
            self.calendarTypeCombo.setEnabled(False)
            return

        candidates = [
            ("Dương lịch (Gregorian)", "Gregorian"),
            ("Julian", "Julian"),
            ("Islamic Civil", "IslamicCivil"),
            ("Jalali", "Jalali"),
            ("Milankovic", "Milankovic"),
        ]
        for label, enum_name in candidates:
            system = getattr(QCalendar.System, enum_name, None)
            if system is None:
                continue
            try:
                calendar = QCalendar(system)
                if hasattr(calendar, "isValid") and not calendar.isValid():
                    continue
                self.calendarTypeCombo.addItem(label, system)
            except Exception:
                continue

        if self.calendarTypeCombo.count() == 0:
            self.calendarTypeCombo.addItem("Dương lịch (Gregorian)")
            self.calendarTypeCombo.setEnabled(False)

    def setup_event_tab(self):
        self.eventTitleEdit.setPlaceholderText("Tên sự kiện")
        self.eventNoteEdit.setPlaceholderText("Ghi chú nhắc lịch")
        self.eventDateTimeEdit.setCalendarPopup(True)
        self.eventDateTimeEdit.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.eventDateTimeEdit.setDateTime(QDateTime.currentDateTime().addSecs(3600))

        headers = ["Sự kiện", "Thời gian", "Múi giờ", "Trạng thái", "Ghi chú"]
        self.eventTable.setColumnCount(len(headers))
        self.eventTable.setHorizontalHeaderLabels(headers)
        self.eventTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.eventTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.eventTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.eventTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.addEventButton.clicked.connect(self.add_event)
        self.deleteEventButton.clicked.connect(self.delete_selected_event)
        self.completeEventButton.clicked.connect(self.complete_selected_event)

    def setup_option_tab(self):
        self.timeFormatCombo.addItems(["24 giờ", "12 giờ AM/PM"])
        self.dateFormatCombo.addItems(["dd/MM/yyyy", "yyyy-MM-dd", "Thứ, dd/MM/yyyy"])
        self.showSecondsCheckBox.setChecked(True)
        self.showDateCheckBox.setChecked(True)
        self.autoUpdateCheckBox.setChecked(True)

        self.timeFormatCombo.currentIndexChanged.connect(lambda: self.update_time_labels())
        self.dateFormatCombo.currentIndexChanged.connect(lambda: self.refresh_all_views())
        self.showSecondsCheckBox.toggled.connect(lambda: self.update_time_labels())
        self.showDateCheckBox.toggled.connect(lambda: self.refresh_all_views())
        self.autoUpdateCheckBox.toggled.connect(self.toggle_auto_update)

    def resolve_local_zone(self) -> str:
        local_tz = datetime.now().astimezone().tzinfo
        local_name = getattr(local_tz, "key", None)
        if local_name in self.timezones:
            return local_name

        local_offset = datetime.now().astimezone().utcoffset()
        if local_offset == timedelta(hours=7) and DEFAULT_LOCAL_ZONE in self.timezones:
            return DEFAULT_LOCAL_ZONE
        return DEFAULT_LOCAL_ZONE if DEFAULT_LOCAL_ZONE in self.timezones else "UTC"

    def set_combo_value(self, combo, value: str):
        index = combo.findText(value)
        if index >= 0:
            combo.setCurrentIndex(index)

    def filter_timezones(self, keyword: str):
        current = self.timezoneCombo.currentText()
        keyword = keyword.strip().lower()
        filtered = [
            zone_name
            for zone_name in self.timezones
            if keyword in zone_name.lower()
        ] if keyword else self.timezones

        self.timezoneCombo.blockSignals(True)
        self.timezoneCombo.clear()
        self.timezoneCombo.addItems(filtered)
        self.timezoneCombo.blockSignals(False)

        if current in filtered:
            self.set_combo_value(self.timezoneCombo, current)
        elif filtered:
            self.timezoneCombo.setCurrentIndex(0)
        self.update_time_labels()

    def selected_timezone_name(self) -> str:
        return self.timezoneCombo.currentText() or self.local_zone_name

    def format_time(self, value: datetime) -> str:
        show_seconds = self.showSecondsCheckBox.isChecked()
        use_12_hour = self.timeFormatCombo.currentIndex() == 1
        if use_12_hour:
            return value.strftime("%I:%M:%S %p" if show_seconds else "%I:%M %p")
        return value.strftime("%H:%M:%S" if show_seconds else "%H:%M")

    def format_date(self, value: datetime) -> str:
        if not self.showDateCheckBox.isChecked():
            return ""

        date_format = self.dateFormatCombo.currentText()
        if date_format == "yyyy-MM-dd":
            return value.strftime("%Y-%m-%d")
        if date_format == "Thứ, dd/MM/yyyy":
            return f"{WEEKDAY_NAMES[value.weekday()]}, {value:%d/%m/%Y}"
        return value.strftime("%d/%m/%Y")

    def update_time_labels(self):
        local_zone = timezone_for(self.local_zone_name)
        selected_zone_name = self.selected_timezone_name()
        selected_zone = timezone_for(selected_zone_name)

        now_local = datetime.now(local_zone)
        now_selected = datetime.now(selected_zone)

        self.localTimeLabel.setText(self.format_time(now_local))
        self.localDateLabel.setText(self.format_date(now_local) or "Ẩn ngày")
        self.localZoneLabel.setText(f"Địa phương: {self.local_zone_name}")
        days_in_year = datetime(now_local.year, 12, 31).timetuple().tm_yday
        self.localDetailLabel.setText(
            f"{offset_text(now_local)} | Tuần {now_local.isocalendar().week} | "
            f"Ngày {now_local.timetuple().tm_yday}/{days_in_year}"
        )

        self.selectedTimeLabel.setText(self.format_time(now_selected))
        self.selectedDateLabel.setText(self.format_date(now_selected) or "Ẩn ngày")
        self.selectedZoneDetailLabel.setText(
            f"{selected_zone_name} | {offset_text(now_selected)} | Chênh lệch "
            f"{self.time_difference_text(now_local, now_selected)}"
        )

    def time_difference_text(self, local_value: datetime, selected_value: datetime) -> str:
        local_offset = local_value.utcoffset() or timedelta()
        selected_offset = selected_value.utcoffset() or timedelta()
        diff = selected_offset - local_offset
        sign = "+" if diff >= timedelta() else "-"
        total_minutes = int(abs(diff.total_seconds()) // 60)
        hours, minutes = divmod(total_minutes, 60)
        return f"{sign}{hours:02d}:{minutes:02d}"

    def change_calendar_system(self):
        if QCalendar is None:
            return

        system = self.calendarTypeCombo.currentData()
        if system is None:
            return

        try:
            self.calendarWidget.setCalendar(QCalendar(system))
            self.update_calendar_details()
        except Exception as exc:
            self.statusLabel.setText(f"Không đổi được bộ lịch: {exc}")

    def change_first_day(self):
        day = self.firstDayCombo.currentData()
        if day is not None:
            self.calendarWidget.setFirstDayOfWeek(day)

    def select_today(self):
        today = datetime.now(timezone_for(self.local_zone_name)).date()
        self.calendarWidget.setSelectedDate(qdate_from_date(today))
        self.calendarWidget.showSelectedDate()
        self.update_calendar_details()

    def update_calendar_details(self):
        selected = self.calendarWidget.selectedDate().toPyDate()
        selected_dt = datetime.combine(selected, time.min)
        selected_text = self.format_date(selected_dt) or selected.strftime("%d/%m/%Y")
        iso_year, iso_week, iso_day = selected.isocalendar()
        self.calendarSelectedLabel.setText(
            f"Ngày chọn: {selected_text} | "
            f"Tuần ISO {iso_week}/{iso_year} | Thứ {iso_day}"
        )

    def toggle_auto_update(self, enabled: bool):
        if enabled:
            self.clock_timer.start(1000)
            self.update_time_labels()
            self.statusLabel.setText("Đã bật tự động cập nhật giờ")
        else:
            self.clock_timer.stop()
            self.statusLabel.setText("Đã tắt tự động cập nhật giờ")

    def refresh_all_views(self):
        self.update_time_labels()
        self.update_calendar_details()
        self.refresh_event_table()

    def event_datetime_from_form(self) -> datetime:
        qdt = self.eventDateTimeEdit.dateTime()
        zone_name = self.eventZoneCombo.currentText() or self.local_zone_name
        event_date = qdt.date().toPyDate()
        event_time = qdt.time().toPyTime()
        return datetime.combine(event_date, event_time).replace(tzinfo=timezone_for(zone_name))

    def add_event(self):
        title = self.eventTitleEdit.text().strip()
        if not title:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập tên sự kiện.")
            return

        zone_name = self.eventZoneCombo.currentText() or self.local_zone_name
        event_time_value = self.event_datetime_from_form()
        now_in_zone = datetime.now(timezone_for(zone_name))
        if event_time_value <= now_in_zone:
            QMessageBox.warning(self, "Thời gian chưa hợp lệ", "Thời gian nhắc phải lớn hơn hiện tại.")
            return

        self.events.append(
            {
                "id": str(uuid4()),
                "title": title,
                "when": event_time_value.isoformat(),
                "zone": zone_name,
                "note": self.eventNoteEdit.toPlainText().strip(),
                "notified": False,
            }
        )
        self.save_events()
        self.refresh_event_table()
        self.eventTitleEdit.clear()
        self.eventNoteEdit.clear()
        self.eventDateTimeEdit.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        self.statusLabel.setText("Đã thêm lịch nhắc")

    def selected_event_id(self):
        selected_items = self.eventTable.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Chưa chọn sự kiện", "Vui lòng chọn một dòng trong bảng.")
            return None
        return selected_items[0].data(Qt.ItemDataRole.UserRole)

    def delete_selected_event(self):
        event_id = self.selected_event_id()
        if event_id is None:
            return

        confirm = QMessageBox.question(
            self,
            "Xác nhận xóa",
            "Bạn có chắc chắn muốn xóa sự kiện đã chọn không?",
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        self.events = [event for event in self.events if event["id"] != event_id]
        self.save_events()
        self.refresh_event_table()
        self.statusLabel.setText("Đã xóa lịch nhắc")

    def complete_selected_event(self):
        event_id = self.selected_event_id()
        if event_id is None:
            return

        for event in self.events:
            if event["id"] == event_id:
                event["notified"] = True
                break
        self.save_events()
        self.refresh_event_table()
        self.statusLabel.setText("Đã đánh dấu hoàn thành")

    def load_events(self):
        if not EVENTS_PATH.exists():
            self.events = []
            return

        try:
            raw_events = json.loads(EVENTS_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            self.events = []
            self.statusLabel.setText("Không đọc được events.json, đã mở danh sách trống")
            return

        valid_events = []
        for event in raw_events:
            if not isinstance(event, dict):
                continue
            if not all(key in event for key in ("id", "title", "when", "zone")):
                continue
            try:
                self.parse_event_datetime(event)
            except ValueError:
                continue
            event.setdefault("note", "")
            event.setdefault("notified", False)
            valid_events.append(event)
        self.events = valid_events

    def save_events(self):
        EVENTS_PATH.write_text(
            json.dumps(self.events, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def parse_event_datetime(self, event: dict) -> datetime:
        event_time_value = datetime.fromisoformat(event["when"])
        if event_time_value.tzinfo is None:
            event_time_value = event_time_value.replace(tzinfo=timezone_for(event["zone"]))
        return event_time_value

    def refresh_event_table(self):
        sorted_events = sorted(self.events, key=lambda event: event["when"])
        self.eventTable.setRowCount(len(sorted_events))

        for row_index, event in enumerate(sorted_events):
            event_time_value = self.parse_event_datetime(event)
            display_zone = timezone_for(event["zone"])
            display_time = event_time_value.astimezone(display_zone)
            status = "Đã nhắc" if event.get("notified") else "Đang chờ"
            values = [
                event["title"],
                f"{self.format_date(display_time)} {self.format_time(display_time)}".strip(),
                event["zone"],
                status,
                event.get("note", ""),
            ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setData(Qt.ItemDataRole.UserRole, event["id"])
                if column_index in (1, 2, 3):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.eventTable.setItem(row_index, column_index, item)

        self.refresh_event_marks()

    def refresh_event_marks(self):
        for marked_date in self.marked_dates:
            self.calendarWidget.setDateTextFormat(marked_date, QTextCharFormat())
        self.marked_dates = []

        highlight = QTextCharFormat()
        highlight.setBackground(QColor("#dbeafe"))
        highlight.setForeground(QColor("#1d4ed8"))

        local_zone = timezone_for(self.local_zone_name)
        for event in self.events:
            if event.get("notified"):
                continue
            event_date = self.parse_event_datetime(event).astimezone(local_zone).date()
            qdate = qdate_from_date(event_date)
            self.calendarWidget.setDateTextFormat(qdate, highlight)
            self.marked_dates.append(qdate)

    def check_due_events(self):
        now_utc = datetime.now(timezone.utc)
        due_events = []

        for event in self.events:
            if event.get("notified"):
                continue
            event_time_value = self.parse_event_datetime(event)
            if event_time_value.astimezone(timezone.utc) <= now_utc:
                event["notified"] = True
                due_events.append(event)

        if not due_events:
            return

        self.save_events()
        self.refresh_event_table()
        message_lines = []
        for event in due_events:
            event_time_value = self.parse_event_datetime(event).astimezone(timezone_for(event["zone"]))
            note = event.get("note", "").strip()
            message = (
                f"- {event['title']} ({self.format_date(event_time_value)} "
                f"{self.format_time(event_time_value)} - {event['zone']})"
            )
            if note:
                message += f"\n  {note}"
            message_lines.append(message)

        QMessageBox.information(
            self,
            "Nhắc lịch",
            "Đến giờ cho sự kiện:\n" + "\n".join(message_lines),
        )


def main():
    app = QApplication(sys.argv)
    window = DateTimeWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
