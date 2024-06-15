from discord.ext import commands
import discord
import asyncio
import time
import vars
import img

COLOR = "[\x1b[32mLOG\x1b[39m]"

class Bot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("{} Bot is initalized!".format(COLOR))
        self.channel = self.bot.get_channel(vars.CHANNEL_ID)
        
    @commands.command()
    async def proof(self, context, discord_ID, roblox_username):
        try:
            user = await self.get_discord_profile_data(discord_ID)
            img.create_conversation(user.name, img.convert_image_bytes(str(user.avatar).replace("=1024", "=48")), roblox_username)
            print("{} Successfully created image!".format(COLOR))           
            
            await self.channel.send("[LOG] Successfully created message!")
            await self.channel.send(file = discord.File("output.png"))
        except Exception as e:
            print("{} Unable to create image {}".format(COLOR, e))
            self.channel.send("[LOG] Unable to create LOG [Check Console]", delete_after = 5)
    
    async def get_discord_profile_data(self, ID):
        try:
            return await self.bot.fetch_user(ID)
        except:
            print("{} User not found".format(COLOR))
            await self.channel.send("[LOG] User not Found!", delete_after = 5)
            

if __name__ == "__main__":
   bot = commands.Bot(command_prefix="/", intents=discord.Intents().all())
   asyncio.run(bot.add_cog(Bot(bot)))
   bot.run(vars.BOT_TOKEN)