from scrapy.loader import ItemLoader
from ..items import Pokemon
import scrapy

base_url = "https://pokeapi.co/api/v2/pokemon?offset={}&limit=20"


class PokemonsSpider(scrapy.Spider):
    name = "pokemons"
    allowed_domains = ["pokeapi.co"]
    start_urls = [base_url.format(0)]
    custom_settings = {
        "FEED_URI": "pokemons.json",
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
    }

    def parse_pokemon(self, response):
        data = response.json()
        item = ItemLoader(Pokemon(), data)
        item.add_value("name", data["name"])
        item.add_value("forms", len(data["forms"]))
        item.add_value("base_exp", data["base_experience"])
        item.add_value("moves", len(data["moves"]))
        item.add_value("height", data["height"])
        item.add_value("weight", data["weight"])
        item.add_value("abilities", len(data["abilities"]))
        item.add_value("game_indices", len(data["game_indices"]))
        item.add_value("hp", data["stats"][0]["base_stat"])
        item.add_value("attack", data["stats"][1]["base_stat"])
        item.add_value("defence", data["stats"][2]["base_stat"])
        item.add_value("sp_attack", data["stats"][3]["base_stat"])
        item.add_value("sp_defence", data["stats"][4]["base_stat"])
        item.add_value("speed", data["stats"][5]["base_stat"])
        yield item.load_item()

    def parse(self, response):
        data = response.json()

        for result in data["results"]:
            yield scrapy.Request(result["url"], callback=self.parse_pokemon)

        if data["next"]:
            yield scrapy.Request(data["next"], callback=self.parse)
