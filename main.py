import os
import sys
import time
import subprocess
import atexit

proc = subprocess.Popen(["Xvfb", ":42"])
atexit.register(proc.terminate)

from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QWidget, QApplication

os.environ["DISPLAY"] = ":42"
time.sleep(1)

app = QApplication(sys.argv)
widget = QWidget()
widget.show()

print("done")
