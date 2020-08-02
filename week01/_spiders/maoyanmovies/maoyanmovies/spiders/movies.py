"""
作业2：
使用 Scrapy 框架和 XPath 抓取猫眼电影的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。
"""

import re

import scrapy
from scrapy.selector import Selector
import pandas as pd



class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3&sortId=3']

    cookies = {
        '__mta': '214915368.1595729169975.1595729511253.1595729516796.8',
        'uuid_n_v': 'v1',
        'uuid': '91DF7E70CEE411EAACA59DB4EC64C4A81A3350F864DB496E86E9FCE0789E74F9', 
        '_csrf': '63953af58cf6aa2ee1b6ad67e77409408f9e6ab5ec2252265ea508648878a9bb',
        '_lxsdk_cuid': '17388decdd1c8-093c63ffd10222-31617403-1fa400-17388decdd1c8',
        '_lxsdk': '91DF7E70CEE411EAACA59DB4EC64C4A81A3350F864DB496E86E9FCE0789E74F9', 
        'mojo-uuid': 'a477c029bcb1c2a6c573360ed1967228',
        'mojo-session-id': '{"id":"4e5b4698113396e405d9f7799c8186e3","time":1595729169957}',
        'lt': 'iOSIt4nYa3hIX_tXf7yfTd5QEdMAAAAAHAsAACnGueM3MFYb5V34skxuW555cjYPLsLRWZg1hpHY_nuKtxpmiJI9i6tFC---bSPVaQ',
        'lt.sig': 'cInxeSjAWXs40JSo9cMx-7Ga7EY',
        'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2': '1595729170,1595729215,1595729264,1595729297',
        '__mta': '214915368.1595729169975.1595729499367.1595729511253.7',
        'mojo-trace-id': '13',
        'Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2': '1595729517',
        '_lxsdk_s': '17388decdd2-04c-28a-d13%7C%7C20'
    }

    data = [
        ['name', 'type', 'date']
    ]

    # def parse(self, response):
    #     pass

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, cookies=self.cookies, dont_filter=True)


    # 解析函数
    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        top = 10
        for movie in movies:
            # 第一部分: 提取电影名称和电影类型
            part1 = movie.xpath('./div[@class="movie-hover-title"]')
            info = [ tag.extract() for tag in part1]
            name = re.search(r'.*<span class="name ">(.*?)</span>', info[0], re.M|re.I)
            if name:
                name = name.group(1)
            type = info[1].split('\n')[2].strip()

            # 第二部分: 提取电影上映时间
            part2 = movie.xpath('./div[@class="movie-hover-title movie-hover-brief"]')
            info = [ tag.extract() for tag in part2 ]
            date = info[0].split('\n')[2].strip()
            
            # 打印关键信息
            self.data = self.data + [[name] + [type] + [date]]
            print('-----------------------------')
            print(f'name={name}, type={type}, date={date}, data={self.data}')

            # 按排名取前十名
            top -= 1
            if top <= 0:
                break
        
        movie2 = pd.DataFrame(data = self.data)
        movie2.to_csv('../movie2.csv', encoding='utf8', index=False, header=False, mode='a')

