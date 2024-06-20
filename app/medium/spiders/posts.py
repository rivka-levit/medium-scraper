import scrapy
import time

from scrapy.loader import ItemLoader
from scrapy.selector import Selector

from selenium import webdriver
from selenium.webdriver.common.by import By

from medium.items import MediumItem


class PostsSpider(scrapy.Spider):
    name = "posts"
    allowed_domains = ["medium.com"]
    start_urls = ["https://medium.com/m/signin", "https://medium.com"]

    def parse(self, r, **kwargs):
        options = webdriver.ChromeOptions()
        # options.headless = True
        driver = webdriver.Remote(
            command_executor='http://chrome:4444',
            options=options
        )
        driver.get(self.start_urls[0])
        driver.implicitly_wait(5)

        driver.find_element(
            By.XPATH,
            '//button[div="Sign in with email"]'
        ).click()
        time.sleep(2)

        input_box = driver.find_element(By.XPATH, './/input[@type="email"]')
        btn = driver.find_element(By.XPATH, './/button[text()="Continue"]')

        input_box.send_keys('juliacreadora@gmail.com')
        time.sleep(1)
        btn.click()

        # driver.get_screenshot_as_file('screenshot.png')

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
