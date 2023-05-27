import os
import sys
import time
import subprocess
import atexit


def test_terminate(proc):
    proc.terminate()


proc = subprocess.Popen(["Xvfb", ":42"])
atexit.register(test_terminate, proc)

from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QWidget, QApplication

os.environ["DISPLAY"] = ":42"
time.sleep(1)

app = QApplication(sys.argv)
widget = QWidget()
widget.show()

print("done")
