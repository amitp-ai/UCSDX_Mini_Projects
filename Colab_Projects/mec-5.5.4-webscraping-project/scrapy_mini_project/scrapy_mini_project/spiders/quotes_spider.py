import scrapy


#from terminal, call using: 'scrapy crawl quotes'
#Basic Spider that only saves the raw content of the scraped website
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        
#####################################################


#from terminal, call using: 'scrapy crawl quotes_extract'
#More advanced Spider that also extracts relevant text from the scraped website
#Note: having start_requests() is not necessary
class QuotesSpider_extract(scrapy.Spider):
    name = "quotes_extract"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
            

#####################################################


#from terminal, call using: 'scrapy crawl quotes_extract_rec_to_scrap_css -o css-scraper-results.json'
#More advanced Spider that also recursively extracts relevant text from the scraped website (like all the links in the page are crawled)
#Note: having start_requests() is not necessary
class QuotesSpider_extract_rec_css(scrapy.Spider):
    name = "quotes_extract_rec_to_scrap_css"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            #yield response.follow(next_page, callback=self.parse)  #supports relative url (unlike scrapy.Request)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


#####################################################

'''
need to fix this. doesn't work as is.
#from terminal, call using: 'scrapy crawl quotes_extract_rec_to_scrap_css -o css-scraper-results.json'
#More advanced Spider that also recursively extracts relevant text from the scraped website (like all the links in the page are crawled)
#Note: having start_requests() is not necessary
class QuotesSpider_extract_rec_xpath(scrapy.Spider):
    name = "quotes_extract_rec_to_scrap_xpath"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.xpath('//div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            #yield response.follow(next_page, callback=self.parse)  #supports relative url (unlike scrapy.Request)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

'''