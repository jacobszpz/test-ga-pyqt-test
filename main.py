import os
import sys
import time
import subprocess
import atexit

from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QWidget, QApplication

def test_terminate(proc):
    time.sleep(12)
    proc.terminate()


proc = subprocess.Popen(["Xvfb", ":42"])
atexit.register(test_terminate, proc)

os.environ["DISPLAY"] = ":42"
time.sleep(1)

app = QApplication(sys.argv)
widget = QWidget()
widget.show()

print("done")
