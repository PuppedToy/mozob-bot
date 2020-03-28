import requests
import threading
import random
import asyncio

TFT_CLASSES = ['Inferno', 'Light', 'Poison', 'Crystal', 'Desert', 'Ocean', 'Shadow', 'Electric', 'Lunar', 'Mountain', 'Woodland', 'Cloud', 'Glacial', 'Steel', 'Alchemist', 'Avatar', 'Ranger', 'Mage', 'Mystic', 'Soulbound', 'Summoner', 'Assasain', 'Berserker', 'Predator', 'Warden', 'Blademaster', 'Druid']

from bot.queries import Connection
from bot.invisibleFriend import InvisibleFriend
from bot.russeRoulette import RusseRoulette
connection = Connection()

PRODUCTION_INTERVAL = 60*60 # 1 product each hour
INVISIBLE_FRIEND_AUTODESTRUCTION_TIME = 60*60*24*7 # cancel invisible friend after a week
RUSSE_ROULETTE_AUTODESTRUCTION_TIME = 60*60*4 # cancel russe roulettes after 4 hours
# PRODUCTION_INTERVAL = 10 # 1 product each 10s
#     `&invisible_friend [(p)ublic|(s)ecret]`: Crea una sala de amigo invisible. Si se elige `secret`, los regalos no se publicarán en el canal.

factories = connection.getFactories()
inventories = connection.getInventories()
invisibleFriends = []
russeRoulettes = []

class Command:

    @classmethod
    def hello(cls, authorId):
        return 'Saludos, <@{0}>.'.format(authorId)

    @classmethod
    def help(cls):
        return '''Lista de comandos:
    `&help`: Te muestro este mensaje entero
    `&hello`: Te saludo
    `&factory create <Nombre fabrica>&<Nombre producto>`: Construye una nueva fábrica.
    `&factory delete`: Si tienes una fábrica, LA DESTRUYES PARA SIEMPRE.
    `&factory list`: Muestra la lista de fábricas existentes.
    `&inventory`: Muestra tu inventario
    `&invisible_friend`: Genera una sala de amigo invisible. Para saber más, puedes usar `&invisible_friend help`.
    `&russe_roulette [capacidad_arma] [numero_balas]`: Crea una sala de ruleta rusa. Por defecto, se asume un arma con 6 huecos y 1 bala.
    `&tft random_classes`: Genera dos clases (clases/orígenes) aleatorios para jugar tu próximo TFT
    `&tft hidden_quest help`: Muestra la ayuda de la modalidad de **TFT Hidden Quest**
    `&tft hidden_quest commands`: Muestra todos los comandos de **TFT Hidden Quest**
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

    @classmethod
    def alaputa(cls):
        a = random.random()
        if a < 0.5:
            frase = "A la puta tú"
        else:
            frase = "Coincido, a la puta con todo"
        return frase

    #ADD BY FranciscoJavierValero 28/3/20 2:21
    @classmethod
    def roll(cls, dice: str):
        parts = dice.lower().split("d")
        d_number = parts[0]
        sides = part[1]
        results = [random.randint(1,sides) for i in range(d_number)]
        return str(results)
    #END ADD

    @classmethod
    def tftRandomClasses(cls, sender):
        return "<@{0}>, en la próxima partida de TFT vas a ir a {1} y {2}. Buena suerte!".format(sender, random.choice(TFT_CLASSES), random.choice(TFT_CLASSES))

    @classmethod
    def tftHiddenQuestHelp(cls):
        return ['''TFT Hidden Quest es una modalidad de TFT que consiste en que todos los que vayan a participar en un TFT reciben una mission secreta (los jugadores tienen 3 rerolls de misión). Durante la próxima partida, los jugadores están obligados a cumplir su misión secreta. Gana el jugador que haya cumplido su misión secreta y se haya posicionado más alto en la partida de TFT.
Lista de pasos para jugar este modo:
    
    1: Un jugador debe crear una sala de TFT Hidden Quest mediante `&tft hidden_quest create [numero_rerolls] [chivarse_de_misiones_descartadas (y/n)]`. Los parámetros son opcionales. Si no se pone ninguno, se asume el comando por defecto `&tft hidden_quest create 3 y`.
    2: El bot responderá un mensaje con un ID de sala. Por ejemplo: `patata-18`.
    3: Todos los jugadores que deseen participar deberán ejecutar: `&tft hidden_quest join <id_sala>`. Por ejemplo: `&tft hidden_quest join patata-18`.
    4: Hablaré en privado al jugador que ha entrado mostrándole su misión secreta.
    5: A quien no le guste su misión secreta, si tiene rerolls disponibles, podrá utilizar `&tft hidden_quest reroll`. En ese caso, descartaré su misión y le daré una nueva.''','''    6: Cuando el jugador esté satisfecho con su misión, deberá enviar `&tft hidden_quest ready`. Si se gasta todos los rerolls, se le considerará preparado. Este comando es irreversible (de momento).
    7: Cuando todos estén listos, el creador de la sala deberá introducir `&tft hidden_quest start`. Si se llega a 8 jugadores preparados, la partida comenzará automáticamente.
    8: Los jugadores disfrutarán (o no) de su partida de TFT.
    9: Cuando un jugador acabe su partida, deberá reportar su resultado: `&tft hidden_quest end <posicion_partida> <mision_cumplida (y/n)>`. Por ejemplo, si Jacobo ha acabado su partida 5º y ha acabado su misión, Jacobo deberá poner `&tft hidden_quest end 5 y`. Si te equivocas escribiendo este comando, puedes volver a poner el comando corregido.
    10: Cuando hayan acabado todos los jugadores, os comentaré quién ha ganado y revelaré cuáles eran las misiones secretas. También me chivaré de las misiones secretas descartadas.

    En cualquier momento, cualquier jugador puede poner `&tft hidden_quest status` para que os cuente el estado completo de la sala.
''']

    @classmethod
    def tftHiddenQuestCommands(cls):
        return '''Lista de comandos de **TFT Hiden Quests**:
    `&tft hidden_quest help`: Te enseño cómo funciona **TFT Hidden Quests** en detalle. Atajos: `&tft hq h`
    `&tft hidden_quest commands`: Te enseño este mismo mensaje. Atajos: `&tft hq cmd`
    `&tft hidden_quest create [numero_rerolls (por defecto 3)] [mostrar_misiones_descartadas (y/n) (por defecto y)]`: Crea una nueva sala de TFT Hidden Quest y muestra su ID. Atajos: `&tft hq c`
    `&tft hidden_quest destroy`: Si eres el creador de una sala, puedes usar este comando para destruir la sala en la que estás.
    `&tft hidden_quest join <id_sala>`: Te unes a la sala _id_sala_. Te envío por privado tu misión secreta. Atajos: `&tft hq j`
    `&tft hidden_quest leave`: Te vas de la sala en la que estás. Atajos: `&tft hq lv`
    `&tft hidden_quest reroll`: Gastas un reroll y te asigno una misión secreta nueva. Atajos: `&tft hq rr`, `&tft hq rrl`
    `&tft hidden_quest ready`: Aceptas tu misión secreta y marcas que estás listo para jugar a TFT. Atajos: `&tft hq rd`, `&tft hq rdy`
    `&tft hidden_quest start`: El creador podrá utilizar este comando para comenzar la partida de TFT cuando todos hayan marcado que están listos. Atajos: `&tft hq sta`, `&tft hq str`
    `&tft hidden_quest end <posición> <he_completado_mi_mision (y/n)>`: Cuando un jugador acaba su partida, deberá poner este comando identificando en que _posición_ ha quedado y si ha completado su misión (**_y_**) o no (**_n_**). Atajos: `&tft hq e`
    `&tft hidden_quest status`: Muestra el estado de la sala en la que estás. Atajos: `&tft hq s`
'''

    @classmethod
    def invisibleFriendHelp(cls):
        return ['''Las salas de amigo invisible permiten organizar un intercambio de mensajes entre un grupo de personas de forma que cada persona reciba otra a la que regalar. Puedes generar una sala sin opciones, lo cual hará totalmente pública toda la información (quién regala a quién y qué se regala). Para hacer privados esos datos, se dispone de las siguientes opciones.
Opciones disponibles:
    `secret_target` o `st`: El regalador no sabe a quién regala hasta que todos los regalos se han repartido. Si esta opción no se selecciona, el regalador conocerá su regalado desde el momento en que empieza el amigo invisible.
    `secret_giver` o `sg`: Nadie sabe quién quien le ha regalado. Si esta opción no está activada, se publicará quién regala a quién excepto si se utiliza `private_giver`.
    `private_giver` o `pg`: Cada persona sabe quién le ha regalado, pero no se publicará en el canal. Si no se selecciona esta opción, se publicará quién ha regalado a quién. Si se activa la opción `secret_giver` esta opción se ignora.
    `private_present` o `pp`: El regalo solo lo conocen las personas involucradas. Si esta opción no se selecciona, los regalos se publicarán en el canal cuando todos hayan enviado su regalo.
.
.
''',
        '''Se pueden combinar las opciones entre ellas. Aquí se listan todas las posibles combinaciones:
    `&invisible_friend st sg`: nadie sabrá a quién está regalando quién le regala. Pero el regalo será público y todos conocerán lo que ha recibido cada uno.
    `&invisible_friend st pg`: nadie sabrá a quién está regalando y no sé publicará quién regala a quién, pero cada persona conocerá quién le ha regalado. Además, los regalos que ha recibido cada uno se harán públicos.
    `&invisible_friend st pp`: nadié sabrá a quién está regalando y los regalos que se hagan no se publicarán. Sin embargo, una vez hechos los regalos, se publicará quién ha regalado a quién.
    `&invisible_friend sg pg`: `sg` sobreescribe siempre a `pg`.
    `&invisible_friend sg pp`: nadie sabe quién le ha regalado y los regalos no se publicarán, pero cada uno sabe a quién regala.
    `&invisible_friend pg pp`: no se publica ni quién ha regalado a quién ni los regalos, pero cada uno sabe tanto a quién regala como quién le ha regalado.
    `&invisible_friend st sg pg`: es equivalente a `&invisible_friend st sg`.
    `&invisible_friend st sg pp`: nadie sabe a quién regala ni quién le ha regalado. Además los regalos no se publicarán.
    `&invisible_friend st pg pp`: nadie sabe a quién regala. Además, no se publicarán ni los regalos ni quién regala a quién, pero cada persona sabe quién le ha regalado.
''']

    @classmethod
    async def invisibleFriendAutodestruction(cls, invisibleFriend):
        await asyncio.sleep(INVISIBLE_FRIEND_AUTODESTRUCTION_TIME)
        if invisibleFriend in invisibleFriends:
            invisibleFriend.cancel()
            invisibleFriends.remove(invisibleFriend)

    @classmethod
    async def russeRouletteAutodestruction(cls, russeRoulette):
        await asyncio.sleep(RUSSE_ROULETTE_AUTODESTRUCTION_TIME)
        if russeRoulette in russeRoulettes:
            russeRoulette.cancel()
            russeRoulettes.remove(russeRoulette)

    @classmethod
    def invisibleFriend(cls, message, isSecretTarget, isSecretGiver, isPrivateGiver, isPrivatePresent):
        invisibleFriend = InvisibleFriend(message, isSecretTarget, isSecretGiver, isPrivateGiver, isPrivatePresent)
        invisibleFriends.append(invisibleFriend)
        asyncio.ensure_future(Command.invisibleFriendAutodestruction(invisibleFriend))

    @classmethod
    def searchInvisibleFriend(cls, messageId):
        for invisibleFriend in invisibleFriends:
            if invisibleFriend.message.id == messageId:
                return invisibleFriend
        return None

    @classmethod
    def searchInvisibleFriendByUser(cls, userId):
        for invisibleFriend in invisibleFriends:
            if invisibleFriend.started and not invisibleFriend.revealed and userId in invisibleFriend.users:
                return invisibleFriend
        return None

    @classmethod
    def sendSettingsInvisibleFriend(cls, messageId, user):
        invisibleFriend = Command.searchInvisibleFriend(messageId)
        if invisibleFriend:
            invisibleFriend.sendSettings(user)

    @classmethod
    def joinInvisibleFriend(cls, messageId, user):
        invisibleFriend = Command.searchInvisibleFriend(messageId)
        if invisibleFriend:
            invisibleFriend.addUser(user)

    @classmethod
    def startInvisibleFriend(cls, messageId, user):
        invisibleFriend = Command.searchInvisibleFriend(messageId)
        if invisibleFriend:
            invisibleFriend.start(user)

    @classmethod
    def givePresentInvisibleFriend(cls, message):
        invisibleFriend = Command.searchInvisibleFriendByUser(message.author.id)
        if invisibleFriend:
            invisibleFriend.givePresent(message.author, message.content)
            if invisibleFriend.revealed:
                invisibleFriends.remove(invisibleFriend)

    @classmethod
    def leaveInvisibleFriend(cls, messageId, user):
        invisibleFriend = Command.searchInvisibleFriend(messageId)
        if invisibleFriend:
            invisibleFriend.removeUser(user)

    @classmethod
    def russeRoulette(cls, channel, size, bullets):
        russeRoulette = RusseRoulette(channel, size, bullets)
        russeRoulettes.append(russeRoulette)
        asyncio.ensure_future(Command.russeRouletteAutodestruction(russeRoulette))

    @classmethod
    def findRusseRoulette(cls, messageId):
        for russeRoulette in russeRoulettes:
            if russeRoulette.bullets > 0 and russeRoulette.message.id == messageId:
                return russeRoulette
        return None

    @classmethod
    def shootRusseRoulette(cls, messageId, user):
        russeRoulette = Command.findRusseRoulette(messageId)
        if russeRoulette is not None:
            russeRoulette.shoot(user)
            if russeRoulette.bullets == 0:
                russeRoulettes.remove(russeRoulette)

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
