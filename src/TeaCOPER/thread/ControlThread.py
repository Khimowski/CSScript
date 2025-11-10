import threading
import queue
import time
from typing import List, Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal


class ControlThread(QObject, threading.Thread):
    def __init__(self):
        QObject.__init__(self)
        threading.Thread.__init__(self)
        self.daemon = True

