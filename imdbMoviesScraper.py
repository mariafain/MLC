from contextlib import suppress
import scrapy

class ImdbSpider(scrapy.Spider):
    name = "imdb"

    start_urls = []
    for i in range(0,199):
        if i is 0:
            start_urls.append('https://www.imdb.com/search/title/?genres=action&start=0&explore=title_type,genres&ref_=adv_nxt')
        else:
            resultCount = str(i*50+1)
            start_urls.append('https://www.imdb.com/search/title/?genres=action&start='+resultCount+'&explore=title_type,genres&ref_=adv_nxt')

    def parse(self, response):
        for movie in response.css('div.lister-item-content'): 
            title = plot = year = genres = ""
            with suppress(AttributeError):
                title = movie.css('h3.lister-item-header a::text')[0].get().strip()
                year = movie.xpath('.//h3/span[2]/text()').get().strip()
                plot = movie.xpath('.//p[2]/text()').get().strip()
                genres = movie.css('p.text-muted span.genre::text').get().strip()
            
            yield {
                'title': title,
                'year': year,
                'plot': plot,
                'genres': genres,
            }
        
        nextPage = response.css('div.desc a::attr(href)')[1].get()
        if nextPage is not None:
            yield response.follow(nextPage, self.parse)