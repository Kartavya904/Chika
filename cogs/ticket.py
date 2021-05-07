import discord
from discord.ext import commands

class Ticket(commands.Cog):
	def __init__(self, bot):
		self.bot=bot

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.message_id==840115124555612170 and payload.emoji.name=='🎫':
			channel = self.bot.get_channel(840072539840446474)
			message = await channel.fetch_message(840115124555612170)
			await message.remove_reaction('🎫',payload.member)
			await channel.set_permissions(payload.member, read_messages=False)
			await self.create_channel(payload.member)
			return
		if payload.emoji.name=='🔒' and payload.user_id!=self.bot.user.id:
			channel = self.bot.get_channel(payload.channel_id)
			message = await channel.fetch_message(payload.message_id)
			if not len(message.embeds)==1:
				return
			else:
				guild = self.bot.get_guild(payload.guild_id)
				user = guild.get_member(payload.user_id)
				cnl = guild.get_channel(payload.channel_id)
				embed = (message.embeds)[0]
				if embed.title=='Ticket Channel' and message.author==self.bot.user:
					if str(payload.user_id)==embed.footer.text.split(' ')[-1]:
						await self.close(cnl, user)
					else:
						permission = user.permissions_in(cnl)
						if permission.manage_channels==True:
							await self.close(cnl, user)
				return

	async def create_channel(self, member):
		guild = await self.bot.fetch_guild(724397936917741608)
		category = self.bot.get_channel(840072033236680724)
		overwrites = {
			guild.default_role: discord.PermissionOverwrite(read_messages=False),
			self.bot.user: discord.PermissionOverwrite(read_messages=True),
			member: discord.PermissionOverwrite(read_messages=True)
		}
		channel = await category.create_text_channel(name=member.name,overwrites=overwrites)
		embed = discord.Embed(color=0xFF00FF)
		embed.title = "Ticket Channel"
		embed.description = "React with 🔒 to close the channel if you have already got a reply."
		embed.set_author(name=member.name,icon_url=member.avatar_url)
		embed.set_footer(text=f"Author id: {member.id}",icon_url=self.bot.user.avatar_url)
		message = await channel.send(content=f"@here it seems like {member.mention} need some help. Please come and help him/her",embed=embed)
		await message.add_reaction('🔒')

	async def close(self,cnl,user):
		channel = await self.bot.fetch_channel(840072539840446474)
		await channel.set_permissions(user, overwrite=None)
		await cnl.delete()


def setup(bot):
	bot.add_cog(Ticket(bot))