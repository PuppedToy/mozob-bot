import asyncio
import random

class InvisibleFriendUser:

	def __init__(self, room, user):
		self.user = user
		self.room = room
		self.present = None
		self.target = None

class InvisibleFriend:

	def __init__(self, message, isSecretRoom = False):
		self.isSecretRoom = isSecretRoom
		self.roomType = 'PÚBLICA'
		if self.isSecretRoom:
			self.roomType = 'SECRETA'
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
				asyncio.ensure_future(currentUser.user.send("¡Te ha tocado {0}! Por favor, escribe tu regalo de amigo invisible para {0}.".format(currentUser.target.user.name)))
			self.refreshStatus()

	def givePresent(self, user, present):
		if user.id in self.users and self.users[user.id].present is None:
			self.users[user.id].present = present
			users = self.getUsersList()
			if len(self.getGiftUsersList()) == len(users):
				self.revealed = True
				for user in users:
					target = user.target
					asyncio.ensure_future(target.user.send('¡Has recibido un regalo de {0}! El contenido del regalo es el siguiente:'.format(user.user.name)))
					asyncio.ensure_future(target.user.send(user.present))
				asyncio.ensure_future(self.channel.send("¡Todos los usuarios del amigo invisible han recibido sus regalos!"))
			self.refreshStatus()

	def cancel(self):
		self.cancelled = True
		self.refreshStatus()

	def refreshStatus(self):
		if self.message is not None:
			asyncio.ensure_future(self.message.edit(content = self.buildStatus()))

	def buildStatus(self):
		users = self.users.items()
		message = "**Sala de amigo invisible [{0}]. Reacciona con 🎁 para unirte y ▶️ para empezar.**\n```\n{1} usuarios dentro de la sala:\n\n".format(self.roomType, len(users))
		if self.cancelled:
			return message + "Amigo invisible cancelado.\n```"
		for userId, user in users:
			if user.target is None:
				message += "{0} está esperando dentro... ⏱\n".format(user.user.name)
			elif user.present is None:
				message += "{0} está fabricando su regalo... ⛏\n".format(user.user.name)
			elif self.revealed == False:
				message += "¡{0} ha envuelto su regalo! 🎁\n".format(user.user.name)
			elif not self.isSecretRoom:
				message += "{0} ha ha entregado su 🎁 a {1} --> {2}\n".format(user.user.name, user.target.user.name, user.present)
			else:
				message += "{0} ha ha entregado su 🎁 a {1} --> [Contenido privado]\n".format(user.user.name, user.target.user.name)

		if len(users) <= 0:
			message += "La sala está vacía"
		message += "```"
		return message
	
	async def createInitialMessage(self):
		self.message = await self.channel.send(self.buildStatus())
		await self.message.add_reaction('🎁')
		await self.message.add_reaction('▶️')