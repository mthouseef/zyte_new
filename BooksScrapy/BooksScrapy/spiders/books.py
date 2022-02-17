import scrapy
from BooksScrapy.BooksScrapy.items import BookItem
from scrapy.loader import ItemLoader


class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = [
        'http://books.toscrape.com'
    ]

    def parsePages(self, response, main_url):
        for book in response.xpath("//section/div/ol[@class='row']/li"):
            book_loader = ItemLoader(item=BookItem(), selector=book)
            product_pod_loader = book_loader.nested_xpath(".//article[contains(@class,'product_pod')]")
            product_pod_loader.add_xpath('book', "./h3/a/@title")
            product_pod_loader.add_xpath('price', "./div[contains(@class,'product_price')]/p[contains(@class,'price_color')]/text()")            
            product_pod_loader.add_xpath('image_url', "concat('{0}',./div[contains(@class,'image_container')]/a/img[contains(@class,'thumbnail')]/@src)".format(main_url))
            product_pod_loader.add_xpath('book_url', "concat('{0}catalogue/',./h3/a/@href)".format(main_url))
            yield book_loader.load_item()

        next_page = response.xpath("//section/div/div//ul[@class='pager']/li[@class='next']/a/@href").extract_first()

        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parsePages, cb_kwargs=dict(main_url=main_url))

    def parse(self, response):
        for category in response.xpath("//ul[@class='nav nav-list']/li/ul/li/a//@href"):
            cat_url = response.urljoin(category.get())
            yield scrapy.Request(url=cat_url, callback=self.parsePages, cb_kwargs=dict(main_url=response.url))

 
