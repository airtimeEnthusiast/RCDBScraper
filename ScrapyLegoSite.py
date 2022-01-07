import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://brickset.com/sets/year-2016']

def parse(self, response):
    SET_SELECTOR  = '. set'
    for brickset in response.css(SET_SELECTOR):
          NAME_SELECTOR = 'h1 ::text'
          PIECES_SELECTOR = 'dl[dr/text() = "Pieces"]/add/a/text()'
          
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
            }
