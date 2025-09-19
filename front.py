import hashlib
import requests
import re
from bs4 import BeautifulSoup


def extract_uuid_from_file(filename):
    """
    从文件中提取UUID字符串

    Args:
        filename (str): 文件名

    Returns:
        str: 提取到的UUID字符串，如果提取失败返回None
    """
    try:
        # 读取文件并获取第12行（索引为11，因为从0开始）
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # 确保文件至少有12行
            if len(lines) < 12:
                return None
            line_12 = lines[11].strip()

        # 使用字符串切割提取目标部分
        # 查找 "SHA1('" 的位置
        start_marker = "SHA1('"
        end_marker = "' + form"

        start_index = line_12.find(start_marker)
        if start_index == -1:
            return None

        start_index += len(start_marker)
        end_index = line_12.find(end_marker)

        if end_index == -1 or end_index <= start_index:
            return None

        # 提取目标字符串
        target_string = line_12[start_index:end_index]
        return target_string

    except FileNotFoundError:
        print(f"错误：文件 {filename} 未找到")
        return None
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return None

def get_uuid(html_content):
    """
    使用BeautifulSoup从HTML响应中提取CryptoJS.SHA1使用的UUID
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找所有script标签
    scripts = soup.find_all('script')
    for script in scripts:
        if script.string and 'CryptoJS.SHA1' in script.string:
            with open("get.txt", "w", encoding="utf-8") as f:
                f.write(script.string)
                f.close()
            return extract_uuid_from_file("get.txt")
    return None

'''
#uuid = input("请输入uuid:")
uuid = "9eae51b7-e3a1-42b2-93a1-5eac605b8db8-"
password = "Sakuya7645."
url = "https://jwxt.sias.edu.cn/eams/loginExt.action"
params = {
    "username": "2023105150156",
    "password": hashlib.sha1((uuid+password).encode()).hexdigest(),
    "session_locale": "zh_CN",
}

response = requests.post(url,params=params,headers=headers)
print(params["password"])
print(response.status_code)
print(response.text)
'''

headers = {
    "User-Agent": "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Referer": "https://jwxt.sias.edu.cn/eams/loginExt.action",
}

url = "https://jwxt.sias.edu.cn/eams/loginExt.action"
session = requests.Session()

response = requests.get(url)
cookies = response.cookies

session.cookies = cookies
session.headers = headers
response = session.get(url)
print(response.text)
print("\n\n\n")
print(f"自动获取的uuid为:{get_uuid(response.text)}")
uuid = get_uuid(response.text)
password = "Sakuya7645."
params = {
    "username": "2023105150156",
    "password": hashlib.sha1((uuid+password).encode()).hexdigest(),
    "session_locale": "zh_CN",
}
response = session.post(url,params=params)
print(response.text)
with open("get.html","w",encoding="utf-8") as f:
    f.write(response.text)
    f.close()
print(response.status_code)
cookie = session.cookies
headers = session.headers
print(headers)