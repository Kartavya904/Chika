import discord
from discord.ext import commands
import aiohttp
import datetime

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
				embed = (message.embeds)[0]
				closer = guild.get_member(payload.user_id)
				user = guild.get_member(int(embed.footer.text.split(' ')[-1]))
				if embed.title=='Ticket Channel' and message.author==self.bot.user:
					if payload.user_id==closer.id:
						await self.close(channel, user, closer)
					else:
						permission = closer.permissions_in(channel)
						if permission.manage_channels==True:
							await self.close(channel, user, closer)
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

	async def close(self,cnl,user, closer):
		channel = await self.bot.fetch_channel(840072539840446474)
		await channel.set_permissions(user, overwrite=None)
		messages = await cnl.history(limit=None).flatten()
		await cnl.delete()
		m = ""
		for i in reversed(range(len(messages)-1)):
			m = m+messages[i].author.name+"#"+messages[i].author.discriminator+" :  "+messages[i].content+'\n\n'
		link = await self.create_log(m)
		embed = discord.Embed(title="Ticket Closed",color=0x00FFAA)
		embed.add_field(name="Opened By",value=f"{user.name}#{user.discriminator}",inline=True)
		embed.add_field(name="Closed By",value=f"{closer.name}#{closer.discriminator}",inline=True)
		embed.add_field(name="Archive",value=f"[Click Here]({link})",inline=True)
		embed.timestamp = datetime.datetime.now()
		embed.set_author(name=self.bot.user.name,icon_url=user.avatar_url)
		embed.set_thumbnail(url=self.bot.avatar_url)
		log_channel = await bot.fetch_channel(840182581630468096)
		await log_channel.send(embed=embed)

	async def create_log(self, messages):
		async with aiohttp.ClientSession() as session:
			async with session.post('https://mystb.in/documents',data=messages) as resp:
				key = await resp.json()
		await session.close()
		return	f'https://mystb.in/{key["key"]}'


def setup(bot):
	bot.add_cog(Ticket(bot))