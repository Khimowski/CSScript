from requests import Session

from utils.configUtil import configUtil
from model.CourseModel import CourseModel
from utils.courseIdUtil import courseIdUtil


class CourseModule:
    """
    [模块类]
    获取课程列表的模块类
    """
    def __init__(self, session: Session):
        self.session = session


    def getCourseList(self):
        """
        获取course列表
        :return: course_list
        """

        courseList = configUtil.readJsonCourseConfigFile("courseList.json")

        for course in courseList:
            id = courseIdUtil.getCourseId(self.session, course)
            course.setCourseId(id)

        return courseList




