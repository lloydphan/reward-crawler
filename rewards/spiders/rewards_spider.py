import scrapy
import logging
import os
from rewards.file import File
from rewards.sql import MySql
import json


class QuotesSpider(scrapy.Spider):
    name = "rewards"
    total_record = 319
    domains = "https://rewards.cimbbank.com.my"
    results_updated = "results_updated.txt"
    results = "results.txt"
    new_file = None
    update_file = None
    connect_mysql = None

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.update_file = File(self.results_updated)
        if self.update_file.isFile(self.results_updated) is False:
            self.new_file = File(self.results)
            self.new_file.openOrCreate()
        else:
            self.connect_mysql = MySql('localhost', 'root', '', 'rewards')
            for line in self.update_file.readLnsFile():
                data = str(line).replace("\n", "").strip()
                # data = json.loads(data_json.strip())
                logging.debug("Code:" + str(data))
                arr = data.split("|")
                values = (arr[0], arr[1], arr[2], arr[3])
                self.connect_mysql.insert_value(values)

    def start_requests(self):
        if self.new_file is not None:
            str_exp = 'https://rewards.cimbbank.com.my/index.php?ch=cb_rwd&pg=cb_rwd_itms&nhmxl5=10&stmxl5='
            urls = self.getArrayUrls(self.total_record, str_exp)
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if self.new_file is not None:
            for row in response.xpath('//tr[has-class("ctlgLine")]')[1:]:
                code = str(row.xpath('td[1]//text()').extract_first()).strip()
                if self.isNotBlank(code):
                    image = str(self.domains + "/" + str(row.xpath('td[1]//a//img/@src').extract_first()))
                    desc = str(row.xpath('td[2]//node()').extract_first())
                    price = str(row.xpath('td[3]//text()').extract_first()).replace('BP', '').replace(',','').strip()
                    line = code + "|" + image + "|" + desc + "|" + price
                self.new_file.writeFile(line)

    def __del__(self):
        if self.new_file is not None:
            self.new_file.rename(self.results, self.results_updated)
            logging.debug("Change name")

    def getArrayUrls(self, total_record, str_exp):
        urls = []
        number_page = round(total_record / 10)
        for i in range(number_page):
            url = str_exp + str(i * 10)
            urls.append(url)
        return urls

    def isNotBlank(self, string):
        return bool(string and string.strip())

    def rename(self, old_name, new_name):
        os.rename(old_name, new_name)
