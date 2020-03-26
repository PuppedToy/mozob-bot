import asyncio
import random

class InvisibleFriendUser:

	def __init__(self, room, user):
		self.user = user
		self.room = room
		self.present = None
		self.target = None

class InvisibleFriend:

	def __init__(self, message, isSecretTarget, isSecretGiver, isPrivateGiver, isPrivatePresent):
		self.isSecretTarget = isSecretTarget
		self.isSecretGiver = isSecretGiver
		self.isPrivateGiver = isPrivateGiver and not isSecretGiver
		self.isPrivatePresent = isPrivatePresent

		self.users = {}
		self.message = None
		self.started = False
		self.revealed = False
		self.cancelled = False
		self.addUser(message.author)
		self.channel = message.channel
		asyncio.ensure_future(self.createInitialMessage())

	def addUser(self, user):
		if not user.id in self.users and not self.started:
			self.users[user.id] = InvisibleFriendUser(self, user)
			self.refreshStatus()

	def removeUser(self, user):
		if user.id in self.users and not self.started:
			del self.users[user.id]
			self.refreshStatus()

	def getUsersList(self):
		return [user[1] for user in self.users.items()]

	def getGiftUsersList(self):
		return list(filter(lambda user: user.present is not None, self.getUsersList()))

	def start(self, user):
		if user.id in self.users:
			users = self.getUsersList()
			if len(users) <= 1:
				asyncio.ensure_future(self.channel.send("¡No hay suficientes usuarios para empezar el amigo invisible! Tiene que haber al menos 2."))
				return
			targets = self.getUsersList()
			self.started = True
			for currentUser in users:
				eligibleTargets = list(filter(lambda target: target != currentUser, targets))
				currentUser.target = random.choice(eligibleTargets)
				targets.remove(currentUser.target)
				if self.isSecretTarget:
					messages = "¡Te ha tocado regalar a alguien (secreto)! Por favor, escribe tu regalo de amigo invisible."
				else:
					message = "¡Te ha tocado regalar a {0}! Por favor, escribe tu regalo de amigo invisible.".format(currentUser.target.user.name)
				asyncio.ensure_future(currentUser.user.send(message))
			self.refreshStatus()

	def givePresent(self, user, present):
		if user.id in self.users and self.users[user.id].present is None:
			self.users[user.id].present = present
			users = self.getUsersList()
			if len(self.getGiftUsersList()) == len(users):
				self.revealed = True
				for user in users:
					target = user.target
					if not self.isSecretGiver:
						message = '¡Has recibido un regalo de {0}! El contenido del regalo es el siguiente:'.format(user.user.name)
					else:
						message = '¡Has recibido un regalo de alguien (secreto)! El contenido del regalo es el siguiente:'.format(user.user.name)

					asyncio.ensure_future(target.user.send(message))
					asyncio.ensure_future(target.user.send(user.present))
				asyncio.ensure_future(self.channel.send("¡Todos los usuarios del amigo invisible han recibido sus regalos!"))
			self.refreshStatus()

	def cancel(self):
		self.cancelled = True
		self.refreshStatus()

	def refreshStatus(self):
		if self.message is not None:
			asyncio.ensure_future(self.message.edit(content = self.buildStatus()))

	def sendSettings(self, user):
		settings = '''Te envío la configuración de la sala de amigo invisible tal y como me has pedido:
- Nadie sabe a quién regala: {0}
- Nadie sabe quién regala a quién: {1}
- Cada persona sabe quién le regala, pero no se publica quién regala a quién: {2}
- Los regalos no se publican: {3}
'''.format(self.isSecretTarget, self.isSecretGiver, self.isPrivateGiver, self.isPrivatePresent).replace('False', '**NO**').replace('True', '**SÍ**')
		asyncio.ensure_future(user.send(settings))

	def buildStatus(self):
		users = self.users.items()
		message = "**Sala de amigo invisible. Reacciona con 🎁 para unirte y ▶️ para empezar.**\nSi quieres conocer la configuración de la sala, reacciona con ⚙️.\n```\n{0} usuarios dentro de la sala:\n\n".format(len(users))
		if self.cancelled:
			return message + "Amigo invisible cancelado.\n```"
		for userId, user in users:
			if user.target is None:
				message += "{0} está esperando dentro... ⏱\n".format(user.user.name)
			elif user.present is None:
				message += "{0} está fabricando su regalo... ⛏\n".format(user.user.name)
			elif self.revealed == False:
				message += "¡{0} ha envuelto su regalo! 🎁\n".format(user.user.name)
			elif not self.isPrivatePresent and not self.isSecretGiver and not self.isPrivateGiver:
				message += "{0} ha ha entregado su 🎁 a {1} --> {2}\n".format(user.user.name, user.target.user.name, user.present)
			elif self.isPrivatePresent and not self.isSecretGiver and not self.isPrivateGiver:
				message += "{0} ha ha entregado su 🎁 a {1} --> [Contenido privado]\n".format(user.user.name, user.target.user.name)
			elif not self.isPrivatePresent and (self.isSecretGiver or self.isPrivateGiver):
				message += "{0} ha entregado su 🎁 a alguien --> {1}\n".format(user.user.name, user.present)
			else:
				message += "{0} ha entregado su 🎁 a alguien --> [Contenido privado]\n".format(user.user.name)

		if len(users) <= 0:
			message += "La sala está vacía"
		message += "```"
		return message
	
	async def createInitialMessage(self):
		self.message = await self.channel.send(self.buildStatus())
		await self.message.add_reaction('🎁')
		await self.message.add_reaction('▶️')
		await self.message.add_reaction('⚙️')

