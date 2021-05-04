import discord
from discord.ext import commands

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot=bot

	@commands.command(
		name='help',
		pass_context=True,
		description='Shows you all the commands available.'
		)
	@commands.guild_only()
	async def help(self, ctx, *, cmd:str='all'):
		h = {
			"Invite Logger":["invites"],
			"Misc":["ping"],
			"Owner Only":["jishaku"]
		}
		helpEmbed = discord.Embed(color=0x00FFFF)
		helpEmbed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
		helpEmbed.set_thumbnail(url=self.bot.user.avatar_url)
		owner = self.bot.get_user(707876147324518440)
		if cmd.lower()=='all':
			helpEmbed.set_footer(text=f'Created by {owner.name}#{owner.discriminator} • Do .help [command-name] for more info about the command.',icon_url=owner.avatar_url)
			helpEmbed.title='Help Command'
			for key, val in h.items():
				helpEmbed.add_field(name=f'{key}',value=f'\n'.join([name for name in val]),inline=True)
		else:
			helpEmbed.set_footer(text=f'Created by {owner.name}#{owner.discriminator}',icon_url=owner.avatar_url)
			cmdHelp = self.bot.get_command(cmd.lower())
			if cmdHelp==None:
				await ctx.send(f'No Command found with name *{cmd}*...')
				return
			aliases = cmdHelp.aliases
			description = '<> → **Mandetory**\n[] → **Not Mandetory**'
			if len(aliases)>0:
				description = description + f'\n\n**Aliases** → {", ".join([a for a in aliases])}'
			helpEmbed.description = description
			if len(cmdHelp.description)<=1024:
				helpEmbed.add_field(name=f'{cmdHelp.name} help'.upper(),value=cmdHelp.description,inline=False)
			else:
				total = len(cmdHelp.description)
				description=cmdHelp.description
				i=1
				value=""
				r=0
				for j in range(len(cmdHelp.description)):
					if description[j:j+2]=='\n\n':
						helpEmbed.add_field(name=f'{i}# {cmdHelp.name} help'.upper(),value=cmdHelp.description[r:j],inline=False)
						i+=1
						r=j
				helpEmbed.add_field(name=f'{i}# {cmdHelp.name} help'.upper(),value=cmdHelp.description[r:],inline=False)

		await ctx.send(embed=helpEmbed)


def setup(bot):
	bot.add_cog(Help(bot))