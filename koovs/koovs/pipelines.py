# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class KoovsPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.con = sqlite3.connect('myquotes.db')
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute("DROP TABLE IF EXISTS quotes_tb")
        self.cur.execute("create table quotes_tb(no text,title text,price text,image text)")

    def process_item(self, item, spider):
        self.store_db(item)

    def store_db(self,item):
        self.cur.execute("insert into quotes_tb values(?,?,?,?)", (item['no'],item['title'],item['price'],item['image']))
        self.con.commit()
