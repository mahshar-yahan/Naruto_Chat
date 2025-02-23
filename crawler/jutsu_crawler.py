import scrapy
from bs4 import BeautifulSoup

class BlogSpider(scrapy.Spider):
    name = 'narutospider'
    start_urls = ['https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu']

    def parse_jutsu(self,response):
        jutsu_name = response.css('span.mw-page-title-main::text').extract()[0]
        jutsu_name = jutsu_name.strip()

        div_selctor = response.css('div.mw-parser-output')[0]
        div_html = div_selctor.extract()

        soup = BeautifulSoup(div_html.find('div'))

        jutsu_type = ""

        if soup.find('aside'):
            aside = soup.find('aside')

            for cell in aside.find_all('div',{'class':'pi-data'}):
                if cell.find('h3'):
                    cell_name = cell.find('h3').text.strip()
                    if cell_name == "Classification":
                        jutsu_type = cell.find('div').text.strip()
        
        soup.find('aside').decompose()
        justsu_description = soup.text.split('Trivia')[0].strip()


        return dict(
            jutsu_name = jutsu_name,
            justsu_description =justsu_description,
            jutsu_type = jutsu_type
        )
    
    def parse(self, response):
        for herf in response.css('.smw-columnlist-container')[0].css("a::attr(href)").extract():
            extracted_data = scrapy.Request('https://naruto.fandom.com/'+ herf, 
                                            callback=self.parse_jutsu)
            yield extracted_data

        for next_page in response.css('a.mw-nextlink'):
            yield response.follow(next_page, self.parse)
    
    






