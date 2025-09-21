import requests
from requests import Session

from utils.configUtil import configUtil


class sessionUtil:
    """
    [工具类]
    操作session的工具类
    """
    @staticmethod
    def getSession():
        """
        获取一个session
        :return: session
        """
        return requests.Session()

    @staticmethod
    def setSession(session : Session):
        """
        设置session
        :param session:

        :return: sessionAfterSetting
        """
        url = configUtil.readConfigFile("websiteConfig.ini", "website")["loginurl"]
        headers = {
            "Connection" : "keep-alive",
            "Content-Type" : "application/x-www-form-urlencoded",
            "Host" :"jwxt.sias.edu.cn",
            "Origin" : "https://jwxt.sias.edu.cn",
            "User-Agent" : configUtil.readConfigFile("sessionConfig.ini","headers")["user-agent"],
            "Referer" : configUtil.readConfigFile("sessionConfig.ini","headers")["referer"],
        }
        session.headers = headers
        response = requests.get(url)
        session.cookies = response.cookies
        return session