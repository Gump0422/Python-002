# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import pymysql

class MaoyanmoviesPipeline:

    def process_item(self, item, spider):
        data = {}
        # temp = []
        # data['name'] = [item['name']]
        # data['type'] = [item['type']]
        # data['date'] = [item['date']]
        # movie2 = pd.DataFrame(data = data)
        # movie2.to_csv('./movie2.csv', encoding='utf8', index=False, header=False, mode='a')
        conn = pymysql.connect(
           host='127.0.0.1', 
           port=3306, 
           user='root',
           password='wujian', 
           db='spidetest', 
           charset='utf8'
           )
           
        cursor = conn.cursor()
        sql = f"insert into spidetest(name, type, date) values({item['name']}, {item['type']}, {item['date']})"

        cursor.execute(sql)
        cursor.close()
        conn.close()
        return item
