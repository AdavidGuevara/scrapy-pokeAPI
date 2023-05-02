from .spiders.pokemons import PokemonsSpider
from itemadapter import ItemAdapter
from dotenv import load_dotenv
from .items import Pokemon
import mysql.connector
import os

load_dotenv()


class PokeapiPipeline:
    def __init__(self):
        self.create_conn()
        self.create_table()

    def create_conn(self):
        self.conn = mysql.connector.connect(
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASS"],
            host=os.environ["MYSQL_HOST"],
            database=os.environ["MYSQL_DB"],
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS pokemons;""")
        self.curr.execute(
            """
            CREATE TABLE pokemons (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(100),
            forms INT,
            base_exp INT,
            moves INT,
            height INT,
            weight INT,
            abilities INT,
            game_indices INT,
            hp INT,
            attack INT,
            defence INT,
            sp_attack INT,
            sp_defence INT,
            speed INT,
            PRIMARY KEY (id));
            """
        )

    def store_items(self, item: Pokemon):
        try:
            base_exp = item["base_exp"][0]
        except:
            base_exp = 0    
        self.curr.execute(
            """INSERT INTO pokemons (name, forms, base_exp, moves, height, weight, abilities, game_indices, hp, attack, defence, sp_attack, sp_defence, speed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
            (
                item["name"][0],
                item["forms"][0],
                base_exp,
                item["moves"][0],
                item["height"][0],
                item["weight"][0],
                item["abilities"][0],
                item["game_indices"][0],
                item["hp"][0],
                item["attack"][0],
                item["defence"][0],
                item["sp_attack"][0],
                item["sp_defence"][0],
                item["speed"][0],
            ),
        )
        self.conn.commit()

    def process_item(self, item: Pokemon, spider: PokemonsSpider):
        self.store_items(item)
        return item
