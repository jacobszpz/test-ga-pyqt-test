import pytest
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QWidget

class TestWorkflow:

    def test_workflow_error(self, qtbot):
        widget = QWidget()
        qtbot.addWidget(widget)
        widget.show()
        assert widget.isVisible()


