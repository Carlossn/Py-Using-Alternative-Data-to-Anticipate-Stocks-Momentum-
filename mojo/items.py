# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
class MovieItem(scrapy.Item):

    Parent = scrapy.Field() 
    Name = scrapy.Field()
    Year = scrapy.Field()
    Date = scrapy.Field()
    Distrib = scrapy.Field()
    Genre = scrapy.Field()
    Opening = scrapy.Field()
    Domestic = scrapy.Field()
    Overseas = scrapy.Field()
    Total = scrapy.Field()
    Budget = scrapy.Field()
    Mkting = scrapy.Field()
    ParentRev = scrapy.Field()
    GProfit = scrapy.Field()
    NProfit = scrapy.Field()
    ROC = scrapy.Field()
    