import requests
import threading
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def login(ip, port, uri, user, password):
    url = "https://{}:{}{}".format(ip, port, uri)

    payload = {
        "grantType": "password",
        "userName": user,
        "value": password
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    login_response = requests.request("PUT", url, json=payload, headers=headers, verify=False)
    if login_response.status_code == 200:
        token = login_response.json()['accessSession']
        print('登录成功！')
        return token
    else:
        print('登录失败！')
        print('登录失败原因：', json.dumps(login_response.json(), indent=4))
        return None


def api_requests(ip, port, api, method, payload, token):
    url = "https://{}:{}{}".format(ip, port, api)
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Language": "en-US",
        "X-AUTH-TOKEN": token
    }

    response = requests.request(method, url, json=payload, headers=header, verify=False)
    if response.status_code == 200:
        print("接口请求成功：", response.status_code)
    else:
        try:
            print("接口请求失败，返回码：", response.status_code, json.dumps(response.json(), indent=4))
        except:
            print("接口请求失败：", response.status_code)


if __name__ == '__main__':

    IP = "10.118.178.194"
    PORT = "26335"
    LOGIN_URL = "/rest/plat/smapp/v1/sessions"
    USER = "RestUser_lkr"
    PASS = "Changeme_123"
    threads = 2000

    auth_token = login(IP, PORT, LOGIN_URL, USER, PASS)

    METHOD = 'GET'
    # API = '/restconf/v1/data/ietf-alarms:alarms/alarm-inventory'
    API = '/restconf/v1/data/ietf-alarms:alarms/alarm-list'
    PAYLOAD = ''

    if auth_token:
        Threads = []
        time1 = time.process_time()
        for i in range(threads):
            t = threading.Thread(target=api_requests, args=(IP, PORT, API, METHOD, PAYLOAD, auth_token,))
            t.setDaemon(True)
            Threads.append(t)

        for t in Threads:
            t.start()
        for t in Threads:
            t.join()

        time2 = time.process_time()

        print("==========测试结果==========")
        print('总耗时（秒）：', time2 - time1)
        print('每次请求耗时（秒）：', (time2 - time1) / threads)

    else:
        print("测试结束")
