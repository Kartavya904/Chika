import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO
import aiohttp

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=['.'], intents=intents, activity=discord.Game(name='.help | Managing HCS invite logging.'), help_command=None)

for file in os.listdir('cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')
bot.load_extension('jishaku')

@bot.event
async def on_ready():
	print(f"Logged in as {bot.user.name}")

@bot.event
async def on_member_join(member):
    guild = bot.get_guild(724397936917741608)
    channel = bot.get_channel(726924534728622231)

    welcome = Image.open("welcome.jpg")
    draw = ImageDraw.Draw(welcome)
    async with aiohttp.ClientSession() as session:
        url = member.avatar_url
        async with session.get(url=str(url)) as response:
            image_bytes = await response.read()
    await session.close()
    pfp = Image.open(BytesIO(image_bytes))
    pfp = pfp.resize((417,417))
    mask = Image.open('mask.png').convert('L')
    mask = mask.resize((417,417))
    W, H = welcome.size
    font = ImageFont.truetype("Octagon.ttf", 90)
    w, h = draw.textsize("WELCOME",font)
    draw.text(((W-w)/2,471),"WELCOME" ,(231, 84, 128),font=font)
    font = ImageFont.truetype("arial.ttf",55)
    text = f"{member.name}#{member.discriminator}! Joined the Server!"
    w, h = draw.textsize(text,font)
    draw.text(((W-w)/2,590),text,(0,0,0),font=font)
    font = ImageFont.truetype("arial.ttf",45)
    text = f"We are now at {guild.member_count} Member Strong"
    w, h = draw.textsize(text,font)
    draw.text(((W-w)/2,670),text,(0,0,0),font=font)
    welcome.paste(pfp, (619,33), mask)
    output_buffer = BytesIO()
    welcome.save(output_buffer,"png")
    output_buffer.seek(0)

    await channel.send(file=discord.File(fp=output_buffer, filename="my_file.png"))

@bot.command(
    name='ping',description='Shows you bots current latency'
    )
async def ping(ctx):
    before = time.monotonic()
    before_ws = int(round(bot.latency * 1000, 1))
    message = await ctx.send("🏓 Pong")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")


if __name__=='__main__':
	bot.run(os.environ.get("TOKEN"))