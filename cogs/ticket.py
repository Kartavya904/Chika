import discord
from discord.components import Button
from discord.ext import commands
import aiohttp
import datetime

class Ticket(commands.Cog):
	def __init__(self, bot):
		self.bot=bot
		self.helper = None
	
	@commands.command()
	@commands.guild_only()
	@commands.is_owner()
	async def start_ticket(self, ctx):
		embed = discord.Embed()
		embed.color = 0x06ffd0
		embed.title = "Ask For Help!"
		embed.description = "React with 🎫 if you want any direct help from the server admins or mods regarding anything related to the server."
		view = discord.ui.View()
		view.add_item(discord.ui.Button(label="| Create a ticket", emoji="🎫", style=discord.ButtonStyle.gray))
		await ctx.send(embed=embed, view=view)
	
	@commands.Cog.listener()
	async def on_interaction(self,interaction: discord.Integration):
		if interaction.type==discord.InteractionType.component:
			message = interaction.message
			button = message.components[0].children[0]
			if button.type==discord.ComponentType.button:
				await interaction.response.defer()
				if interaction.message.id==868680368956530709:
					channel = self.bot.get_channel(840072539840446474)
					await channel.set_permissions(interaction.user, read_messages=False)
					await self.create_channel(interaction.user, interaction.guild_id)
					return
				elif interaction.guild_id==724397936917741608 and interaction.channel.category.id==840072033236680724:
					if not len(message.embeds)==1:
						return
					else:
						guild = message.guild
						embed = (message.embeds)[0]
						closer = interaction.user
						user = guild.get_member(int(embed.footer.text.split(' ')[-1]))
						if embed.title=='Ticket Channel' and message.author==self.bot.user and button.label=="| Close":
							if user==closer:
								await self.close(interaction.channel, user, closer)
							else:
								permission = closer.permissions_in(interaction.channel)
								if permission.manage_channels==True:
									await self.close(interaction.channel, user, closer)
						return

	# @commands.Cog.listener()
	# async def on_raw_reaction_add(self, payload):
	# 	if payload.user_id==self.bot.user.id:
	# 		return
	# 	if payload.message_id==840287218152505386 and payload.emoji.name=='🎫':
	# 		channel = self.bot.get_channel(840072539840446474)
	# 		message = await channel.fetch_message(840287218152505386)
	# 		await message.remove_reaction('🎫',payload.member)
	# 		await channel.set_permissions(payload.member, read_messages=False)
	# 		await self.create_channel(payload.member, payload.guild_id)
	# 		return
	# 	if payload.emoji.name=='🔒' and payload.user_id!=self.bot.user.id:
	# 		channel = self.bot.get_channel(payload.channel_id)
	# 		message = await channel.fetch_message(payload.message_id)

	# 		if not len(message.embeds)==1:
	# 			return
	# 		else:
	# 			guild = self.bot.get_guild(payload.guild_id)
	# 			user = guild.get_member(payload.user_id)
	# 			embed = (message.embeds)[0]
	# 			closer = guild.get_member(payload.user_id)
	# 			user = guild.get_member(int(embed.footer.text.split(' ')[-1]))
	# 			if embed.title=='Ticket Channel' and message.author==self.bot.user:
	# 				if payload.user_id==closer.id:
	# 					await self.close(channel, user, closer)
	# 				else:
	# 					permission = closer.permissions_in(channel)
	# 					if permission.manage_channels==True:
	# 						await self.close(channel, user, closer)
	# 			return

	async def create_channel(self, member, guild_id):
		guild = await self.bot.fetch_guild(724397936917741608)
		category = self.bot.get_channel(840072033236680724)
		guild = self.bot.get_guild(guild_id)
		if self.helper==None:
			self.helper = guild.get_role(824998575590473769)
		overwrites = {
			guild.default_role: discord.PermissionOverwrite(read_messages=False),
			self.bot.user: discord.PermissionOverwrite(read_messages=True),
			member: discord.PermissionOverwrite(read_messages=True),
			self.helper: discord.PermissionOverwrite(read_messages=True)
		}
		channel = await category.create_text_channel(name=member.name,overwrites=overwrites)
		embed = discord.Embed(color=0xFF00FF)
		embed.title = "Ticket Channel"
		embed.description = "React with 🔒 to close the channel if you have already got a reply."
		embed.set_author(name=member.name,icon_url=member.avatar.url)
		embed.set_footer(text=f"Author id: {member.id}",icon_url=self.bot.user.avatar.url)
		view = discord.ui.View(timeout=1)
		view.add_item(discord.ui.Button(label="| Close", style=discord.ButtonStyle.gray, emoji="🔒"))
		await channel.send(content=f"@here it seems like {member.mention} need some help. Please come and help him/her",embed=embed, view=view)

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
		embed.set_author(name=self.bot.user.name,icon_url=user.avatar.url)
		embed.set_thumbnail(url=self.bot.user.avatar.url)
		log_channel = await self.bot.fetch_channel(840182581630468096)
		await log_channel.send(embed=embed)

	async def create_log(self, messages):
		async with aiohttp.ClientSession() as session:
			async with session.post('https://mystb.in/documents',data=messages) as resp:
				key = await resp.json()
		await session.close()
		return	f'https://mystb.in/{key["key"]}'


def setup(bot):
	bot.add_cog(Ticket(bot))