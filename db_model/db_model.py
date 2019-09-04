from redis import StrictRedis
from pickle import loads,dumps
from random import choice
"""
创建redis数据库类，实现一个url队列,包括取和放
"""
REDIS_HOST = "192.168.1.138"
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_USER = None
REDIS_PASSWORD = None
REDIS_KEY = "url_queue"
MAX_SCORE = 5
MIN_SCORE = 0
class RedisDB():
    def __init__(self):
        """
        初始化redis，配置redis的基本参数
        """
        try:
            redis = StrictRedis(host=REDIS_HOST,port=REDIS_PORT,db = REDIS_DB)
            self.redis=redis
        except Exception as e:
            print("连接数据库失败：", e.args)
    def add(self,url,score=MAX_SCORE):
        """
        添加序列化url，设置初始化参数
        :param url:序列化url类
        :param score:成绩
        :return: 添加结果
        """
        if not self.redis.zscore(REDIS_KEY,url):
            print("id:",loads(url)["id"],"添加成功")
            self.redis.zadd(REDIS_KEY,{url:score})
    def decrease(self,url):
        """
        请求失败后，分数减一分,请求5次后移除
        :param url:
        :return: 减分结果
        """
        score = self.redis.zscore(REDIS_KEY,url)
        if score and score>=1:
            print("id:",loads(url)["id"],"请求次数：",MAX_SCORE-score+1,"请求次数+1")
            return self.redis.zincrby(REDIS_KEY,-1,url)
        else:
            print("id:",loads(url)["id"],"请求次数：",MAX_SCORE-score+1,"移除")
            return self.redis.zrem(REDIS_KEY,url)
    def rem(self,url):
        """
        请求成功后移除
        :param url:
        :return: 移除结果
        """
        print("id:", loads(url)["id"], "请求成功", "移除")
        return self.redis.zrem(REDIS_KEY, url)

    def random(self):
        """
        随机获取一个url，首先尝试获取分数最高的，如果高分数不存在，则按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.redis.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.redis.zrevrange(REDIS_KEY, 0, 5)
            if len(result):
                return choice(result)
            else:
                raise Exception
    def empty(self):
        """
        判断是否为空
        :return: 布尔值
        """
        return self.redis.zcard(REDIS_KEY)==0
    def count(self):
        """
        集合元素个数
        :return: 数量
        """
        return self.redis.zcard(REDIS_KEY)
