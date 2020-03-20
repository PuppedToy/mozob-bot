import asyncio

invisibleFriends = {}

class InvisibleFriendUser:

	def __init__(self, room, user):
		self.user = user
		self.room = room
		self.present = None
		self.sender = None

class InvisibleFriend:

	def __init__(self, message):
		self.users = {}
		self.addUser(message.author)
		self.channel = message.channel
		self.message = None
		asyncio.ensure_future(self.createInitialMessage())

	def addUser(self, user):
		if not user.id in self.users:
			self.users[user.id] = InvisibleFriendUser(self, user)
		if not user.id in invisibleFriends:
			invisibleFriends[user.id] = []
		if not self in invisibleFriends[user.id]:
			invisibleFriends[user.id].append(self)

	def refreshStatus(self):
		asyncio.ensure_future(self.message.edit(content = self.buildStatus()))

	def buildStatus(self):
		message = "**Sala de amigo invisible - Reacciona con 🎁 para unirte y quita la reacción para irte**\n```\nUsuarios dentro de la sala:\n\n"
		for userId, user in self.users.items():
			if user.sender is None:
				message += "{0} está esperando dentro... ⏱\n".format(user.user.name)
			elif user.present is None:
				message += "{0} está fabricando su regalo... ⛏\n".format(user.user.name)
			else:
				message += "¡{0} ha envuelto su regalo! 🎁\n".format(user.user.name)
		message += "```"
		return message
	
	async def createInitialMessage(self):
		self.message = await self.channel.send(self.buildStatus())
		await self.message.add_reaction('🎁')
