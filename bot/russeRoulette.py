import random
import asyncio

class RusseRoulette:

	def __init__(self, channel, size, bullets):
		self.channel = channel
		self.size = size
		self.history = []
		self.historyId = 0
		if bullets <= size:
			self.bullets = bullets
		else:
			self.bullets = size
		self.state = []
		for i in range(self.bullets):
			self.state.append(True)
		for i in range(self.size - self.bullets):
			self.state.append(False)
		random.shuffle(self.state)
		asyncio.ensure_future(self.createInitialMessage())

	def log(self, message):
		self.history.append('#{0} {1}'.format(self.historyId, message))
		self.historyId += 1
		if len(self.history) > 25:
			self.history.pop(0)

	def refreshStatus(self):
		if self.message is not None:
			asyncio.ensure_future(self.message.edit(content = self.buildStatus()))

	def buildStatus(self):
		message = "Ruleta Rusa - Pulsa 🔫 para dispararte en la cabeza\n```\nQuedan {0} balas en {1} disparos.\n\n".format(self.bullets, self.size)
		for histroyEntry in self.history:
			message += "| " + histroyEntry + "\n"
		message += "```"
		return message

	def cancel(self):
		self.bullets = 0
		self.log('La ruleta rusa ha sido cancelada.')
		self.refreshStatus()

	def shoot(self, user):
		dead = self.state.pop()
		self.size -= 1
		if dead:
			self.bullets -= 1
			self.log("☠️ ¡{0} ha muerto!".format(user.name))
		else:
			self.log("✅ {0} ha sobrevivido.".format(user.name))
		if self.bullets == 0:
			self.log("¡Ya no quedan balas en la pistola!")
		self.refreshStatus()

	async def createInitialMessage(self):
		self.message = await self.channel.send(self.buildStatus())
		await self.message.add_reaction('🔫')
