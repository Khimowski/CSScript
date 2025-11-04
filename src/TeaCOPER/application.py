import time
from tkinter.tix import Select

from src.TeaCOPER.utils.SessionUtil import SessionUtil

from src.TeaCOPER.module.SelectModule import SelectModule
from src.TeaCOPER.module.LoginModule import LoginModule
from src.TeaCOPER.module.CourseModule import CourseModule

from src.TeaCOPER.manager.LogManager import LogManager

def run():
    logger = LogManager("中央控件")
    logger.info("正在获取会话")
    session = SessionUtil.getSession()
    session = SessionUtil.initSession(session)
    logger.info("获取会话成功")
    time.sleep(1)

    LoginModuleObject = LoginModule(session)
    get = LoginModuleObject.login()
    print(get.text)
    url = "https://jwxt.sias.edu.cn/eams/homeExt.action"
    response = session.get(url)
    print("发送主页get请求:")
    print(response.cookies)
    print(response.headers)

    CourseModuleObject = CourseModule(session)
    courseList = CourseModuleObject.getCourseList()

    userInput = float(input("请输入一个抢课间隔(若输入过大则自动归位0.5s):"))
    SelectModuleObject = SelectModule(session, courseList, max(0.5,userInput))
    SelectModuleObject.selectStart()

if __name__ == '__main__':
    run()