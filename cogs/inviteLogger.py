import discord
from discord.ext import commands
import typing

class InviteLogger(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.guild = 724397936917741608
		self.log = 763378620818784307
		self.old_invites = {}
		self.roles = {
			"5":757868256072695909,
			"10":757868320094421123,
			"20":757868368547020890
		}

	@commands.Cog.listener()
	async def on_ready(self):
		main_guild = self.bot.get_guild(self.guild)
		for invite in await main_guild.invites():
			self.old_invites[invite.id]=invite

	@commands.Cog.listener()
	async def on_invite_create(self, invite):
		self.old_invites[invite.id]=invite

	@commands.Cog.listener()
	async def on_member_join(self,member):
		main_guild = self.bot.get_guild(self.guild)
		for invite in await ctx.guild.invites():
			if invite.uses > self.old_invites[invite.id].uses:
				self.old_invites[invite.id]=invite
				count = 0
				for key,value in self.old_invites.items():
					if invite.inviter.id == value.inviter.id:
						count+=value.uses
				logChannel = self.bot.get_channel(self.log)
				await logChannel.send(f"{member.mention} just joined {main_guild.name}! {member.name} was invited by {invite.inviter.name}! ({count}!)")
				if str(count) in self.roles.keys():
					role = main_guild.get_role(self.roles[str(count)])
					if role != None:
						if not role in invite.inviter.roles():
							await invite.inviter.add_roles(role)
				break

	@commands.command()
	@commands.guild_only()
	async def invites(self, ctx, user:typing.Optional[typing.Union[discord.Member,discord.User]]):
		user = user or ctx.author
		count = 0
		for key,values in self.old_invites.items():
			if values.inviter.id == user.id:
				count+=values.uses
		embed = discord.Embed(title="📨 Invites",color=0x00FFFF)
		embed.description = f"{user.name} has {count} invite"+("" if count<=1 else "s")
		embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(InviteLogger(bot))