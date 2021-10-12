import requests
import json
import os
from requests import RequestException

def read_key():
    """  持久化key,便于读取 """
    key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user-key')
    with open(key_path, 'r', encoding='utf-8') as f:
        key = f.read()
    return key

def request_url_get(url, paraments):
    """ 请求url方法get方法 """
    try:
        r = requests.get(url=url, params=paraments, timeout = 10)
        if r.status_code == 200:
            return r.text
    except RequestException:
        print('请求url返回错误异常')
        return None

def parse_json(content_json):
    """  解析json函数 """
    result_json = json.loads(content_json)
    return result_json

def request_api(url, address):
    """ 请求高德api 解析json """
    params = {
        'key': read_key(),
        'keywords': address,
        'extensions' : all
    }
    result = request_url_get(url, params)
    result_json = parse_json(result)
    return result_json

def distance_get(pos1, pos2):
    url = 'https://restapi.amap.com/v4/direction/bicycling?parameters'
    params = {
        'key' : read_key(),
        'origin' : pos1,
        'destination' : pos2,
    }
    result = request_url_get(url, params)
    result_json = parse_json(result)
    distance = result_json['data']["paths"][0]["distance"]
    return distance