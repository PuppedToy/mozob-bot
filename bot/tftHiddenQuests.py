import random
import re
import numpy as np
import asyncio

TFT_HIDDEN_QUEST_VERSION = '1.01'
AUTODESTRUCTION_TIME = 60*60*4 # Autodestruction after 4 hours

TFT_CLASSES = [
    {
        'name': 'Ranger',
        'props': [2, 4, 6],
        'type': 'class'
    },
    {
        'name': 'Alchemist',
        'props': [1],
        'type': 'class'
    },
    {
        'name': 'Avatar',
        'props': [1],
        'type': 'class'
    },
    {
        'name': 'Mage',
        'props': [3, 6],
        'type': 'class'
    },
    {
        'name': 'Mystic',
        'props': [2, 4],
        'type': 'class'
    },
    {
        'name': 'Assassin',
        'props': [3, 6],
        'type': 'class'
    },
    {
        'name': 'Berserker',
        'props': [3, 6],
        'type': 'class'
    },
    {
        'name': 'Blademaster',
        'props': [2, 4, 6],
        'type': 'class'
    },
    {
        'name': 'Predator',
        'props': [3],
        'type': 'class'
    },
    {
        'name': 'Summoner',
        'props': [3, 6],
        'type': 'class'
    },
    {
        'name': 'Alchemist',
        'props': [1],
        'type': 'class'
    },
    {
        'name': 'Warden',
        'props': [2, 4, 6],
        'type': 'class'
    },
    {
        'name': 'Soulbound',
        'props': [2],
        'type': 'class'
    },
    {
        'name': 'Druid',
        'props': [2],
        'type': 'class'
    },
    {
        'name': 'Inferno',
        'props': [3, 6],
        'type': 'origin'
    },
    {
        'name': 'Poison',
        'props': [3],
        'type': 'origin'
    },
    {
        'name': 'Shadow',
        'props': [3, 6],
        'type': 'origin'
    },
    {
        'name': 'Crystal',
        'props': [2],
        'type': 'origin'
    },
    {
        'name': 'Desert',
        'props': [2, 4],
        'type': 'origin'
    },
    {
        'name': 'Ocean',
        'props': [2, 4],
        'type': 'origin'
    },
    {
        'name': 'Electric',
        'props': [2, 3],
        'type': 'origin'
    },
    {
        'name': 'Glacial',
        'props': [2, 4],
        'type': 'origin'
    },
    {
        'name': 'Light',
        'props': [3, 6],
        'type': 'origin'
    },
    {
        'name': 'Lunar',
        'props': [2],
        'type': 'origin'
    },
    {
        'name': 'Mountain',
        'props': [2],
        'type': 'origin'
    },
    {
        'name': 'Cloud',
        'props': [2],
        'type': 'origin'
    },
    {
        'name': 'Woodland',
        'props': [3],
        'type': 'origin'
    },
    {
        'name': 'Steel',
        'props': [2],
        'type': 'origin'
    },
]
TFT_CLASSES_NAMES = list(map(lambda el: el['name'], TFT_CLASSES))

BASIC_ITEMS = [
    '<:BFSword:689507540651999246> B.F. Sword',
    '<:NeedlesslyLargeRod:689507541478277146> Needlessly Large Rod',
    '<:RecurveBow:689507541129887804> Recurve Bow',
    '<:SparringGloves:689507540945469440> Sparring Gloves',
    '<:TearoftheGoddess:689507541083750407> Tear of the Goddess',
    '<:ChainVest:689507540740210739> Chain Vest',
    '<:GiantsBelt:689507540689617000> Giant\'s Belt',
    '<:NegatronCloak:689507541235138623> Negatron Cloak'
]
UPGRADED_ITEMS = [
    '<:Bloodthirster:689507540677165084> Bloodthirster',
    '<:HandofJustice:689507541096726555> Hand of Justice',
    '<:JeweledGauntlet:689507541079818424> Jeweled Gauntlet',
    '<:LastWhisper:689507541189001313> Last Whisper',
    '<:LocketoftheIronSolari:689507540823834681> Locket of the Iron Solari',
    '<:LudensEcho:689507540991737915> Luden\'s Echo',
    '<:RabadonsDeathcap:689507541163704428> Rabadon\'s Deathcap',
    '<:RapidFirecannon:689507540954120308> Rapid Firecannon',
    '<:Redemption:689507541012709471> Redemption',
    '<:RunaansHurricane:689507541155315804> Runaan\'s Hurricane',
    '<:StatikkShiv:689507540987412541> Statikk Shiv',
    '<:BrambleVest:689507540631158788> Bramble Vest',
    '<:Deathblade:689507540647804973> Deathblade',
    '<:DragonsClaw:689507541096595467> Dragon\'s Claw',
    '<:GuinsoosRageblade:689507541029486594> Guinsoo\'s Rageblade',
    '<:Hush:689507541180350544> Hush',
    '<:IonicSpark:689507541129887803> Ionic Spark',
    '<:Quicksilver:689507541113241793> Quicksilver',
    '<:RedBuff:689507541129887774> Red Buff',
    '<:SpearofShojin:689507541180481648> Spear of Shojin',
    '<:TitansResolve:689507541138276362> Titan\'s Resolve',
    '<:WarmogsArmor:689507541612363827> Warmog\'s Armor',
    '<:FrozenHeart:689507540546879608> Frozen Heart',
    '<:GiantSlayer:689507541129887929> Giant Slayer',
    '<:HextechGunblade:689507541142470701> Hextech Gunblade',
    '<:ZekesHerald:689507541134213120> Zeke\'s Herald',
    '<:IceborneGauntlet:689507541134213213> Iceborne Gauntlet',
    '<:SwordBreaker:689507541201191047> Sword Breaker',
    '<:TitanicHydra:689507540744142857> Titanic Hydra',
    '<:TrapClaw:689507541105115236> Trap Claw'
]

CHAMPIONS_1 = ['Diana', 'Ivern', 'Kog\'Maw', 'Leona', 'Maokai', 'Nasus', 'Ornn', 'Renekton', 'Taliyah', 'Vayne', 'Vladimir', 'Warwick', 'Zyra']
CHAMPIONS_2 = ['Braum', 'Jax', 'LeBlanc', 'Malzahar', 'Neeko', 'Rek\'Sai', 'Senna', 'Skarner', 'Syndra', 'Thresh', 'Varus', 'Volibear', 'Yasuo']
CHAMPIONS_3 = ['Aatrox', 'Azir', 'Dr. Mundo', 'Ezreal', 'Karma', 'Kindred', 'Nautilus', 'Nocturne', 'Qiyana', 'Sion', 'Sivir', 'Soraka', 'Veigar']
CHAMPIONS_4 = ['Annie', 'Ashe', 'Brand', 'Janna', 'Kha\'Zix', 'Lucian', 'Malphite', 'Olaf', 'Twitch', 'Yorick']
CHAMPIONS_5 = ['Amumu', 'Master Yi', 'Nami', 'Singed', 'Taric', 'Zed']

CHAMPIONS_WITH_PRICE = np.concatenate([
    list(map(lambda el: '[1] ' + el, CHAMPIONS_1)),
    list(map(lambda el: '[2] ' + el, CHAMPIONS_2)),
    list(map(lambda el: '[3] ' + el, CHAMPIONS_3)),
    list(map(lambda el: '[4] ' + el, CHAMPIONS_4)),
    list(map(lambda el: '[5] ' + el, CHAMPIONS_5))
])

IDS = list(map(lambda el: re.sub(r'[^a-z]', '', el.lower()), np.concatenate([
    ['alfalfa', 'almorta', 'guisante', 'frijol', 'garbanzo', 'habas', 'ejote', 'lenteja', 'altramuz', 'cacahuetes', 'soja', 'arveja', 'mungo', 'almendra', 'anacardo', 'avellana', 'castaña', 'gevuina', 'nuece', 'piñone', 'pistacho', 'calabaza', 'girasol', 'pipas', 'aguacate', 'albaricoque', 'piña', 'arandano', 'banana', 'cereza', 'ciruela', 'coco', 'damasco', 'durazno', 'frambuesa', 'fresa', 'frutilla', 'guinda', 'granada', 'grosella', 'higo', 'kiwi', 'lima', 'limon', 'mandarina', 'mango', 'manzana', 'maracuya', 'melocoton', 'melon', 'membrillo', 'mora', 'naranja', 'nectarina', 'papaya', 'palta', 'pera', 'piña', 'platano', 'pomelo', 'sandia', 'toronja', 'uva', 'zarzamora', 'patata', 'arroz', 'quinoa', 'asno', 'buey', 'vaca', 'pollo', 'pato', 'cabra', 'oveja', 'poni', 'caballo', 'gallo', 'gallina', 'toro', 'pavo', 'perdiz', 'cerdo', 'codorniz', 'conejo', 'hipopotamo', 'elefante', 'rinoceronte', 'llama'],
    list(map(lambda el: el['name'], TFT_CLASSES)),
    BASIC_ITEMS,
    UPGRADED_ITEMS,
    CHAMPIONS_1,
    CHAMPIONS_2,
    CHAMPIONS_3,
    CHAMPIONS_4,
    CHAMPIONS_5
])))

def gen_ID():
    return random.choice(IDS) + '-' + str(random.randint(1, 999))

def aux_tft_get_n_from_list(items, n, repeat = True):
    if repeat:
        return list(map(lambda el: random.choice(items), [0] * n))
    else:
        result = []
        itemsCopy = list(items).copy()
        for i in range(n):
            item = random.choice(itemsCopy)
            itemsCopy.remove(item)
            result.append(item)
        return result

def aux_tft_get_n_champions_sorted_with_price(n, repeat = True):
    result = aux_tft_get_n_from_list(CHAMPIONS_WITH_PRICE, n, repeat)
    result.sort()
    return result

def aux_tft_create_list(items):
    return "\n" + "\n".join(map(lambda el: '- {0}'.format(el), items))

def tft_6_team_class():
    CLASS = random.choice(list(filter(lambda el: 6 in el['props'], TFT_CLASSES)))
    return 'Acaba la partida con 6 unidades del {0} "{1}"'.format(CLASS['type'], CLASS['name'])

def tft_2_4_team_class():
    CLASS_4 = random.choice(list(filter(lambda el: 4 in el['props'], TFT_CLASSES)))
    CLASS_2 = random.choice(
        list(
            filter(
                lambda el: 2 in el['props'] and el['name'] != CLASS_4['name'] and el['type'] == CLASS_4['type'], 
                TFT_CLASSES
            )
        )
    )
    return 'Acaba la partida con 4 unidades del {0} "{1}" y 2 unidades del {0} "{2}"'.format(CLASS_4['type'], CLASS_4['name'], CLASS_2['name'])

def tft_3_3_team_class():
    CLASS_A = random.choice(list(filter(lambda el: 3 in el['props'], TFT_CLASSES)))
    CLASS_B = random.choice(
        list(
            filter(
                lambda el: 3 in el['props'] and el['name'] != CLASS_A['name'] and el['type'] == CLASS_A['type'], 
                TFT_CLASSES
            )
        )
    )
    return 'Acaba la partida con 3 unidades del {0} "{1}" y 3 unidades del {0} "{2}"'.format(CLASS_A['type'], CLASS_A['name'], CLASS_B['name'])

def tft_2_out_of_4_items_same_character():
    items = aux_tft_create_list(aux_tft_get_n_from_list(UPGRADED_ITEMS, 4))
    return 'Acaba la partida con un personaje equipado con 2 de los siguientes objetos, a tu elección: {0}'.format(items)

def tft_2_characters_same_item():
    itemsWithGauntlet = np.concatenate([UPGRADED_ITEMS, ['Thief\'s Gloves']])
    items = aux_tft_create_list(aux_tft_get_n_from_list(itemsWithGauntlet, 6, False))
    return 'Acaba la partida con dos personajes diferentes equipados con el mismo objeto, dentro de los siguientes: {0}'.format(items)

def tft_3_out_of_10_items():
    items = aux_tft_create_list(aux_tft_get_n_from_list(UPGRADED_ITEMS, 8))
    return 'Acaba la partida con un personaje equipado con 3 de los siguientes objetos, a tu elección: {0}'.format(items)

def tft_forbidden_champions():
    characters = aux_tft_create_list(aux_tft_get_n_champions_sorted_with_price(12, False))
    return 'No utilices en ninguna batalla a ninguno de los siguientes personajes: {0}'.format(characters)

def tft_forbidden_items():
    items = aux_tft_create_list(aux_tft_get_n_from_list(UPGRADED_ITEMS, 14, False))
    return 'No construyas ni obtengas en un caroussel ninguno de los siguientes objetos: {0}'.format(items)

def tft_forbidden_classes():
    classes = aux_tft_create_list(aux_tft_get_n_from_list(TFT_CLASSES_NAMES, 7, False))
    return 'No actives el beneficio de ninguna de las siguientes clases/orígenes: {0}'.format(classes)

def tft_3_out_of_8_classes():
    classes = aux_tft_create_list(aux_tft_get_n_from_list(TFT_CLASSES_NAMES, 8, False))
    return 'Acaba la partida con 3 de las siguientes 8 clases/orígenes activadas: {0}'.format(classes)

def tft_2_out_of_6_characters_with_item():
    characters = aux_tft_get_n_champions_sorted_with_price(6)
    charactersWithItems = []
    for character in characters:
        charactersWithItems.append('{0} equipado con el objeto "{1}"'.format(character, random.choice(UPGRADED_ITEMS)))
    characters = aux_tft_create_list(charactersWithItems)
    return 'Acaba la partida con dos de los siguientes personajes: {0}'.format(characters)

def tft_3_stars():
    characters = aux_tft_create_list([
        '[1] ' + random.choice(CHAMPIONS_1),    
        '[1] ' + random.choice(CHAMPIONS_1),    
        '[2] ' + random.choice(CHAMPIONS_2),    
        '[2] ' + random.choice(CHAMPIONS_2),    
        '[3] ' + random.choice(CHAMPIONS_3),    
        '[3] ' + random.choice(CHAMPIONS_3),    
        '[4] ' + random.choice(CHAMPIONS_4),    
    ])
    return 'Acaba con un personaje de 3 estrellas (***) a tu elección, de entre los siguientes: {0}'.format(characters)

def tft_5_champions():
    characters = aux_tft_create_list(aux_tft_get_n_champions_sorted_with_price(15, False))
    return 'Acaba la partida con 5 de los siguientes personajes (a tu elección): {0}'.format(characters)

def tft_3_items_2_champions():
    characters = aux_tft_create_list(aux_tft_get_n_champions_sorted_with_price(5, False))
    items = aux_tft_create_list(aux_tft_get_n_from_list(UPGRADED_ITEMS, 15))
    return 'Elige 2 personajes de la lista. Acaba la partida con ambos en el equipo equipados con 3 objetos de la lista cada uno. Solo puedes repetir objetos si aparecen duplicados en la lista.\n\nPersonajes: {0}\n\nObjetos: {1}'.format(characters, items)

def tft_team_leader():
    defeatConditions = aux_tft_create_list([
        'El personaje elegido aparece en la tienda y no lo compras (a menos que lo tengas a ***).', 
        'El personaje elegido aparece en un caroussel y, sin que otro personaje te lo robe, decides no adquirirlo (a menos que lo tengas a ***).',
        'Equipas un objeto a un personaje que no sea el elegido antes de que el elegido posea el máximo de objetos posible.', 
        'Libras una sola batalla sin el elegido (una vez ha sido adquirido).',
        'No llegas a obtener al elegido en toda la partida.', 
        'Libras una sola batalla sin colocar los personajes de forma simétrica, donde el eje de simetría contenga al elegido (esto solo aplica desde que se obtiene al elegido).',
    ])
    characters = aux_tft_create_list(aux_tft_get_n_champions_sorted_with_price(3, False))
    return 'Elige uno de los siguientes 3 personajes para hacerlo el líder de tu equipo: {0}\nTienes estas condiciones de derrota: {1}.\nAclaración: si decides no adquirir un personaje de los propuestos la primera vez que tienes la posibilidad, todavía optas a obtener el resto de ellos.'.format(characters, defeatConditions)

def tft_fast_campions():
    characters = aux_tft_create_list(aux_tft_get_n_champions_sorted_with_price(5, False))
    return 'Debes comprar los 3 primeros personajes que encuentres en la tienda dentro de la siguiente lista: {0}.\nPierdes si dejas pasar uno solo de ellos, si no los incluyes en todos los combates desde la adquisición o si acabas la partida sin haber encontrado 3 de ellos.'.format(characters)

def tft_fast_golem_kill():
    eligibleCharacters = np.concatenate([
        list(map(lambda el: '[1] ' + el, CHAMPIONS_1)),
        list(map(lambda el: '[2] ' + el, CHAMPIONS_2)),
        list(map(lambda el: '[3] ' + el, CHAMPIONS_3)),
        ['[4] ' + random.choice(CHAMPIONS_4)]
    ])
    characters = aux_tft_get_n_from_list(eligibleCharacters, 12, False)
    characters.sort()
    characters = aux_tft_create_list(characters)
    return 'Derrota a los golems **únicamente con 4 personajes**. Estos personajes podrán ser elegidos dentro de las siguientes opciones: {0}'.format(characters)

def tft_1_champion_1_class_1_item():
    character = random.choice(CHAMPIONS_WITH_PRICE)
    itemsWithGauntlet = np.concatenate([UPGRADED_ITEMS, ['Thief\'s Gloves']])
    item = random.choice(itemsWithGauntlet)
    chosenclass = random.choice(TFT_CLASSES)
    return 'Adquiere lo más rápido posible un {0} equipado con un {1}. Adicionalmente, activa lo más rápido posible la {2} {3}. Libra el resto de batallas con ellos. Deberás acabar la partida con todos los requisitos cumplidos.'.format(character, item, chosenclass['type'], chosenclass['name'])

def generate_quest():
    return random.choice([
        tft_6_team_class,
        tft_2_4_team_class,
        tft_3_3_team_class,
        tft_2_out_of_4_items_same_character,
        tft_2_characters_same_item,
        tft_3_out_of_10_items,
        tft_forbidden_champions,
        tft_forbidden_items,
        tft_forbidden_classes,
        tft_3_out_of_8_classes,
        tft_2_out_of_6_characters_with_item,
        tft_3_stars,
        tft_5_champions,
        tft_3_items_2_champions,
        tft_team_leader,
        tft_fast_campions,
        tft_fast_golem_kill,
        tft_1_champion_1_class_1_item
    ])()

tftRooms = {}
tftPlayers = {}

class TFTRoom:

    def __init__(self, id, creator, channel, rerolls = 3, showDiscarded = True):
        self.id = id
        self.rerolls = rerolls
        self.showDiscarded = showDiscarded
        self.players = {}
        self.join(creator)
        self.creator = creator.id
        self.channel = channel
        self.players[creator.id]['creator'] = True
        self.status = 'preparing'

    def internalError(self, player = 'unknown'):
        print('Internal error: player {0} should not try to ready from room "{1}"', player, self.id)
        return 'este mensaje no debería llegarte nunca y es un error interno. Por favor, espera mientras lo arreglamos.'

    def sendChannel(self, message):
        asyncio.ensure_future(self.channel.send(message))

    def playersWithStatus(self, status):
        playersWithStatusAmount = 0
        for playerId, player in self.players.items():
            if player['status'] == status:
                playersWithStatusAmount += 1
        return playersWithStatusAmount      

    def readyPlayers(self):
        return self.playersWithStatus('ready')

    def finishedPlayers(self):
        return self.playersWithStatus('finished')

    def sendEveryPlayer(self, message):
        for playerId, player in self.players.items():
            asyncio.ensure_future(player['user'].send(message))

    def destroy(self, player = None, automatic = False):
        if player != None and player != self.creator:
            return 'no tienes permisos para hacer eso. Pídele a <@{0}> que lo haga.'.format(self.creator)
        else:
            if player != None or automatic:
                self.sendEveryPlayer('La sala de TFT _{0}_ en la que estabas ha sido destruida.'.format(self.id))

            if automatic:
                self.sendChannel('La sala de TFT _{0}_ ha sido destruida porque llevaba demasiado tiempo activa.'.format(self.id))

            for playerId, player in self.players.items():
                del tftPlayers[playerId]
            del tftRooms[self.id]

            return 'tu sala se ha destruido correctamente.'

    def join(self, player):
        if player.id in self.players.items():
            return 'no te preocupes. Ya estabas unido a esta sala. Si lo que deseas es irte, deberías utilizar `&tft hidden_quest leave`'
        elif player.id in tftPlayers:
            return 'ya estás unido a la sala "{0}". Utiliza `&tft hidden_quest leave` para irte de la sala en la que estás.'.format(tftPlayers[player.id])
        elif len(self.players) >= 8:
            return 'lo siento, esta sala ya está llena.'
        else:
            self.players[player.id] = {
                'creator': False,
                'user': player,
                'status': 'preparing',
                'quest': generate_quest(),
                'questCompleted': False,
                'rerolls': self.rerolls,
                'discarded': [],
                'position': 0,
                'value': 0
            }
            tftPlayers[player.id] = self.id
            self.sendQuest(player)
            return 'te has unido con éxito a la sala _{0}_.'.format(tftPlayers[player.id])

    def leave(self, playerId):
        if self.status != 'preparing':
            return 'no puedes irte de una partida que está en curso. Tendrás que esperar a que se termine'
        elif self.creator == playerId:
            return 'no puedes irte de una sala si eres el creador. Si quieres destruir la sala, puedes utilizar `&tft hidden_quest destroy`.'
        else:
            del self.players[playerId]
            del tftPlayers[playerId]
            return 'te has ido correctamente de la partida _{0}_.'.format(self.id)

    def ready(self, playerId):
        if not playerId in self.players:
            return self.internalError(playerId)
        elif self.status != 'preparing':
            return 'la sala "{0}" no está en fase de preparación, así que no puedes marcar que estás listo. Para más ayuda, escribe `&tft hidden_quest help`.'
        elif self.players[playerId]['status'] == 'ready':
            return 'no te preocupes, que eso ya me lo habías dicho y lo tengo apuntado ;)'
        else:
            self.players[playerId]['status'] = 'ready'
            readyPlayersAmount = self.readyPlayers()
            if readyPlayersAmount == 8:
                self.startGame()
            return 'has aceptado tu misión secreta y has marcado que ya estás listo. Personajes preparados: {0}/{1}.'.format(readyPlayersAmount, len(self.players))

    def reroll(self, playerId):
        if not playerId in self.players:
            return self.internalError(playerId)
        playerObject = self.players[playerId]
        if playerObject['status'] != 'preparing':
            return 'ya has aceptado tu misión. No se permiten más rerolls en este punto.'
        if playerObject['rerolls'] <= 0:
            return 'ya no te quedan más rerolls. ¡Lo siento!'
        playerObject['rerolls'] -= 1
        playerObject['discarded'].append(playerObject['quest'])
        playerObject['quest'] = generate_quest()
        self.sendQuest(playerObject['user'])
        return 'te he enviado por privado tu nueva misión secreta. Te quedan {0} rerolls disponibles.'.format(playerObject['rerolls'])

    def start(self, playerId):
        if playerId != self.creator:
            return 'no tienes permisos para hacer eso. Pídele a <@{0}> que lo haga.'.format(self.creator)
        readyPlayersAmount = self.readyPlayers()
        if readyPlayersAmount < len(self.players):
            return 'todavía no está todo el mundo listo. Están listas {0}/{1} personas.'.format(readyPlayersAmount, len(self.players))
        self.startGame()
        self.sendEveryPlayer('¡Todos los jugadores de tu partida de TFT están listos para jugar!')
        return 'estáis todos listos. ¡Que comience la partida de TFT! Quien vaya terminando, por favor, que utilice el comando `&tft hidden_quest end <posicion_partida> <mision_cumplida (y/n)>`.'

    def end(self, playerId, position, quest):
        if not playerId in self.players:
            return self.internalError(playerId)
        if self.status != 'playing':
            return 'no puedes acabar una partida que no ha empezado. Para salirte de la sala, utiliza `&tft hidden_quest leave`. Para eliminar la sala, <@{0}> puede utilizar el comando. `&tft hidden_quest delete`'
        try:
            positionNumber = int(position)
            if positionNumber < 1 or positionNumber > 8:
                raise
        except:
            return '"{0}" no es una posición válida. Debería ser un número entre el 1 y el 8, incluidos. ¿En qué posición has quedado en el TFT?'.format(position)
        if quest[0] != 'y' and quest[0] != 'n':
            return '"{0}" no es una respuesta de sí o no. Por favor, utiliza "y" si has completado la misión secreta y "n" si no la has completado.'
        playerObject = self.players[playerId]
        if playerObject['status'] == 'preparing':
            return 'hasta que no empiece la partida no podrás hacer eso.'
        playerObject['status'] = 'finished'
        playerObject['position'] = positionNumber
        playerObject['value'] = positionNumber
        if quest[0] == 'y':
            playerObject['questCompleted'] = True
            response = 'has completado con éxito tu misión secreta'
        else:
            playerObject['questCompleted'] = False
            playerObject['value'] += 10
            response = 'has fracasado tu misión secreta'
        response += ' y has quedado en la {0}ª posición de tu partida. Si esto no es correcto, por favor, vuelve a introducir el comando con los parámetros adecuados.'.format(positionNumber)
        finishedPlayersAmount = self.finishedPlayers()
        if finishedPlayersAmount < len(self.players):
            response += ' Jugadores que han terminado: {0}/{1}'.format(finishedPlayersAmount, len(self.players))
        else:
            self.endGame()
        return response

    def startGame(self):
        self.status = 'playing'
        for playerId, player in self.players.items():
            player['status'] = 'playing'

    def endGame(self):
        self.status = 'finished'
        self.sendStatus()
        self.destroy()

    def sendQuest(self, player):
        asyncio.ensure_future(player.send('Esta es tu misión secreta: _{0}_'.format(self.players[player.id]['quest'])))
        asyncio.ensure_future(player.send('Te quedan {0}/{1} rerolls disponibles.'.format(self.players[player.id]['rerolls'], self.rerolls)))

    def sendStatus(self):
        totalPlayers = len(self.players)
        if self.status == 'preparing':
            readyPlayers = self.readyPlayers()
            gameStatus = 'La partida no ha empezado todavía.\nLos siguientes jugadores se han unido ({0}/{1} ya están preparados):\n'.format(readyPlayers, totalPlayers)
            for playerId, player in self.players.items():
                gameStatus += '- <@{0}>'.format(playerId)
                if(player['creator'] == True):
                    gameStatus += ' [CREADOR]'
                if(player['status'] == 'ready'):
                    gameStatus += ' (Preparado)'
                gameStatus += '\n'

        elif self.status == 'playing':
            finishedPlayers = self.finishedPlayers()
            gameStatus = 'La partida está en curso.\n {0}/{1} han finalizado la partida. Jugadores presentes:\n'.format(finishedPlayers, totalPlayers)
            for playerId, player in self.players.items():
                gameStatus += '- <@{0}>'.format(playerId)
                if(player['creator'] == True):
                    gameStatus += ' [CREADOR]'
                if(player['status'] == 'finished'):
                    gameStatus += ' (Finalizado)'
                gameStatus += '\n'

        elif self.status == 'finished':
            gameStatus = 'La partida ha finalizado. Las posiciones finales son:\n'
            playerItems = list(self.players.items())
            playerItems.sort(key = lambda playerItem: playerItem[1]['value'])
            count = 1
            countStatus = 0
            for playerId, player in playerItems:
                if countStatus == 0:
                    gameStatus += '**Han conseguido completar la misión secreta:**\n'
                    countStatus = 1
                    if player['questCompleted'] == False:
                        gameStatus += '\t¡Ninguno!\n'
                        countStatus = 2
                        gameStatus += '**Han fracasado en su misión secreta:**\n'
                elif countStatus == 1 and player['questCompleted'] == False:
                    gameStatus += '**Han fracasado en su misión secreta:**\n'
                    countStatus = 2

                gameStatus += '\t#{0} - <@{1}> [Posición {2}]\n'.format(count, playerId, player['position'])
                count += 1
        else:
            self.sendChannel(self.internalError())
            return

        self.sendChannel('Sala "{0}" - {1}'.format(self.id, gameStatus))

        if self.status == 'finished':
            self.sendChannel('Y ahora procedo a revelar las misiones secretas de los jugadores.')
            for playerId,player in self.players.items():
                self.sendChannel('**La mision secreta de <@{0}> era la siguiente:** _{1}_'.format(playerId, player['quest']))
                if self.showDiscarded and len(player['discarded']) > 0:
                    self.sendChannel('Además, <@{0}> descartó las siguientes misiones'.format(playerId))
                    for quest in player['discarded']:
                        self.sendChannel('_{0}_'.format(quest))


def tellUser(userId, message):
    return '<@{0}>, {1}'.format(userId, message)

class TFTHiddenQuestsCommands:

    @classmethod
    async def autodestruction(cls, roomId):
        await asyncio.sleep(AUTODESTRUCTION_TIME)
        if roomId in tftRooms:
            tftRooms[roomId].destroy(None, True)

    @classmethod
    def create(cls, creator, channel, rerolls = '3', showDiscarded = 'y'):
        if creator.id in tftPlayers:
            return tellUser(creator.id, 'ya estás en una sala de TFT. Solo puedes crear una sala si no estás en ninguna. Puedes abandonar tu sala actual mediante `&tft hidden_quest leave`.')
        try:
            rerollsNumber = int(rerolls)
        except:
            return tellUser(creator.id, 'el parámetro _rerolls_ debe ser un número (_{0}_ no me parece suficientemente _número_). Por ejemplo `&tft hidden_quest create 2`.'.format(rerolls))

        if showDiscarded[0] != 'y' and showDiscarded[0] != 'n':
            return tellUser(creator.id, 'el último parámetro solo espera dos opciones: **_y_** o **_n_**. Si quieres que ponga por el grupo las misiones descartadas, puedes usar **_y_** (valor por defecto). En caso contrario, puedes usar **_n_**. Por ejemplo: `&tft hidden_quest 3 n`.')

        showDiscardedBool = showDiscarded[0] == 'y'

        newId = gen_ID()
        while newId in tftRooms:
            newId = gen_ID()
        tftRooms[newId] = TFTRoom(newId, creator, channel, rerollsNumber, showDiscardedBool)
        asyncio.ensure_future(TFTHiddenQuestsCommands.autodestruction(newId))
        return tellUser(creator.id, 'has creado con éxito la sala _{0}_ y te has unido.'.format(newId))


    @classmethod
    def join(cls, user, roomId):
        if not roomId in tftRooms:
            return tellUser(user.id, 'la sala _{0}_ no existe.'.format(roomId))
        response = tftRooms[roomId].join(user)
        return tellUser(user.id, response)

    @classmethod
    def destroy(cls, user):
        if not user.id in tftPlayers:
            return tellUser(user.id, 'no estás en ninguna sala de TFT.')
        return tellUser(user.id, tftRooms[tftPlayers[user.id]].destroy(user.id))

    @classmethod
    def leave(cls, user):
        if not user.id in tftPlayers:
            return tellUser(user.id, 'no estás en ninguna sala de TFT.')
        return tellUser(user.id, tftRooms[tftPlayers[user.id]].leave(user.id))

    @classmethod
    def ready(cls, user):
        if not user.id in tftPlayers:
            return tellUser(user.id, 'no estás en ninguna sala de TFT.')
        return tellUser(user.id, tftRooms[tftPlayers[user.id]].ready(user.id))

    @classmethod
    def reroll(cls, user):
        if not user.id in tftPlayers:
            return tellUser(user.id, 'no estás en ninguna sala de TFT.')
        return tellUser(user.id, tftRooms[tftPlayers[user.id]].reroll(user.id))

    @classmethod
    def start(cls, user):
        if not user.id in tftPlayers:
            return tellUser(user.id, 'no estás en ninguna sala de TFT.')
        return tellUser(user.id, tftRooms[tftPlayers[user.id]].start(user.id))

    @classmethod
    def end(cls, user, position, quest):
        if not user.id in tftPlayers:
            return tellUser(user.id, 'no estás en ninguna sala de TFT.')
        return tellUser(user.id, tftRooms[tftPlayers[user.id]].end(user.id, position, quest))

    @classmethod
    def status(cls, user):
        if not user.id in tftPlayers:
            return tellUser(user.id, 'no estás en ninguna sala de TFT.')
        tftRooms[tftPlayers[user.id]].sendStatus()
        return None
