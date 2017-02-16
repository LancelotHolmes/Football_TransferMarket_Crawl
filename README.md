# Football_TransferMarket_Crawl

**using scrapy to crawl data from a football transfer market website**

## Aim: crawl data from a football player tranfer market website named [transfermarkt][1] to do some research.

## Tools: 
* Python v2.7
* [Scrapy][2]

## Notes for Files: 
* ../crawl_league/crawl_league:
 * settings: set to deal with the anti-crawl system
 * rotate_useragent.py: method to change the user agent info dynamically to deal with anti-crawl system,set in the settings.
* ../crawl_league/crawl_league/spiders:
 * ContinentCountrySpider.py: spider simply crawl the country info of different continent according to the website.
 * league_spider.py: spider to crawl the league size of different country varies of different seasons
 * LeagueSizeSpider.py: spider to crawl league with detail clubs info.

## Log:  
* crawl the detail clubs of different leagues during different seasons


[1]: http://www.transfermarkt.co.uk
[2]: https://scrapy.org/
