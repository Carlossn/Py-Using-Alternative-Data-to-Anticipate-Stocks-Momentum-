# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter

class WriteItemPipeline(object):

    def __init__(self):
        self.filename = 'mojo.csv'

    def open_spider(self, spider):
        self.csvfile = open(self.filename, 'wb') #'wb' = write in binary ab= append in binary
        self.exporter = CsvItemExporter(self.csvfile)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csvfile.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    # def process_item(self, item, spider):
    #     line = str(item['film'][0]) + '\t' + str(item['year'][0])\
    #             + '\t' + str(item['awards'][0]) + '\t'\
    #             + str(item['nominations'][0]) + '\n'
    #     self.file.write(line)
    #     return item
        
