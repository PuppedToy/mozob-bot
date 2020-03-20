import asyncio

class InvisibleFriendUser:

	def __init__(self, room, user):
		self.user = user
		self.room = room
		self.present = None
		self.sender = None

class InvisibleFriend:

	def __init__(self, message):
		self.users = {}
		self.message = None
		self.addUser(message.author)
		self.channel = message.channel
		asyncio.ensure_future(self.createInitialMessage())

	def addUser(self, user):
		if not user.id in self.users:
			self.users[user.id] = InvisibleFriendUser(self, user)
			self.refreshStatus()

	def removeUser(self, user):
		if user.id in self.users:
			del self.users[user.id]
			self.refreshStatus()

	def refreshStatus(self):
		if self.message is not None:
			asyncio.ensure_future(self.message.edit(content = self.buildStatus()))

	def buildStatus(self):
		users = self.users.items()
		message = "**Sala de amigo invisible - Reacciona con 🎁 para unirte y quita la reacción para irte**\n```\n{0} usuarios dentro de la sala:\n\n".format(len(users))
		for userId, user in users:
			if user.sender is None:
				message += "{0} está esperando dentro... ⏱\n".format(user.user.name)
			elif user.present is None:
				message += "{0} está fabricando su regalo... ⛏\n".format(user.user.name)
			else:
				message += "¡{0} ha envuelto su regalo! 🎁\n".format(user.user.name)
		if len(users) <= 0:
			message += "La sala está vacía"
		message += "```"
		return message
	
	async def createInitialMessage(self):
		self.message = await self.channel.send(self.buildStatus())
		await self.message.add_reaction('🎁')
