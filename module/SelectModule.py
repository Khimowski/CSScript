import logging

from model.CourseModel import CourseModel
from utils.configUtil import configUtil

import requests
from requests import Session
import time
import threading
from bs4 import BeautifulSoup

class SelectModule:
    def __init__(self, session: Session, courseList : list, interval = 1):
        self.session = session
        self.courseList = courseList
        self.url = configUtil.readConfigFile("websiteConfig.ini","website")["courseselecturl"]
        self.profile = configUtil.readConfigFile("websiteConfig.ini","website")["profile"]

        self.url = self.url + self.profile
        print(self.url)
        self.session.headers["Referer"] = "https://jwxt.sias.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id="+self.profile
        self.interval = interval
        self.timelock = threading.Lock()
        self.lasttime = time.time()

        print(self.session.headers)
        print(self.session.cookies)
        self.session.cookies["semester.id"] = "242"
        self.session.cookies["srv_id"] = "srv1"
        print(self.session.cookies)

        input("回车继续...")


    def isSuccess(self, response):
        print(response.text)
        print(dict(response.cookies))
        print(response.headers)
        print(response.status_code)
        soup = BeautifulSoup(response.text, "html.parser")
        result_div = soup.find('div',
                               style=lambda s: s and 'width:85%' in s and 'text-align:left' in s and 'margin:auto' in s)

        if not result_div:
            print("未找到!")
            return 404

        result_text = result_div.get_text(strip=True)

        logging.info(result_text)
        if "成功" in result_text:
            print(f"抢课成功!")
            return 200
        else:
            if "已经选过" in result_text:
                print(f"已经选过!")
                return 201
            print(f"抢课失败!原因:{result_text}")
            return 400

    def SelectMethod(self, course : CourseModel, retry_count = 1):
        data = {
            'optype': 'true',
            'operator0': f'{course.getCourseId()}:true:0',
            'lesson0': f'{course.getCourseId()}',
            f'schLessonGroup_{course.getCourseId()}': 'undefined'
        }
        params = {
            'profileId' : self.profile,
        }

        try:
            print(f"第 {retry_count} 次尝试选课 {course.getCourseName()}")

            with self.timelock:
                elapsed = time.time() - self.lasttime
                if elapsed < self.interval:
                    time.sleep(self.interval - elapsed)
                self.lasttime = time.time()
            response = self.session.post(self.url, data=data, params=params)
            result = self.isSuccess(response)
            if result == 400 or result == 404:
                if retry_count < 3:
                    return self.SelectMethod(course, retry_count + 1)
                else:
                    return False
            else:
                return True
        except Exception as e:
            if retry_count < 3:
                return self.SelectMethod(course, retry_count + 1)
            else:
                print(f"发生错误{e}")
                return False


    def worker(self):
        while not len(self.courseList) <= 0:
            course = self.courseList.pop()
            status = self.SelectMethod(course)
            if status:
                print(f"{course} 抢课成功")
            else:
                print(f"{course} 抢课失败，正在重试")
                self.courseList.append(course)
                time.sleep(self.interval)

    def selectStart(self):
        threads = []
        for i in range(min(len(self.courseList), 8)):
            thread = threading.Thread(target=self.worker)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()





