import os
import discord
from discord.ext import commands
# from discord_slash import SlashCommand, SlashContext
from dotenv import load_dotenv
import time

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=['.'], intents=intents, activity=discord.Game(name='.help | Managing HCS invite logging.'), help_command=None)
# slash = SlashCommand(bot, override_type=True, sync_commands=True, sync_on_cog_reload=True)

for file in os.listdir('cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')
bot.load_extension('jishaku')

@bot.event
async def on_ready():
	print(f"Logged in as {bot.user.name}")

@bot.command(
    name='ping',description='Shows you bots current latency'
    )
async def ping(ctx):
    before = time.monotonic()
    before_ws = int(round(bot.latency * 1000, 1))
    message = await ctx.send("🏓 Pong")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

# @slash.slash(name="ping",description="Shows bots latency")
# async def pong(ctx: SlashContext):
#     before = time.monotonic()
#     before_ws = int(round(bot.latency * 1000, 1))
#     message = await ctx.send("🏓 Pong")
#     ping = (time.monotonic() - before) * 1000
#     await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

if __name__=='__main__':
	bot.run(os.environ.get("TOKEN"))