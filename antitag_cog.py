import discord
from discord.ext import commands
import asyncio # 

# -----------------------------------------------------------------
# 
PROTECTED_USER_NAMES = {
    "theodoree99",
    "lazzikaa",
    "nika_geims"
}
# -----------------------------------------------------------------

class AntiTagCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        is_protected_tagged = False
        
        for user in message.mentions:
            if user.name in PROTECTED_USER_NAMES:
                is_protected_tagged = True
                break
        
        if is_protected_tagged:
            
            tagger = message.author
            
            reply_text = f"| წაიშალა {tagger.mention} ის შეტყობინება მიზეზი : მონიშვნის გამო | ამ წევრის მონიშვნა შეუძლებელია"
            
            try:
                await message.delete()
                
                await message.channel.send(reply_text, delete_after=5.0)
                
            except discord.Forbidden:
                print(f"ERROR: არ მაქვს უფლება წავშალო შეტყობინება არხში #{message.channel.name}")
            except Exception as e:
                print(f"Anti-tag შეცდომა: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(AntiTagCog(bot))
