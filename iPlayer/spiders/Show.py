import scrapy
from scrapy import Selector
from scrapy.http import Response


class ShowSpider(scrapy.Spider):
    name = "shows"

    def start_requests(self):
        urls = [
            'https://www.bbc.co.uk/iplayer/episodes/b00mjlxv/merlin',
            'https://www.bbc.co.uk/iplayer/episodes/b006mf4b/spooks'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def get_episodes(self, response: Response):
        for episode in response.css('ul.gel-layout li'):
            print(f"https://bbc.co.uk/{episode.css('a').attrib['href']}")
            yield {
                'url': f"https://bbc.co.uk{episode.css('a').attrib['href']}"
            }

    def parse(self, response: Response):
        series: Selector = response.css('nav.series-nav ul')
        yield from self.get_episodes(response)
        # Find all season links
        for link in series.css('li a'):
            yield scrapy.Request("https://bbc.co.uk" + link.attrib['href'], self.get_episodes)
