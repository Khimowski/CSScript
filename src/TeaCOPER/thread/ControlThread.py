import threading
import queue
import time
from typing import List, Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot

from src.TeaCOPER.manager import LogManager
from src.TeaCOPER.module import SelectModule
from src.TeaCOPER.model import Course
from src.TeaCOPER.thread import WorkerThread

logger = LogManager("控制线程")

class ControlThread(QObject, threading.Thread):
    course_status_changed = Signal(str, str)   # 课程代码 : 状态
    worker_status_changed = Signal(int, str)   # 线程号 : 状态
    process_finished = Signal(int, int)        # 完成数 : 总数

    def __init__(self):
        QObject.__init__(self)
        threading.Thread.__init__(self)
        self.daemon = True

        self.command_queue = queue.Queue()   # 命令队列 : GUI -> 控制线程
        self.worker_queue = queue.Queue()    # 工作队列 : 工作线程 -> 控制线程
        self.resource_queue = queue.Queue()  # 资源队列 : 控制线程 -> 工作线程

        self.workers = []
        self.running = False
        self.course_list = []

    def run(self):
        """控制线程主循环"""
        self.running = True
        self._start_workers()

        while self.running:
            try:
                # 监听并处理来自前端的命令
                self._process_commands()

                # 处理工作线程状态更新
                self._process_worker_status_update()

                # 检查工作线程状态
                self._check_workers_status()

                time.sleep(0.05)
            except Exception as e:
                logger.error(e)

    def _start_workers(self):
        from src.TeaCOPER.module import SelectModule
        from src.TeaCOPER.module import LoginModule
        from src.TeaCOPER.utils import SessionUtil

        # 初始化session
        logger.info("正在获取会话")
        session = SessionUtil.getSession()
        session = SessionUtil.initSession(session)
        logger.info("成功获取会话")

        # 模拟登录
        logger.info("正在模拟登录")
        login_module = LoginModule(session)
        get = login_module.login()
        logger.debug(get)
        logger.info("完成模拟登录")

        ### 这里需要补充验证方法来激活会话
        ### 否则后续抢课进程无法进行，会被重定向回主页
        ### 等待开发这一部分

        # 创建工作线程
        for i in range(8): # 8线程测试，后续改为GUI输入
            worker = WorkerThread(
                worker_id = i,
                session = session,
                course_list = self.course_list,
                status_queue = self.worker_queue,
                resource_queue = self.resource_queue
            )
            self.workers.append(worker)
            worker.start()
            self.worker_status_changed.emit()

    def _process_commands(self):
        """处理来自前端的命令"""

    def _execute_command(self, command: Dict[str, Any]):
        """执行具体命令"""

    def _distribute_courses(self):
        """分配课程到工作线程"""

    def _process_worker_status_update(self):
        """处理工作线程状态更新"""

    def _handle_workers_status(self):
        """处理单个工作线程状态"""

    def _check_workers_status(self):
        """检查工作线程状态"""

    def _stop_workers(self):
        """停止所有工作线程"""

    def _pause_workers(self):
        """暂停所有工作线程"""

    def _resume_workers(self):
        """恢复所有工作成饭"""

    def start_selection(self, courses: List[Course]):
        """开始选课"""

    def stop_selection(self):
        """停止选课"""

    def update_settings(self, settings : Dict[str : Any]):
        """更新设置"""
