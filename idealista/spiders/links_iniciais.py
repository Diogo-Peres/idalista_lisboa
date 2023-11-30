import scrapy

class PrecosMiniprecoSpider(scrapy.Spider):

    name = "precos_idealista"
    allowed_domains = ["www.idealista.pt"]

    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000
        },
        "REQUEST_FINGERPRINTER_CLASS": "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ZYTE_API_KEY": "9d29172683b843caa81c9fa7504e1894", # Enter Your API Key kere
        "ZYTE_API_TRANSPARENT_MODE": True
    }

    start_urls = [
                    "https://www.idealista.pt/geo/comprar-casas/area-metropolitana-de-lisboa/"
                ]

    def parse(self, response):
        # Extract information about each product in the category
        for product_link in response.xpath('//a[@class="item-link "]/@href').extract():
            yield scrapy.Request(response.urljoin(product_link), callback=self.parse_item)

        # Pagination: Follow the "Next" link
        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_item(self, response):
        yield {
            "id_produto": response.xpath('//div[@class="ad-reference-container"]/p/text()').get(),
            'titulo': response.xpath('//span[@class="main-info__title-main"]/text()').get(),
            "preco": response.xpath('//span[@class="info-data-price"]/span/text()').get(),
            
        }

