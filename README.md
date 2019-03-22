# scrapy_lagou
使用scrapy，对拉勾招聘信息进行全网抓取。
几个小知识点：
1.使用fake-useragent代理；
2.使用twisted的异步机制将爬到的数据异步保存到数据库；
3.使用scrapy item loader机制，便于以后代码的维护。
