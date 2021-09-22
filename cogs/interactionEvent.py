import discord
from discord.ext import commands
import time

class InteractionEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_interaction(self,interaction: discord.Integration):
        if interaction.type == discord.InteractionType.application_command:
            name = interaction.data['name']
            toCall = getattr(self, name)
            await toCall(interaction)
    
    async def ping(self, interaction: discord.Integration):
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        ping = (time.monotonic() - before) * 1000
        await interaction.response.send_message(f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")


def setup(bot):
    bot.add_cog(InteractionEvent(bot))