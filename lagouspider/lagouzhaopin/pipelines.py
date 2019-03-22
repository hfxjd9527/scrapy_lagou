# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from lagouzhaopin.settings import SQL_DATETIME_FORMAT
class LagouzhaopinPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            db=settings['MYSQL_DBNAME'],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = """
        insert into lagou(url_object_id, url, title, salary, job_city, work_years, degree_need, job_type, 
        publish_time, job_advantage, job_desc, job_addr, company_name, company_url, crawl_time)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (item['url_object_id'], item['url'], item['title'], item['salary'],
                                   item['job_city'], item['work_years'], item['degree_need'], item['job_type'],
                                   item['publish_time'], item['job_advantage'], item['job_desc'], item['job_addr'],
                                   item['company_name'], item['company_url'], item['crawl_time'].strftime(SQL_DATETIME_FORMAT)))
