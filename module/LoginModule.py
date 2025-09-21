import hashlib
import logging

from requests import Session
from utils.saltUtil import SaltUtil
from utils.configUtil import configUtil

class LoginModule:
    """
    [模块类]
    实现模拟登录的模块类
    """
    def __init__(self, session : Session):
        self.session = session
        self.url = configUtil.readConfigFile("websiteConfig.ini","website")["loginurl"]
        self.__username = configUtil.readConfigFile("userConfig.ini","user")["username"],
        self.__password = configUtil.readConfigFile("userConfig.ini","user")["password"]

    def login(self):
        """
        实现模拟登录的方法
        :return: responseWhenLogin
        """
        logging.info("LoginModule | 正在准备模拟登录")
        logging.info("LoginModule | 正在调用saltUtil")
        salt = SaltUtil.getSalt(self.session,self.url)
        print(salt)
        print(self.__password)

        params = {
            "username" : self.__username,
            "password" : hashlib.sha1((salt+self.__password).encode()).hexdigest(),
            "session_locale" : "zh_CN",
        }

        response = self.session.post(self.url,params = params)
        print(response.cookies)
        return response