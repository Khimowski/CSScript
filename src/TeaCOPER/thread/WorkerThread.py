import threading
from queue import Queue
from typing import List, Dict
from src.TeaCOPER.model import Course, Session


class WorkerThread(threading.Thread):
    def __init__(self, worker_id:int , session:Session,
                 course_list:List[Course], status_queue:Queue, resource_queue:Queue):
        threading.Thread.__init__(self)
        self.worker_id = worker_id
        self.session = session
        self.course_list = course_list
        self.status_queue = status_queue
        self.resource_queue = resource_queue