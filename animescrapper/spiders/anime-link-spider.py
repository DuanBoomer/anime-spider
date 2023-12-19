import scrapy
from animescrapper.items import AnimeItem
# from scrapy.utils.project import data_path
# import os

class LinkSpider(scrapy.Spider):
    name = 'anime-spider'
    # page = 0
    page = 13100
    start_urls = [f'https://myanimelist.net/topanime.php?limit={page}']

    # saving progress
    # path = data_path('link.txt')
    # initialize file if it does not exist
    # if not os.path.exists(path):
    #     with open(path, 'w') as file:
    #         file.write(start_urls[0])
    # read from the file
    # else:
    #     with open(path, 'r') as file:
    #         start_urls = [file.read()]

    def parse(self, response):
        # get all links for on a anime page and follow them
        for anime in response.css('td.title.al.va-t.word-break'):
            link = anime.css(
                'h3.hoverinfo_trigger.fl-l.fs14.fw-b.anime_ranking_h3 a::attr(href)')
            yield response.follow(link.get(), callback=self.parse_anime)

        next_page_href = response.css('a.link-blue-box.next::attr(href)').get()

        # if next page button exists follow it and save it in progress
        if next_page_href is not None:
            next_page = 'https://myanimelist.net/topanime.php' + next_page_href
            # path = data_path('link.txt')
            # with open(path, 'w') as file:
            #     file.write(next_page)
            yield response.follow(next_page, callback=self.parse)

        # if next page button does not exist remove the progress file(.scrapy/link.txt)
        # else:
        #     path = data_path('link.txt')
        #     os.remove(path)

    # get details from the anime page
    def parse_anime(self, response):
        anime_item = AnimeItem()

        # get name from title
        anime_item['Name'] = response.css('h1.title-name strong::text').get()

        # find all other fields from the sidebar
        ref_string = 'Type:Episodes:Status:Aired:Premiered:Broadcast:Producers:Licensors:Studios:Genres:Duration:Rating:Members:Favorites:'
        for spaceit_pads in response.css('div.spaceit_pad'):
            dark_text = spaceit_pads.css('span.dark_text::text').get()
            if dark_text is None:
                dark_text = 'None'
            if dark_text == 'Genre:':
                dark_text = 'Genres:'
            if dark_text in ref_string:
                anime_item[dark_text[:-1]] = list(set([x for x in list(map(
                    str.strip, spaceit_pads.css('::text').getall())) if x != '' and x != ','][1:]))
        yield anime_item
