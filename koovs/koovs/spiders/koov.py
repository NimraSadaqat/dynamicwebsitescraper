import scrapy
from selenium.common.exceptions import TimeoutException
from ..items import KoovsItem
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class KoovSpider(scrapy.Spider):
    name = 'koov'
    start_urls = ['https://www.koovs.com/tags/sweet-summer-vibes']

    def __init__(self, name=None, **kwargs):
        super(KoovSpider, self).__init__(name, **kwargs)
        self.browser = webdriver.Chrome('D:/chromedriver_win32/chromedriver.exe')

    @staticmethod
    def get_selenium_response(browser, url):
        browser.get(url)
        WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='prodBox']/li")))
        table = browser.find_element_by_css_selector("#prodBox")

        get_number = 0
        while True:
            count = get_number
            products = table.find_elements_by_css_selector("li.imageView")
            # print(products)
            browser.execute_script("arguments[0].scrollIntoView();", products[-1])  # scroll to last row
            try:
                button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "loadMoreList")))
                button.click()
            except TimeoutException:
                print("No more LOAD MORE RESULTS button to be clicked")
                break
            get_number = len(products)
            print(get_number)
            time.sleep(1)
            if get_number == count:
                break

        return browser.page_source.encode('utf-8')

    def parse(self, response):
        koov_response = scrapy.Selector(text=self.get_selenium_response(self.browser, response.url)) # Sending url to selenium webdriver and collecting the selenium response
        item = KoovsItem()
        products = koov_response.css('li.imageView')
        a=1
        for x in products:
            item['no'] = a
            a = a+1
            title = x.css('.productName::text').extract()
            price = x.css('.product_price').css('::text').extract()
            image = x.css('img.prodImg::attr(src)').extract()
            item['title'] = ''.join(title)
            item['price'] = ''.join(price)
            item['image'] = ''.join(image)
            with open('data.txt', 'a', encoding="utf-8") as f: # Writing data to file
                f.write('Item No: {0}, Title: {1},Price: {2}, Image: {3}\n'.format(item['no'], item['title'], item['price'],  item['image']))
            yield item # Writing data to sqlite database file
