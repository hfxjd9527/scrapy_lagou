# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import scrapy
from w3lib.html import remove_tags


class LagouItemLoad(ItemLoader):
    default_output_processor = TakeFirst()


class LagouzhaopinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    def remove_splash(value):
        # 去掉工作城市的斜线
        return value.replace("/", "")

    def handle_job_addr(value):
        addr_list = value.split("\n")
        addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
        return "".join(addr_list)

    def handle_publish_time(value):
        return value.replace("发布于拉勾网", "").strip()

    def remove_space(value):
        return value.strip()

    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field(
        input_processor=MapCompose(remove_space),
    )
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash, remove_space),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field(
        input_processor=MapCompose(handle_publish_time),
    )
    crawl_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_space),
    )
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_job_addr),
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
