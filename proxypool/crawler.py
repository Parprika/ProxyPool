import json
from pyquery import PyQuery as pq
from proxypool.utils import get_page


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=10):
        """
        获取66免费代理网
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url=url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_kuaidaili(self, page_count=10):
        """
        获取快代理免费代理
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url=url)
            if html:
                doc = pq(html)
                trs = doc('#list tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_xicidaili(self, page_count=10):
        """
        获取西刺免费代理ip
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.xicidaili.com/nn/{}'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url=url)
            if html:
                doc = pq(html)
                trs = doc('#body table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(2)').text()
                    port = tr.find('td:nth-child(3)').text()
                    yield ':'.join([ip, port])

    def crawl_data5u(self):
        """
        获取无忧代理ip
        :return: 代理
        """
        start_url = 'http://www.data5u.com/free/{}/index.shtml'
        urls = [start_url.format(type) for type in ['gngn', 'gnpt']]
        for url in urls:
            print('Crawling', url)
            html = get_page(url=url)
            if html:
                doc = pq(html)
                uls = doc('.wlist ul li ul:gt(0)').items()
                for ul in uls:
                    ip = ul.find('span:nth-child(1)').text()
                    port = ul.find('span:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_kxdaili(self, page_count=10):
        """
        获取开心代理
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://ip.kxdaili.com/dailiip/1/{}.html#ip'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url=url)
            if html:
                doc = pq(html)
                trs = doc('.tab_c_box table tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_mogudaili(self):
        """
        获取蘑菇代理
        :return: 代理
        """
        start_url = 'http://www.mogumiao.com/proxy/free/listFreeIp'
        print('Crawling', start_url)
        html = get_page(url=start_url)
        if html:
            items = json.loads(html).get('msg')
            for item in items:
                ip = item.get('ip')
                port = item.get('port')
                yield ':'.join([ip, port])

    def crawl_yundaili(self, page_count=10):
        """
        获取云代理
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.ip3366.net/?stype=1&page={}'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url=url)
            if html:
                doc = pq(html)
                trs = doc('#container table tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_xiongmaodaili(self):
        """
        获取熊猫代理
        :return: 代理
        """
        start_url = 'http://www.xiongmaodaili.com/xiongmao-web/freeip/list'
        print('Crawling', start_url)
        html = get_page(start_url)
        if html:
            items = json.loads(html).get('obj')
            for item in items:
                ip = item.get('ip')
                port = str(item.get('port'))
                yield ':'.join([ip, port])
