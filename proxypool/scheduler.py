import time
from multiprocessing import Process
from proxypool import settings
from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester


class Scheduler():
    def scheduler_tester(self, cycle=settings.TESTER_CYCLE):
        """
        定时测试代理
        :param cycle: 测试周期
        :return: None
        """
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def scheduler_getter(self, cycle=settings.GETTER_CYCLE):
        """
        定时获取代理
        :param cycle: 获取周期
        :return: None
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def scheduler_api(self):
        """
        开启API
        :return: None
        """
        app.run(settings.API_HOST, settings.API_PORT)

    def run(self):
        print('代理池开始运行')
        if settings.TESTER_ENABLED:
            tester_process = Process(target=self.scheduler_tester)
            tester_process.start()
        if settings.GETTER_ENABLED:
            getter_process = Process(target=self.scheduler_getter)
            getter_process.start()
        if settings.API_ENABLED:
            api_process = Process(target=self.scheduler_api)
            api_process.start()
