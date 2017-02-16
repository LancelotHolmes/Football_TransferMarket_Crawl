import scrapy

class LeagueSpider(scrapy.Spider):
    name='leagues'

    # def start_requests(self):
    #     urls=[
    #         'http://www.transfermarkt.co.uk/wettbewerbe/europa?page=1',
    #         'http://www.transfermarkt.co.uk/wettbewerbe/europa?page=2',
    #         'http://www.transfermarkt.co.uk/wettbewerbe/europa?page=3',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url,callback=self.parse)
    start_urls=[ # start from the leagues website divided by continents
        # 'http://www.transfermarkt.co.uk/wettbewerbe/europa?page=1',
        # 'http://www.transfermarkt.co.uk/wettbewerbe/europa?page=2',
        # 'http://www.transfermarkt.co.uk/wettbewerbe/europa?page=3',
        'http://www.transfermarkt.co.uk/wettbewerbe/europa?page=1',
        'http://www.transfermarkt.co.uk/wettbewerbe/asien?page=1',
        'http://www.transfermarkt.co.uk/wettbewerbe/amerika?page=1',
        'http://www.transfermarkt.co.uk/wettbewerbe/afrika?page=1',
    ]

    def parse(self,response):
        # download the raw html page of compact league info
        # page=response.url.split('=')[-1]
        # continent = response.url.split('/')[-1].split('?')[-2]
        # filename = '%s_leagues_%s.html' % (continent, page)
        # with open(filename,'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s'% filename)

        lst_league=self.get_league_url(response)
        # follow links to specific leagues page
        for href in lst_league:
            yield scrapy.Request(response.urljoin(href),callback=self.parse_league)

        # follow pagination links
        next_page= response.css("li.naechste-seite a::attr(href)").extract_first()
        if next_page is not None:
            next_page=response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse)

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

        # download the raw html page of league info of each season
        # filename = '%s_%s.html' % (league_name, season_id)
        # with open(filename,'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s'% filename)

        # store data
        dct_league_club=dict(league_name=league_name,season_id=season_id,league_size=league_size,club=lst_club)
        dct_league_size=dict(league_name=league_name,season_id=season_id,league_size=league_size)
        # store league size info to csv file bu call 'scrapy crawl leagues -o leagues_size.csv'
        yield dct_league_size


