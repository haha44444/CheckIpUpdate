# -*- coding: utf-8 -*-
import socket
import time
import datetime
import requests

# 邮箱
email = f'xxx@xxx.com'
# 密码
password = f'password'

# 使用了LeCDN的网站的url
url_website = f'https://cdn.kkccc.com'

# 你使用ddns的域名
domain = f'test1.haha44444.top'
# 端口
port = f'25565'
# 权重
weight = f'15'

# 更改转发列表中第x行的转发
# 0代表1，1代表2，以此类推，如果你只有一个转发保持默认即可
forward_list_row_x = f'0'


def get_cookie():
    url = f'{url_website}/prod-api/login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    data = {
        "email": email,
        "password": password
    }
    session = requests.session()
    res = session.post(url, data=data, headers=headers)
    token = res.json()
    return token['data']['access_token']


def get_stream_id():
    url = f'{url_website}/prod-api/stream?listen_port=&cname=&stream_id=&status=&current_page=1&total=0&page_size=10'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'Authorization': f'Bearer {get_cookie()}'
    }
    session = requests.session()
    res = session.get(url, headers=headers)
    stream_id = res.json()['data']['data'][forward_list_row]['id']
    return stream_id


def get_id():
    url = f'{url_website}/prod-api/stream_source?stream_id={get_stream_id()}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'Authorization': f'Bearer {get_cookie()}'
    }
    session = requests.session()
    res = session.get(url, headers=headers)
    id = res.json()['data'][0]['id']
    return id


def change_ip(ip):
    url_put = f'{url_website}/prod-api/stream_source/105'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'Authorization': f'Bearer {get_cookie()}'
    }

    data = {
        'stream_id': get_stream_id(),
        'content': ip,
        'port': port,
        'weight': weight,
        'id': get_id()
    }
    session = requests.session()
    res = session.put(url_put, headers=headers, data=data)
    if res.status_code == '200':
        print("update successful.")
    else:
        print("update failed")

def get_ipAddresses(domain):
    ipAddresses = [0]
    while True:
        time.sleep(2)
        ip = socket.gethostbyname(domain)
        if ip != ipAddresses[-1]:
            ipAddresses.append(ip)
            print(str(datetime.datetime.now())[:19] + '===>' + ip)
            change_ip(ip)


if __name__ == "__main__":
    get_ipAddresses(domain)