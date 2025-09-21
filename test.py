from utils.configUtil import configUtil

import re
import json

def extract_number_from_line(line):
    """
    从字符串中提取数字
    """
    if line is None:
        return None

    # 使用正则表达式匹配数字
    match = re.search(r'(\d+)', line)
    if match:
        return match.group(1)
    return None

def find_previous_line(filename, search_text):
    """
    在文件中搜索文本，找到时返回上一行的内容
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            previous_line = None
            current_line = None

            for line in file:
                current_line = line.strip()

                if search_text in current_line:
                    if previous_line is not None:
                        match = re.search(r'(\d+)', previous_line)
                        if match:
                            return match.group(1)
                        return None
                    else:
                        return "这是第一行，没有上一行"

                previous_line = current_line

            return f"未找到包含 '{search_text}' 的行"

    except FileNotFoundError:
        return f"文件不存在: {filename}"
    except Exception as e:
        return f"读取文件时出错: {e}"

def parse_javascript_json(response_text):
    """
    从JavaScript变量声明中提取JSON数据
    """
    try:
        # 使用正则表达式提取JSON数组部分
        # 匹配 var lessonJSONs = [{...}]; 模式
        pattern = r'var lessonJSONs\s*=\s*(\[.*?\]);'
        match = re.search(pattern, response_text, re.DOTALL)

        if match:
            json_str = match.group(1)
            # 解析JSON
            data = json.loads(json_str)
            return data
        else:
            print("未找到 lessonJSONs 变量定义")
            return None

    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None
    except Exception as e:
        print(f"其他错误: {e}")
        return None

def test():
    str = find_previous_line("course_data.action","25261.12022026-2.03")
    a = extract_number_from_line(str)
    print(a)


if __name__ == '__main__':
    test()