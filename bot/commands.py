import requests

factories = {}

class Command:

    @classmethod
    def hello(cls, authorId):
        return 'Saludos, <@{0}>.'.format(authorId)

    @classmethod
    def help(cls):
        return '''Lista de comandos:
    &help: Te muestro este mensaje entero
    &hello: Te saludo
    &leet <mensaje>: Mi código venía con esta puta mierda que todavía no he quitado.
'''

    @classmethod
    def createFactory(cls, owner, name, product):
        if owner in factories:
            return "Parece que posees la fábrica \"{0}\" de {1}s. Solo puedes tener una fábrica!!!".format(factories[owner]["name"], factories[owner]["product"])
        factories[owner] = {
            "name": name,
            "product": product
        }
        return "He creado tu fábrica \"{0}\" de {1}s correctamente.".format(name, product)

    # Converts user-input to 1337 5p34k.
    @classmethod
    def leet_speak(cls, in_string):
        replacement_characters = (('l', '1'), ('e', '3'), ('a', '4'), ('s', '5'), ('t', '7'), ('o', '0'))
        out_string = in_string.lower()
        for old, new in replacement_characters:
            out_string = out_string.replace(old, new)

        return out_string
