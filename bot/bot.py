import os
import discord
import asyncio
import configparser
import random

from bot.commands import Command
from bot.tftHiddenQuests import TFTHiddenQuestsCommands
from bot.unicodeEmojis import emojis

client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as: {0} - {1}'.format(client.user.name, client.user.id))
    print('-'*20)

shortcuts = [
    ['tft hq', 'tft hidden_quest', True],
    ['tft hidden_quest h', 'tft hidden_quest help', False],
    ['tft hidden_quest cmd', 'tft hidden_quest commands', False],
    ['tft hidden_quest c', 'tft hidden_quest create', False],
    ['tft hidden_quest c', 'tft hidden_quest create', True],
    ['tft hidden_quest j', 'tft hidden_quest join', True],
    ['tft hidden_quest lv', 'tft hidden_quest leave', True],
    ['tft hidden_quest rrl', 'tft hidden_quest reroll', False],
    ['tft hidden_quest rr', 'tft hidden_quest reroll', False],
    ['tft hidden_quest rdy', 'tft hidden_quest ready', False],
    ['tft hidden_quest rd', 'tft hidden_quest ready', False],
    ['tft hidden_quest re', 'tft hidden_quest ready', False],
    ['tft hidden_quest sta', 'tft hidden_quest start', False],
    ['tft hidden_quest str', 'tft hidden_quest start', False],
    ['tft hidden_quest s', 'tft hidden_quest status', False],
    ['tft hidden_quest e', 'tft hidden_quest end', True]
]

def applyShortcuts(command):
    result = command
    for shortcut in shortcuts:
        fullShortcut = '&' + shortcut[0]
        fullReplacement = '&' + shortcut[1]
        hasExtraParameters = shortcut[2]
        
        if not hasExtraParameters and result == fullShortcut:
            result = fullReplacement
        elif hasExtraParameters:
            result = result.replace(fullShortcut + ' ', fullReplacement + ' ')
    return result

@client.event
@asyncio.coroutine
def on_reaction_remove(reaction, user):
    if user == client.user:
        return
    if reaction.emoji == '🎁':
        Command.leaveInvisibleFriend(reaction.message.id, user)
    if reaction.emoji == '🔫':
        Command.shootRusseRoulette(reaction.message.id, user)

    # From here random reactions
    if reaction.message.author == client.user:
        return
    if random.randint(0, 50) == 0:
        yield from reaction.message.add_reaction(reaction.emoji)

@client.event
@asyncio.coroutine
def on_reaction_add(reaction, user):
    if user == client.user:
        return
    if reaction.emoji == '🎁':
        Command.joinInvisibleFriend(reaction.message.id, user)
    if reaction.emoji == '▶️':
        Command.startInvisibleFriend(reaction.message.id, user)
    if reaction.emoji == '⚙️':
        Command.sendSettingsInvisibleFriend(reaction.message.id, user)
    if reaction.emoji == '🔫':
        Command.shootRusseRoulette(reaction.message.id, user)

    # From here random reactions
    if reaction.message.author == client.user:
        return
    if random.randint(0, 100) == 0:
        yield from reaction.message.add_reaction(reaction.emoji)

@client.event
@asyncio.coroutine
def on_message(message):
    command = applyShortcuts(message.content.lower())
    if message.author == client.user:
        return
    elif isinstance(message.channel, discord.DMChannel):
        Command.givePresentInvisibleFriend(message)
    elif command == '&':
        yield from message.channel.send('<@{0}>, No command has been passed.'.format(message.author.id))
    elif command == '&help':
        yield from message.channel.send(Command.help())
    elif command == '&hello':
        yield from message.channel.send(Command.hello(message.author.id))
    elif command.startswith('&factory create'):
        parts = command.replace('&factory create', '').split('&')
        if len(parts) != 2:
            response = '''No has usado bien el comando. 
Hay que usar: `&factory create <Nombre fabrica>&<Nombre producto>`
Por ejemplo: `&factory create mi fabrica de tomates&tomate`
'''
        else:
            response = Command.createFactory(message.author.id, parts[0].strip(), parts[1].strip())
        yield from message.channel.send(response)

    elif command == '&factory delete':
        yield from message.channel.send(Command.deleteFactory(message.author.id))

    elif command == '&factory list':
        yield from message.channel.send(Command.listFactory())

    elif command == '&inventory':
        yield from message.channel.send(Command.inventory(message.author.id))

    elif command.startswith('&invisible_friend h'):
        responses = Command.invisibleFriendHelp()
        yield from message.channel.send('<@{0}>, te he enviado un mensaje privado.'.format(message.author.id))
        yield from message.author.send(responses[0])
        yield from message.author.send(responses[1])
        return

    elif command.startswith('&invisible_friend'):
        isSecretTarget = False
        isSecretGiver = False
        isPrivateGiver = False
        isPrivatePresent = False

        parts = command.split(' ')
        for part in parts:
            if part == 'secret_target' or part == 'st':
                isSecretTarget = True
            if part == 'secret_giver' or part == 'sg':
                isSecretGiver = True
            if part == 'private_giver' or part == 'pg':
                isPrivateGiver = True
            if part == 'private_present' or part == 'pp':
                isPrivatePresent = True

        Command.invisibleFriend(message, isSecretTarget, isSecretGiver, isPrivateGiver, isPrivatePresent)

    elif command.startswith('&russe_roulette'):
        parts = command.split(' ')
        size = 6
        bullets = 1
        if len(parts) >= 2:
            try:
                size = int(parts[1])
            except:
                yield from message.channel.send('"{0}" no es un número válido para la capacidad de la pistola.'.format(parts[1]))
                return
        if len(parts) >= 3:
            try:
                bullets = int(parts[2])
            except:
                yield from message.channel.send('"{0}" no es una cantidad válida de balas de la pistola.'.format(parts[2]))
                return
        Command.russeRoulette(message.channel, size, bullets)

    elif command == '&alaputa':
        yield from message.channel.send(Command.alaputa())

    elif command == '&tft random_classes':
        yield from message.channel.send(Command.tftRandomClasses(message.author.id))

    elif command == '&tft hidden_quest help':
        responses = Command.tftHiddenQuestHelp()
        yield from message.channel.send(responses[0])
        yield from message.channel.send(responses[1])

    elif command == '&tft hidden_quest commands':
        yield from message.channel.send(Command.tftHiddenQuestCommands())

    elif command.startswith('&tft hidden_quest create'):
        parts = command.split(' ')
        if len(parts) == 3:
            yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.create(message.author, message.channel)))
        elif len(parts) == 4:
            yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.create(message.author, message.channel, parts[3])))
        else:
            yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.create(message.author, message.channel, parts[3], parts[4])))

    elif command.startswith('&tft hidden_quest join'):
        parts = command.split(' ')
        if len(parts) < 4:
            yield from message.channel.send('Es necesario especificar el ID de la sala a la que te quieres unir. Por ejemplo, `&tft hidden_quest join patata-18`.')
        else:
            yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.join(message.author, parts[3])))

    elif command.startswith('&tft hidden_quest destroy'):
        yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.destroy(message.author)))

    elif command.startswith('&tft hidden_quest leave'):
        yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.leave(message.author)))

    elif command.startswith('&tft hidden_quest reroll'):
        yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.reroll(message.author)))

    elif command.startswith('&tft hidden_quest ready'):
        yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.ready(message.author)))

    elif command.startswith('&tft hidden_quest start'):
        yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.start(message.author)))

    elif command.startswith('&tft hidden_quest end'):
        parts = command.split(' ')
        if len(parts) < 5:
            yield from message.channel.send('Es necesario especificar la posición en la que has quedado y si has cumplido tu misión (y) o no (n). Por ejemplo, si has quedado 5º y has fracasado en tu misión secreta, deberías poner: `&tft hidden_quest end 3 n`.')
        else:
            yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.end(message.author, parts[3], parts[4])))

    elif command.startswith('&tft hidden_quest status'):
        response = TFTHiddenQuestsCommands.status(message.author)
        if response is not None:
            yield from message.channel.send('{0}'.format(response))

    elif random.randint(0, 2000) == 1000:
        yield from message.add_reaction('<:Gartu:689953022285185089>')

    elif random.randint(0, 1000) == 1000:
        yield from message.add_reaction(random.choice(client.emojis))

    elif random.randint(0, 1000) == 1000:
        yield from message.add_reaction(random.choice(emojis))

    elif random.randint(0, 2000) == 1000:
        yield from message.add_reaction('✅')

# Set up the base bot
class DiscordBot(object):
    def __init__(self):
        self.token = None
        self.configPath = os.path.join(os.getcwd(), 'config.ini')
        self.config = configparser.ConfigParser()

    def exists_config(self):
        return os.path.exists(self.configPath)

    def create_config(self):
        # Ask user for bot token
        self.token = input('Bot Token:')
        # Creates base config file
        self.config.add_section('DiscordBot')
        self.config.set('DiscordBot', 'token', self.token)
        with open(self.configPath, 'w') as configfile:
            self.config.write(configfile)

    def get_token(self):
        self.config.read(self.configPath)
        self.token = self.config.get('DiscordBot', 'token')

    def set_token(self, token):
        self.config.read(self.configPath)
        self.config.set('DiscordBot', 'token', token)
        with open(self.configPath, 'w') as configfile:
            self.config.write(configfile)

    def run(self):
        client.run(self.token)
