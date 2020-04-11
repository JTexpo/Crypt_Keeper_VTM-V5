import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import os
import sqlite3

def is_admin():
    def predicate(ctx):
        conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM admin_table")
        admins = c.fetchall()
        for admin in admins:
            if (ctx.author.id in admin) : return True
        return False
    return commands.check(predicate)

class Weekly_Reset(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.join_us_msg = '<:Crypt_Keeper:694324654227062825> Come Visit The Testing Server For Any Questions/Help : [Server_Link](https://discord.gg/weXYh8D)'
        self.colour = (0x96110F)

    # // -- A Function To Print Information In The Testing Servers Command Chat -- //
    async def log_command(self,ctx,func_name):
        try:
            # // -- Creating and Embed -- //
            log_embed = discord.Embed(
                title = ('Crypt Keeper Command Log'),
                description = ("Command : {}\nContent : `{}`".format(func_name,ctx.message.content)),
                colour = self.colour
                )
            # // -- Giving the Embed Fields -- //
            log_embed.add_field(name = "Guild", value = "{}".format(ctx.guild), inline = False)
            log_embed.add_field(name = "Channel", value = "{}".format(ctx.channel), inline = False)
            log_embed.add_field(name = "Author", value = "{}".format(ctx.author), inline = False)
            log_embed.add_field(name = "Time", value = "{}".format(datetime.now()), inline = False)
            # // -- Sending the Embed -- //
            await self.bot.get_channel(694247048396013698).send(embed = log_embed)
        except Exception as error:
            # // -- Printing What Went Wrong to the Shell -- // 
            print("Error Occured : [{}]".format(error))
        return
    # // -- A Function To Print Information In The Testing Server Error Chat -- //
    async def error_log_command(self,ctx,func_name,error):
        try:
            # // -- Creating and Embed -- //
            log_embed = discord.Embed(
                title = ('Crypt Keeper Error Log'),
                description = ("Command : {}\nContent : `{}`\nError : ```{}```".format(func_name,ctx.message.content,error)),
                colour = self.colour
                )
            # // -- Giving the Embed Fields -- //
            log_embed.add_field(name = "Guild", value = "{}".format(ctx.guild), inline = False)
            log_embed.add_field(name = "Channel", value = "{}".format(ctx.channel), inline = False)
            log_embed.add_field(name = "Author", value = "{}".format(ctx.author), inline = False)
            log_embed.add_field(name = "Time", value = "{}".format(datetime.now()), inline = False)
            # // -- Sending the Embed -- //
            await self.bot.get_channel(696027589827100792).send(embed = log_embed)
        except Exception as error:
            # // -- Printing What Went Wrong to the Shell -- // 
            print("Error Occured : [{}]".format(error))
        return

    @commands.command(name = 'weekly_reset',
                      aliases = ['wklyrst'])
    @is_admin()
    async def weekly_reset(self,ctx):
        await self.log_command(ctx,'weekly_reset')
        try:
            c_msg = ''
            conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
            c = conn.cursor()
            c.execute("SELECT room_ID, room_type, reset_msg_ID, pin_reset FROM rp_room_table")
            categories = c.fetchall()
            c.execute("SELECT * FROM reset_msg_table")
            all_table_msgs = c.fetchall()
            for rp_room in categories:
                for reset_messages in all_table_msgs:
                    if rp_room[2] == reset_messages[0] : c_msg = reset_messages[2]
                c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> The Channel Has Been Reset <:Crypt_Keeper:694324654227062825>",
                        description = (c_msg),
                        colour = self.colour
                    )
                if (rp_room[1] == 'CATEGORY'):
                    for channel in self.bot.get_channel(rp_room[0]).channels:
                        c_pin = await channel.send( embed = c_embed)
                        print(rp_room[0],rp_room[1],rp_room[2],rp_room[3])
                        if rp_room[3] == "NO":
                            continue
                        await c_pin.pin()
                else :
                    c_pin = await self.bot.get_channel(rp_room[0]).send(embed = c_embed)
                    if rp_room[3] == "NO":
                        continue
                    await c_pin.pin()
        except Exception as error:
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'weekly_reset',error)
            c_embed = discord.Embed(title = "An Error Occured",
                description = 'Error : {}\n---\n{}'.format(error,self.join_us_msg),
                colour = self.colour
                )
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif") 
            await ctx.send(file = c_file, embed = c_embed)
        return

def setup(bot):
    bot.add_cog(Weekly_Reset(bot))
