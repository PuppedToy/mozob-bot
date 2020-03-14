import requests
import threading
import random

TFT_CLASSES = ['Inferno', 'Light', 'Poison', 'Crystal', 'Desert', 'Ocean', 'Shadow', 'Electric', 'Lunar', 'Mountain', 'Woodland', 'Cloud', 'Glacial', 'Steel', 'Alchemist', 'Avatar', 'Ranger', 'Mage', 'Mystic', 'Soulbound', 'Summoner', 'Assasain', 'Berserker', 'Predator', 'Warden', 'Blademaster', 'Druid']

from bot.queries import Connection
connection = Connection()

PRODUCTION_INTERVAL = 60*60 # 1 product each hour
# PRODUCTION_INTERVAL = 10 # 1 product each 10s

factories = connection.getFactories()
inventories = connection.getInventories()

class Command:

    @classmethod
    def hello(cls, authorId):
        return 'Saludos, <@{0}>.'.format(authorId)

    @classmethod
    def help(cls):
        return '''Lista de comandos:
    `&help`: Te muestro este mensaje entero
    `&hello`: Te saludo
    `&leet <mensaje>`: Mi código venía con esta puta mierda que todavía no he quitado.
    `&factory create <Nombre fabrica>&<Nombre producto>`: Construye una nueva fábrica.
    `&factory delete`: Si tienes una fábrica, LA DESTRUYES PARA SIEMPRE.
    `&factory list`: Muestra la lista de fábricas existentes.
    `&inventory`: Muestra tu inventario
    `&tft random_classes`: Genera dos clases (clases/orígenes) aleatorios para jugar tu próximo TFT
'''

    @classmethod
    def createFactory(cls, owner, name, product):
        if owner in factories:
            return "Parece que posees la fábrica \"{0}\" de {1}s. Solo puedes tener una fábrica!!! Si no te gusta tu fábrica, la puedes destruir con `factory delete`. Pero cuidado, que no hay vuelta atrás.".format(factories[owner]["name"], factories[owner]["product"])
        factories[owner] = {
            "name": name,
            "product": product
        }
        connection.insertFactory(owner, name, product)
        return "He creado tu fábrica \"{0}\" de {1}s correctamente.".format(name, product)

    @classmethod
    def listFactory(cls):
        response = ""
        for owner, factory in factories.items():
            response += "- <@{0}>: fábrica \"{1}\" de {2}s.\n".format(owner, factory["name"], factory["product"])
        if response == "":
            response = "No existe ninguna fábrica por el momento."
        return response

    @classmethod
    def deleteFactory(cls, owner):
        if not owner in factories:
            return "No puedes destruir algo que no tienes. Construye una fábrica con `factory create` para poder destruirla."
        else:
            response = "BUUUM!!! Adiós para siempre, fábrica \"{0}\"".format(factories[owner]["name"])
            del factories[owner]
            connection.deleteFactory(owner)
            return response

    @classmethod
    def inventory(cls, owner):
        if not owner in inventories:
            return "Tienes la mochila vacía."
        response = ""
        for item, amount in inventories[owner].items():
            if amount > 0:
                response += "\t- {0}s: {1}\n".format(item, str(amount))
        return response

    # Converts user-input to 1337 5p34k.
    @classmethod
    def leet_speak(cls, in_string):
        replacement_characters = (('l', '1'), ('e', '3'), ('a', '4'), ('s', '5'), ('t', '7'), ('o', '0'))
        out_string = in_string.lower()
        for old, new in replacement_characters:
            out_string = out_string.replace(old, new)

        return out_string

    @classmethod
    def tftRandomClasses(cls, sender):
        return "<@{0}>, en la próxima partida de TFT vas a ir a {1} y {2}. Buena suerte!".format(sender, random.choice(TFT_CLASSES), random.choice(TFT_CLASSES))


def produce():
    for owner, factory in factories.items():
        if not owner in inventories:
            inventories[owner] = {}
        item = factory["product"]
        if not item in inventories[owner]:
            inventories[owner][item] = 1
            connection.createInventory(owner, item, inventories[owner][item])
        else:
            inventories[owner][item] += 1
            connection.updateInventory(owner, item, inventories[owner][item])

    threading.Timer(PRODUCTION_INTERVAL, produce).start()
threading.Timer(PRODUCTION_INTERVAL, produce).start()
