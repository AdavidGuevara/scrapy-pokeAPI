import scrapy


class Pokemon(scrapy.Item):
    name = scrapy.Field()
    forms = scrapy.Field()
    base_exp = scrapy.Field()
    moves = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    abilities = scrapy.Field()
    game_indices = scrapy.Field()
    hp = scrapy.Field()
    attack = scrapy.Field()
    defence = scrapy.Field()
    sp_attack = scrapy.Field()
    sp_defence = scrapy.Field() 
    speed = scrapy.Field()
