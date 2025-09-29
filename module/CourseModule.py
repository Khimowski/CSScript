from requests import Session

from utils.ConfigUtil import ConfigUtil
from utils.CourseIdUtil import CourseIdUtil

from model.CourseModel import CourseModel

from manager.LogManager import LogManager

class CourseModule:
    """
    [模块类]
    获取课程列表的模块类
    """
    def __init__(self, session : Session):
        self.logger = LogManager("课程代码模块")
        self.session = session


    def getCourseList(self):
        """
        获取course列表
        :return: course_list
        """

        courseList = ConfigUtil.readJsonCourseConfigFile("courseList.json")

        for course in courseList:
            id = CourseIdUtil.getCourseId(self.session, course)
            course.setCourseId(id)

        return courseList




