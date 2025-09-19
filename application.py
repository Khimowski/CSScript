import time

from utils.sessionUtil import sessionUtil
from utils.configUtil import configUtil

from module.LoginModule import LoginModule

def run():
    session = sessionUtil.getSession()
    session = sessionUtil.setSession(session)
    time.sleep(2)

    LoginModel = LoginModule(session)
    get = LoginModel.login()
    print(get.text)

if __name__ == '__main__':
    run()