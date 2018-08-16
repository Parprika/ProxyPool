import redis
from random import choice
from proxypool import settings
from proxypool.error import PoolEmptyError


class RedisClient(object):
    def __init__(self, host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis 密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=settings.INITIAL_SCORE):
        """
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not self.db.zscore(settings.REDIS_KEY, proxy):
            return self.db.zadd(settings.REDIS_KEY, score, proxy)

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果最高分数不存在，则按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(settings.REDIS_KEY, settings.MAX_SCORE, settings.MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(settings.REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        代理值减一分，分数小于最小值则代理删除
        :param proxy:
        :return:
        """
        score = self.db.zscore(settings.REDIS_KEY, proxy)
        if score and score > settings.MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(settings.REDIS_KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(settings.REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断代理是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(settings.REDIS_KEY, proxy) is None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结束
        """
        print('代理', proxy, '可用，设置为', settings.MAX_SCORE)
        return self.db.zadd(settings.REDIS_KEY, settings.MAX_SCORE, proxy)

    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zcard(settings.REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(settings.REDIS_KEY, settings.MIN_SCORE, settings.MAX_SCORE)
