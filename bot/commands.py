import requests
import threading

PRODUCTION_INTERVAL = 60*60 # 1 product each hour

inventories = {}
factories = {}

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
'''

    @classmethod
    def createFactory(cls, owner, name, product):
        if owner in factories:
            return "Parece que posees la fábrica \"{0}\" de {1}s. Solo puedes tener una fábrica!!! Si no te gusta tu fábrica, la puedes destruir con `factory delete`. Pero cuidado, que no hay vuelta atrás.".format(factories[owner]["name"], factories[owner]["product"])
        factories[owner] = {
            "name": name,
            "product": product
        }
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

def produce():
    for owner, factory in factories.items():
        if not owner in inventories:
            inventories[owner] = {}
        item = factory["product"]
        if not item in inventories[owner]:
            inventories[owner][item] = 1
        else:
            inventories[owner][item] += 1
    threading.Timer(PRODUCTION_INTERVAL, produce).start()
threading.Timer(PRODUCTION_INTERVAL, produce).start()
