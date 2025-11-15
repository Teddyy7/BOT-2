import discord
from discord.ext import commands
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
if BOT_TOKEN is None:
    print("შეცდომა: BOT_TOKEN ვერ მოიძებნა Railway Variables-ში.")
    exit()

intents = discord.Intents.default()
intents.members = True       # 
intents.message_content = True # 

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ბოტი ჩაირთო როგორც {bot.user}")
    print("-" * 30)

    try:
        await bot.load_extension('antitag_cog')
        print(f"წარმატებით ჩაიტვირთა: antitag_cog")
    except Exception as e:
        print(f"შეცდომა: ვერ ჩაიტვირთა antitag_cog: {e}")

    print("-" * 30)
    
    try:
        synced = await bot.tree.sync()
        print(f"წარმატებით დარეგისტრირდა {len(synced)} ბრძანება.")
    except Exception as e:
        print(f"შეცდომა ბრძანებების რეგისტრაციისას: {e}")

bot.run(BOT_TOKEN)
