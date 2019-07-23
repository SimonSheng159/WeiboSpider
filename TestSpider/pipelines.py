# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
import mysql.connector
import pandas as pd
import redis
from scrapy.exceptions import DropItem

redis_db = redis.Redis(host='127.0.0.1', port=3306, db='scrapymysql') #连接redis，相当于MySQL的conn
redis_data_dict = "userId"  #key的名字，写什么都可以，这里的key相当于字典名称，而不是key值。

class TestspiderPipeline(object):
    def process_item(self, item, spider):
        self.cursor.execute(
            """insert ignore into infoTable(userName, sex, location,userid)
            value (%s, %s, %s,%s)""",  # 纯属python操作mysql知识，不熟悉请恶补
            (item['userName'],  # item里面定义的字段和表字段对应
             item['sex'],
             item['location'],
             item['userid']
            ))

        # 提交sql语句
        self.connect.commit()
        print('item ok')
        return item  # 必须实现返回

    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='scrapyMysql',  # 数据库名
            user='root',  # 数据库用户名
            passwd='s19990615z',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();

#        redis_db.flushdb()   # 删除全部key，保证key为0，不然多次运行时候hlen不等于0，刚开始这里调试的时候经常出错。
#       if redis_db.hlen(redis_data_dict) == 0:    #
#            sql = "SELECT userId FROM infoTable"  # 从你的MySQL里提数据，我这里取url来去重。
#           df = pd.read_sql(sql, self.conn)  # 读MySQL数据
#            for userId in df['userId'].get_values():  # 把每一条的值写入key的字段里
#                redis_db.hset(redis_data_dict, userId, 0)  # 把key字段的值都设为0，你要设成什么都可以，因为后面对比的是字段，而不是值。

#    def process_item(self, item, WeiboSpider):
#        if redis_db.hexists(redis_data_dict,
#                item['userId']):  # 取item里的userId和key里的字段对比，看是否存在，存在就丢掉这个item。不存在返回item给后面的函数处理
#                raise DropItem("Duplicate item found: %s" % item)
#        return item

