import traceback
import sys
import discord
from discord.ext import commands

class ErrorHandeler(commands.Cog):
	def __init__(self, bot):
		self.bot=bot

	@commands.Cog.listener()
	async def on_commands_error(self, ctx, error):
		if hasattr(ctx.command, 'on_error'):
			return

		cog = ctx.cog
		if cog:
			if cog._get_overridden_method(cog.cog_command_error) is not None:
				return

		ignored = (commands.CommandNotFound, discord.Forbidden, commands.NotOwner, discord.HTTPException, discord.NotFound, discord.errors.Forbidden)

		error = getattr(error, 'original', error)

		if isinstance(error, ignored):
			return

		if isinstance(error, commands.DisabledCommand):
			await ctx.send(f'{ctx.command} has been disabled.')

		elif isinstance(error, commands.NoPrivateMessage):
			try:
				await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
			except discord.HTTPException:
				pass

		elif isinstance(error, commands.BadArgument):
			await ctx.send('I could not find that member. Please try again.')

		elif isinstance(error, commands.MissingRequiredArgument):
			complete = self.bot.get_command('help')
			if await complete.can_run(ctx):
				await complete(ctx=ctx, cmd=ctx.command.name)
			if ctx.command.is_on_cooldown:
				self.bot.get_command(ctx.command.name).reset_cooldown(ctx)

		elif isinstance(error, commands.MissingPermissions):
			await ctx.send(f'You are missing **{",".join([perm for perm in error.missing_perms])}** permission to run this command.')

		else:
			print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
			traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
	bot.add_cog(ErrorHandeler(bot))