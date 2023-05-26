from enum import IntEnum
from typing import Optional
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QWidget, QFileDialog


class SyncPeriod(IntEnum):
    """Enum containing all valid Sync intervals for this UI."""

    HALF_HOUR = 60 * 30
    ONE_HOUR = 60 * 60
    SIX_HOURS = 60 * 60 * 6


class Assets:
    """Helper class to get the path of app assets."""

    _icon_filename = 'logo.png'
    _watermark_filename = 'watermark.png'

    @staticmethod
    def _get_qt_asset_path(asset_file) -> Path:
        """Get the `Path` corresponding to a Qt UI file."""
        return (Path(__file__).parent / f"{asset_file}.ui").resolve()

    @classmethod
    def load_ui(cls, qt_obj):
        """Load a UI file for a `QObject`."""
        uic.loadUi(cls._get_qt_asset_path(qt_obj.__class__.__name__), qt_obj)

    @staticmethod
    def _get_asset_path(icon) -> Path:
        """Get the `Path` of a media asset."""
        return (Path(__file__).parent.parent / 'assets' / icon).resolve()

    @classmethod
    @property
    def icon(cls) -> QIcon:
        """`QIcon` of application logo."""
        return QIcon(str(cls._get_asset_path(cls._icon_filename)))

    @classmethod
    @property
    def watermark(cls) -> QPixmap:
        """`QPixmap` of application watermark."""
        wm = QPixmap(str(cls._get_asset_path(cls._watermark_filename)))
        wm = wm.scaledToWidth(100)
        return wm


class SettingsWindow(QWidget):
    """Settings windown UI element."""

    _window_title = "Settings"
    _initial_position = (300, 300)
    _log_out_signal = pyqtSignal()
    _save_signal = pyqtSignal()

    def __init__(self):
        """Create instance of SettingsWindow."""
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        Assets.load_ui(self)

        self.move(*self._initial_position)
        self.setWindowTitle(self._window_title)

        self.select_download_location.clicked.connect(self._choose_location)
        self._log_out_signal = self.log_out_button.clicked
        self._save_signal = self.button_box.accepted

    def _choose_location(self) -> None:
        if (location := self._file_chooser_dialog()):
            self.download_location = location

    def _file_chooser_dialog(self) -> Optional[Path]:
        self.file_chooser = QFileDialog()
        self.file_chooser.setFileMode(QFileDialog.Directory)

        if self.file_chooser.exec():
            new_location = self.file_chooser.directory()
            return Path(new_location.path())

        return None

    @property
    def download_location(self) -> Path:
        """`Path` of download location."""
        return self._download_location

    @download_location.setter
    def download_location(self, location: Path) -> None:
        self._download_location = location.resolve()
        self.download_location_hint.setText(str(self._download_location))

    @property
    def data_source(self) -> str:
        """Filter which Blackboard source to download."""
        return self.data_source_edit.text()

    @data_source.setter
    def data_source(self, data_source: str) -> None:
        self.data_source_edit.setText(data_source)

    @property
    def sync_frequency(self) -> int:
        """Seconds to wait between each sync job."""
        return int([*SyncPeriod][self.frequency_combo.currentIndex()])

    @sync_frequency.setter
    def sync_frequency(self, f: int) -> None:
        self.frequency_combo.setCurrentIndex([*SyncPeriod].index(SyncPeriod(f)))

    @property
    def username(self) -> str:
        """Username of current session."""
        return self.current_session_label.text()

    @username.setter
    def username(self, username: str) -> None:
        if username:
            self.current_session_label.setText(f"Logged in as {username}")
        else:
            self.current_session_label.setText("Not currently logged in")

    @property
    def log_out_signal(self):
        """Fire when user chooses to log out."""
        return self._log_out_signal

    @property
    def save_signal(self):
        """Fire when settings are saved."""
        return self._save_signal

