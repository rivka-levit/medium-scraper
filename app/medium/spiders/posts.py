import scrapy
import time

from scrapy.loader import ItemLoader
from scrapy.selector import Selector

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from medium.items import MediumItem


class PostsSpider(scrapy.Spider):
    name = "posts"
    allowed_domains = ["medium.com"]
    start_urls = ["https://medium.com"]

    def parse(self, r, **kwargs):
        options = webdriver.ChromeOptions()
        # options.headless = True
        driver = webdriver.Remote(
            command_executor='http://chrome:4444',
            options=options
        )
        driver.get(self.start_urls[0])
        driver.implicitly_wait(5)

        try:
            driver.find_element(
                By.XPATH,
                '/html/body/div[1]/div/div[3]/div[2]/div/div[1]/div/div/div/div[3]/div[4]/div/p/span/a'
            ).click()
            time.sleep(3)
        except (Exception, NoSuchElementException) as e:
            print(e.msg)

        i = 1
        num_scrolls = 10
        last_height = driver.execute_script(
            "return document.body.scrollHeight"
        )

        while True and i <= num_scrolls:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(3)
            new_height = driver.execute_script(
                "return document.body.scrollHeight"
            )
            if new_height == last_height:
                break
            last_height = new_height

            response = driver.page_source
            selector = Selector(text=response)
            containers = selector.xpath('//main//div[@class="gb lk ll lm"]')

            for c in containers:
                item = ItemLoader(
                    item=MediumItem(),
                    response=response,
                    selector=c
                )
                item.add_xpath(
                    'title',
                    './/h2/text()'
                )
                item.add_xpath(
                    'excerpt',
                    './/div[@class="h k ng ej eo"]/p/text()'
                )
                item.add_xpath(
                    'link',
                    './/div[@class="ly s"]//a/@href'
                )
                yield item.load_item()

            i += 1

        driver.quit()
