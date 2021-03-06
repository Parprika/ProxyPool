import requests
from requests.exceptions import ConnectionError

base_headers = {
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
}


def get_page(url, options={}):
    headers = dict(base_headers, **options)
    print('正在抓取', url)
    try:
        response = requests.get(url=url, headers=headers)
        print('抓取成功', url, response.status_code)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('抓取失败', url)
        return None
