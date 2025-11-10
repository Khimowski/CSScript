import threading


class BaseThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        return None