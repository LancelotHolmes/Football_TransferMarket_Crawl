import scrapy

class LeagueSizeSpider(scrapy.Spider):
    name='leagues_size'

    start_urls=[
        # start from the leagues website divided by continents
        'http://www.transfermarkt.co.uk/wettbewerbe/europa?page=1',
        'http://www.transfermarkt.co.uk/wettbewerbe/asien?page=1',
        'http://www.transfermarkt.co.uk/wettbewerbe/amerika?page=1',
        'http://www.transfermarkt.co.uk/wettbewerbe/afrika?page=1',
    ]

    def parse(self,response):
        # lst_league=self.get_league_url(response)
        # # follow links to specific leagues page
        # for href in lst_league:
        #     yield scrapy.Request(response.urljoin(href),callback=self.parse_league)
        #
        # # follow pagination links
        # next_page= response.css("li.naechste-seite a::attr(href)").extract_first()
        # if next_page is not None:
        #     next_page=response.urljoin(next_page)
        #     yield scrapy.Request(next_page,callback=self.parse)

        lst_countries=response.css('map area::attr("href")').extract()
        for url_country in lst_countries:
            yield scrapy.Request(response.urljoin(url_country),callback=self.parse_country)

    def parse_country(self,response):
        lst_league=self.get_league_url(response)
        # follow links to specific leagues page
        for href in lst_league:
            yield scrapy.Request(response.urljoin(href),callback=self.parse_league)

    # def get league urls
    def get_league_url(self, response):
        leagues = response.css("div.responsive-table")
        lst = leagues.css("td.hauptlink .inline-table td a::attr(href)").extract()
        size = len(lst)
        lst1 = []
        for i in range(0, size):
            if i % 2 != 0:
                lst1.append(lst[i])
        return lst1

    def parse_league(self,response):
        league = response.css(".content form::attr(action)").extract_first()
        lst_season=response.css(".inline-select option::attr(value)").extract()
        for season in lst_season:
            url = league + "?saison_id=" + season
            # follow links to leagues website of different seasons
            yield scrapy.Request(response.urljoin(url),callback=self.parse_club)

    def parse_club(self,response):
        season_id=response.url.split('=')[-1]
        league_name=response.url.split('/')[3]
        lst_club=response.css("td.hauptlink.no-border-links.hide-for-small.hide-for-pad a.vereinprofil_tooltip::text").extract()
        league_size=len(lst_club)
        league_level=response.css(".profilheader tr:nth-child(1) td::text").extract()[0].strip()
        country_name=response.css(".profilheader tr:nth-child(1) td::text").extract()[1].strip()

        # store data
        # dct_league_club=dict(league_name=league_name,season_id=season_id,league_size=league_size,club=lst_club)
        # dct_league_size=dict(league_name=league_name,season_id=season_id,league_size=league_size,league_level=league_level,country_name=country_name)

        # store detail club list of each league each season
        for club in lst_club:
            dct_league_club = dict(league_name=league_name, season_id=season_id,country_name=country_name, club=club,league_level=league_level)
            yield dct_league_club
        # store league size info to csv file by call 'scrapy crawl leagues_size -o leagues_size_change.csv'
        # yield dct_league_size


