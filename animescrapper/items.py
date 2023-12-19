import scrapy

class AnimeItem(scrapy.Item):
    Name = scrapy.Field()
    Type = scrapy.Field()
    Episodes = scrapy.Field()
    Status = scrapy.Field()
    Aired = scrapy.Field()
    Premiered = scrapy.Field()
    Broadcast = scrapy.Field()
    Producers = scrapy.Field()
    Licensors = scrapy.Field()
    Studios = scrapy.Field()
    Genres = scrapy.Field()
    Duration = scrapy.Field()
    Rating = scrapy.Field()
    Members = scrapy.Field()
    Favorites = scrapy.Field()

