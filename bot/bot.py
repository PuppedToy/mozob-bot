import os
import discord
import asyncio
import configparser
from bot.commands import Command

client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as: {0} - {1}'.format(client.user.name, client.user.id))
    print('-'*20)


@client.event
@asyncio.coroutine
def on_message(message):
    command = message.content.lower()
    if message.author == client.user:
        return
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
    elif command.startswith('&leet'):
        response = Command.leet_speak(command.replace('&leet', ''))
        yield from message.channel.send('{0}'.format(response))

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
