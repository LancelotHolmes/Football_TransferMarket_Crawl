import scrapy

class ContinentCountrySpider(scrapy.Spider):
    name='continent_country_spider'

    start_urls=[
        # start from the leagues website divided by continents
        'http://www.transfermarkt.co.uk/wettbewerbe/europa',
        'http://www.transfermarkt.co.uk/wettbewerbe/asien',
        'http://www.transfermarkt.co.uk/wettbewerbe/amerika',
        'http://www.transfermarkt.co.uk/wettbewerbe/afrika',
    ]

    def parse(self,response):
        # lst_countries=response.css('map area::attr("href")').extract()
        dct_country = {}
        lst_country = response.css('map area::attr("title")').extract()
        continent = response.url.split('/')[-1]
        dct_continent={}
        dct_continent[continent] = lst_country

        dct_country=dict.fromkeys(lst_country,continent)
        # print dct_country
        yield dct_continent
        # for url_country in lst_countries:
        #     yield scrapy.Request(response.urljoin(url_country),callback=self.parse_country)