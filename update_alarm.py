import requests
import threading
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# import random

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def login(ip, port, uri, user, password):
    url = "https://{}:{}{}".format(ip, port, uri)

    payload = {
	"grantType":"password",
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
        "X-AUTH-TOKEN": token,
        # "fileLocationURI": "sftp://sopuser:Changeme_123@{}:22/home/sopuser/alarm_lkr_pentestxxx_{}.json".format(ip, random.randint(0,1000))
    }

    response = requests.request(method, url, json=payload, headers=header, verify=False)
    if response.status_code == 200:
        print("接口请求成功：", response.status_code)
    else:
        try:
            print("接口请求失败，返回码：", response.status_code, json.dumps(response.json(), indent=4))
        except:
            print("接口请求失败：", response.status_code, response.text)


if __name__ == '__main__':

    # 环境信息
    IP = "76.0.39.11"
    PORT = "26335"
    LOGIN_URL = "/rest/plat/smapp/v1/oauth/token"
    USER = "nbiuser"
    PASS = "Test_12345"

    # 并发数
    threads = 100
    # 请求数
    request_num = 1000000

    auth_token = login(IP, PORT, LOGIN_URL, USER, PASS)

    # METHOD = 'GET'
    METHOD = 'POST'
    API = '/restconf/v1/operations/huawei-nce-alarm:update-alarms'
    # API = '/restconf/v1/operations/huawei-nce-notification-action:establish-subscription'
    # API = '/restconf/v1/data/ietf-alarms:alarms/alarm-inventory'
    # API = '/restconf/v1/data/ietf-alarms:alarms/alarm-list'
    # API = '/restconf/v1/operations/huawei-nce-notification-action:establish-subscription'
    # API = '/restconf/v1/data/ietf-alarms:alarms/shelved-alarms'
    # API = '/restconf/streams/ws/v1/identifier/7934bacd-8586-4cab-8158-0d26dfaeee11'
    # API = '/api/rest/performanceManagement/v1/10.25.76.33/telemetrySubscription'
    # API = '/restconf/v2/data/huawei-nce-resource-inventory:ltps'
    # API = '/restconf/v2/data/huawei-nce-resource-inventory:optical-nes'
    # API = '/restconf/v2/data/huawei-nce-resource-inventory:network-elements'
	
	PAYLOAD = 
	
    if auth_token:
        T = 0
        for num in range(request_num):
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
            T += time2 - time1

        print("==========测试结果==========")
        print('总耗时（秒）：', T)
        print('每次请求耗时（秒）：', T / threads * request_num)

    else:
        print("测试结束")
	
