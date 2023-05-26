from PyQt5.QtWidgets import (QMenu, QStyle, QAction, QDialog, QWidget, QWizard,
                             QCompleter, QFileDialog, QMessageBox,
                             QApplication, QSystemTrayIcon)

from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from pathlib import Path

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

    def __init__(self):
        """Create instance of SettingsWindow."""
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        Assets.load_ui(self)

        self.move(*self._initial_position)
        self.setWindowTitle(self._window_title)

    @property
    def download_location(self) -> Path:
        """`Path` of download location."""
        return self._download_location

    @download_location.setter
    def download_location(self, location: Path) -> None:
        self._download_location = location.resolve()
        self.download_location_hint.setText(str(self._download_location))

