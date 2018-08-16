import time
import aiohttp
import asyncio
from asyncio import TimeoutError
from proxypool import settings
from proxypool.database import RedisClient
try:
    from aiohttp import ClientError, ClientConnectorError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy: 单个代理
        :return: None
        """
        connection = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=connection) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(url=settings.TEST_URL, headers=settings.HEADERS, proxy=real_proxy, timeout=15) as response:
                    if response.status in settings.VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print('代理可用', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应码不合法', proxy)
            except (ClientError, ClientConnectorError, TimeoutError, AttributeError, TimeoutError):
                self.redis.decrease(proxy)
                print('代理请求失败', proxy)

    def run(self):
        """
        测试主函数
        :return: None
        """
        print('测试器开始运行')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            # 批量测试
            for i in range(0, len(proxies), settings.BATCH_TEST_SIZE):
                test_proxies = proxies[i:i + settings.BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)
