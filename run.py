import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=['.'],intents=intents)
slash = SlashCommand(bot, override_type=True)

@bot.event
async def on_ready():
	print(f"Logged in as {bot.user.name}")

for file in os.listdir('cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')
bot.load_extension('jishaku')

if __name__=='__main__':
	bot.run(os.environ.get("TOKEN"))