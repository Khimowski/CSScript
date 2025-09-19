import requests
from requests import Session

from utils.configUtil import configUtil


class sessionUtil:
    @staticmethod
    def getSession():
        return requests.Session()

    @staticmethod
    def setSession(session : Session):
        url = configUtil.readConfigFile("websiteConfig.ini", "website")["url"]
        headers = {
            "User-Agent" : configUtil.readConfigFile("sessionConfig.ini","headers")["user-agent"],
            "Referer" : configUtil.readConfigFile("sessionConfig.ini","headers")["referer"],
        }
        session.headers = headers
        response = requests.get(url)
        session.cookies = response.cookies
        return session