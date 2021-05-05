import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO

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
    pfp = Image.open(BytesIO(await (member.avatar_url).read()))
    pfp = pfp.resize((215,215))
    mask = Image.open('mask.png').convert('L')
    mask = mask.resize((215,215))
    W, H = welcome.size
    font = ImageFont.truetype("Octagon.ttf", 70)
    w, h = draw.textsize("WELCOME",font)
    draw.text(((W-w)/2,228),"WELCOME" ,(231, 84, 128),font=font,stroke_width=2, stroke_fill=(255,255,255))
    font = ImageFont.truetype("arial.ttf",35)
    text = f"{member.name}#{member.discriminator} Joined the Server!"
    w, h = draw.textsize(text,font)
    draw.text(((W-w)/2,308),text,(0,0,0),font=font,stroke_width=2, stroke_fill=(255,255,255))
    font = ImageFont.truetype("arial.ttf",25)
    text = f"We are now at {guild.member_count} Members Strong"
    w, h = draw.textsize(text,font)
    draw.text(((W-w)/2,368),text,(0,0,0),font=font,stroke_width=2, stroke_fill=(255,255,255))
    welcome.paste(pfp, (450,15), mask)
    output_buffer = BytesIO()
    welcome.save(output_buffer,"png")
    output_buffer.seek(0)

    content = f"Welcome to **Heaven's Coffeeshop [AniFarm]**, {member.mention}! \nPlease read the rules in <#727259226988216402> \nand check out the roles in <#742831976293203978> !\nWe hope you enjoy our service!  💧"
    await channel.send(content=content, file=discord.File(fp=output_buffer, filename="my_file.png"))

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(726924534728622231)
    await channel.send(f"{member.name}#{member.discriminator} has just left the server. We hope to see you again soon! 👋")

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