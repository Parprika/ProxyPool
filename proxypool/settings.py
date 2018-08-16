MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'

POOL_UPPER_THRESHOLD = 10000    # 代理池的最大数量

VALID_STATUS_CODES = [200]
TEST_URL = 'https://www.zhihu.com/'
BATCH_TEST_SIZE = 100

TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

API_HOST = '0.0.0.0'
API_PORT = 5555

HEADERS = {
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
}
