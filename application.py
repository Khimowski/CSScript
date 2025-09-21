import time
from tkinter.tix import Select

from module.SelectModule import SelectModule
from utils.sessionUtil import sessionUtil
from utils.configUtil import configUtil

from module.LoginModule import LoginModule
from module.CourseModule import CourseModule

def run():
    session = sessionUtil.getSession()
    session = sessionUtil.setSession(session)
    time.sleep(2)

    LoginModuleObject = LoginModule(session)
    get = LoginModuleObject.login()
    print(get.text)
    url = "https://jwxt.sias.edu.cn/eams/homeExt.action"
    response = session.get(url)
    print(response.cookies)
    print(response.headers)

    CourseModuleObject = CourseModule(session)
    courseList = CourseModuleObject.getCourseList()

    userInput = float(input("请输入一个抢课间隔(若输入过大则自动归位0.5s):"))
    SelectModuleObject = SelectModule(session, courseList, max(0.5,userInput))
    SelectModuleObject.selectStart()

if __name__ == '__main__':
    run()