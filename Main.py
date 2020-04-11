import discord
from discord.ext import commands
import asyncio 

TOKEN = open("resources/Token.txt",'r').read()

bot = commands.Bot(command_prefix = "$")

cogs = ['Weekly_Reset','Server_SQL','Character_Creation','Character_Manager']

SPACING = 10

### GETTING STARTED ###
@bot.event
async def on_ready():
    print('//--- LOG IN --- //')
    print('Name :'.ljust(SPACING) + str(bot.user.name))
    print('ID :'.ljust (SPACING) + str(bot.user.id))
    print('//--- SERVERS --- //')
    for server in bot.guilds:
        print(str(server.name).ljust(3*SPACING) +" : "+ str(server.id))
    print('//--- COMMAND LOGS --- //')

### Cogs ###
if __name__ == '__main__':
    print('//--- LOADING COGS --- //')
    for cog in cogs:
        try:
            bot.load_extension(cog)
            print('Loaded :'.ljust(SPACING)+str(cog))
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(cog,error))
    bot.run(TOKEN)
