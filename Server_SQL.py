import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import os
import sqlite3

def is_owner():
    def predicate(ctx):
        return (ctx.guild.owner.id == ctx.author.id or 319199396724211722 == ctx.author.id)
    return commands.check(predicate)

def is_JTexpo():
    def predicate(ctx):
        return 319199396724211722 == ctx.author.id
    return commands.check(predicate)

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

class Server_SQL(commands.Cog):
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
            # // -- Creating an Instance of a File and Setting it to the Thumbnail -- //
            # // -- Sending the Embed -- //
            await self.bot.get_channel(696027589827100792).send(embed = log_embed)
        except Exception as error:
            # // -- Printing What Went Wrong to the Shell -- // 
            print("Error Occured : [{}]".format(error))
        return
    # // -- MANUAL SQL FOR QUICK FIXES -- //
    @commands.command(name = 'SQL_Manual',
                      aliases = ['sql_man'])
    @is_JTexpo()
    async def SQL_Manual(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'SQL_Manual')

        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        
        conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
        c = conn.cursor()
        c_embed = discord.Embed(title = "Please Write Out The SQL Command, Be Careful",
                description = "This command is only useable by JTexpo",
                colour = self.colour
                )
        await ctx.send(embed = c_embed)
        in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
        c.execute(in_msg.content)
        conn.commit()
        conn.close()
        c_embed = discord.Embed(title = "Everything Went Well Sucessfully",
                description = "You Wrote : `{}`".format(in_msg.content),
                colour = self.colour
                )
        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
        await ctx.send(file = c_file, embed = c_embed)
        
    # // -- Command Tip -- //
    def command_tip(self, command):
        if command == 'room_type':
            return 'Please Type Either `CATEGORY` or `CHANNEL`'
        elif command == 'title':
            return 'Please Type A Nickname For This Item\nEx : Moderator, Favorite-Channel, READ-THIS'
        elif command == 'pin_reset':
            return 'Please Type Either `YES` or `NO`'
        return ''
                    
    # CODE FOR THE MANAGE COG FOUND BELOW ---------------------------------------------
    @commands.command(name = 'add_to_server_database_table',
                      aliases = ['add_to_server_db_table','atsdbt'])
    @is_admin()
    async def add_to_server_database_table(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'add_to_server_database')

        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        
        try:
            conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
            c = conn.cursor()
            c.execute("""SELECT name FROM sqlite_master
                    WHERE type='table'
                    ORDER BY name;""")
            my_tables = c.fetchall()
            index = 1
            table_dict = {}
            c_msg = ''
            sql_c_msg = 'INSERT INTO '
            for table in my_tables:
                table_dict[index] = table[0]
                c_msg += "{} : {}\n".format(index,table[0])
                index += 1
            c_embed = discord.Embed(title = "Please Select The Number Of The Table You Wish To Add To",
                description = c_msg,
                colour = self.colour
                )
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await ctx.send(file = c_file, embed = c_embed)
            
            in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
            sql_c_msg += " {} VALUES( ".format(table_dict[int(in_msg.content)])
            c.execute("PRAGMA table_info({});".format(table_dict[int(in_msg.content)]))
            collumns = c.fetchall()
            c_embed = discord.Embed(title = "Loading...",
                colour = self.colour
                )
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            c_out_msg = await ctx.send(file = c_file, embed = c_embed)
            
            backComma = False
            for collumn in collumns:
                
                if backComma:
                    sql_c_msg += ','
                backComma = True
                
                if collumn[1] == 'db_ID':
                    sql_c_msg += " NULL "
                    continue
                if collumn[1] == 'author_ID':
                    sql_c_msg += " {} ".format(ctx.author.id)
                    continue

                c_tip = self.command_tip(collumn[1])
                c_embed = discord.Embed(title = "Please Type The {}".format(collumn[1]),
                    description = c_tip,
                    colour = self.colour
                    )
                c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
                await c_out_msg.edit(embed = c_embed)
                
                in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                if "VARCHAR" in collumn[2]:
                    sql_c_msg += ' "{}" '.format(in_msg.content)
                else : sql_c_msg += ' {} '.format(in_msg.content)
            sql_c_msg += " );"
            c.execute(sql_c_msg)
            conn.commit()
            conn.close()
            c_embed = discord.Embed(title = "Everything Went Well Sucessfully",
                description = "You Wrote : `{}`".format(sql_c_msg),
                colour = self.colour
                )
        except Exception as error:
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'add_to_server_database',error)
            # // -- Notify The User -- //
            c_embed = discord.Embed(title = "An Error Occured",
                description = 'Error : {}\n---\n{}'.format(error,self.join_us_msg),
                colour = self.colour
                )
        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif") 
        await ctx.send(file = c_file, embed = c_embed)
        return

    
    @commands.command(name = 'register_server',
                      aliases = ['rs'])
    @is_owner()
    async def register_server(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'register_server')
        try :
            # // -- Getting Current Working Directory -- //
            cwd = os.getcwd()
            # // -- Checking If The Directory Exists -- //
            isdir = os.path.isdir(cwd + '/servers/' + str(ctx.guild.id))
            if (isdir == False):
                # // -- If Not, Make The Directory -- //
                os.mkdir(cwd + '/servers/' + str(ctx.guild.id))
                c_msg = 'Server Is Registered!'
                        ### SETTING UP THE SERVER DATA BASE ###
                # // -- Creating The SQLite3 Databases For The Server-- //
                conn = sqlite3.connect(cwd + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
                c = conn.cursor()
                # // -- Creating The admin_table -- //
                sql_cmd = open("resources/admin_table_ref.txt",'r').read()
                c.execute(sql_cmd)
                    # // -- Adding the Owner to the Admins Table -- //
                c.execute("""INSERT INTO admin_table
                            VALUES (NULL, {}, "OWNER");""".format(ctx.author.id))
                    # // -- Adding Me to the Admins Table (Help config to server) -- //
                if (ctx.author.id != 319199396724211722):
                    c.execute("""INSERT INTO admin_table
                            VALUES (NULL, 319199396724211722, "DEVELOPER");""")
                # // -- Creating weekly_reset_msg_table -- //
                sql_cmd = open("resources/reset_msg_table_ref.txt",'r').read()
                c.execute(sql_cmd)
                    # // -- Adding 1 reset message as a default -- //
                c.execute("""INSERT INTO reset_msg_table
                            VALUES (NULL, {}, "RP Room Reset!");""".format(ctx.author.id))
                # // -- Creating rp_room_table -- //
                sql_cmd = open("resources/rp_room_table_ref.txt",'r').read()
                c.execute(sql_cmd)
                # // -- Creating resource_table -- //
                sql_cmd = open("resources/resource_table_ref.txt",'r').read()
                c.execute(sql_cmd)
                # // -- Creating The flag_message_table -- //
                sql_cmd = open("resources/flag_message_table_ref.txt",'r').read()
                c.execute(sql_cmd)
                # // -- Creating The char_table -- //
                sql_cmd = open("resources/char_table_ref.txt",'r').read()
                c.execute(sql_cmd)
                # // -- Creating The ichannel -- //
                sql_cmd = open("resources/ichannel_table_ref.txt",'r').read()
                c.execute(sql_cmd)
                c.execute("""INSERT INTO ichannel_table
                            VALUES (NULL, {}, "CHAR-CREATE-CATEGORY");""".format(ctx.channel.id))
                c.execute("""INSERT INTO ichannel_table
                            VALUES (NULL, {}, "FLAG-MSG");""".format(ctx.channel.id))
                # // -- Committing & Closing -- //
                conn.commit()
                conn.close()
            else : c_msg = 'Server Is Already Registered!'
            # // -- Confirmation Embed -- //
            c_embed = discord.Embed(title = "{}".format(c_msg),
                    description = self.join_us_msg,
                    colour = self.colour
                    )
        except Exception as error :
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'register_server',error)
            # // -- Notify The User -- //
            c_embed = discord.Embed(title = "An Error Occured",
                description = 'Error : {}\n---\n{}'.format(error,self.join_us_msg),
                colour = self.colour
                )
        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
        await ctx.send(file = c_file, embed = c_embed)
        return

    @commands.command(name = 'show_server_database_table_contents',
                      aliases = ['show_server_db_table_contents','ssdbtc'])
    @is_admin()
    async def show_server_database_table_contents(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'show_server_database_table_contents')

        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        
        try:
            conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
            c = conn.cursor()
            c.execute("""SELECT name FROM sqlite_master
                    WHERE type='table'
                    ORDER BY name;""")
            my_tables = c.fetchall()
            index = 1
            table_dict = {}
            c_msg = ''
            sql_c_msg = ''
            for table in my_tables:
                table_dict[index] = table[0]
                c_msg += "{} : {}\n".format(index,table[0])
                index += 1
            c_embed = discord.Embed(title = "Please Select The Number Of The Table You Wish To See",
                description = c_msg,
                colour = self.colour
                )
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            c_embed.set_footer(text = "PLEASE PLEASE PLEASE DON'T CHOSE CHAR_TABLE")
            await ctx.send(file = c_file, embed = c_embed)
    
            in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
            c.execute("SELECT * FROM {}".format(table_dict[int(in_msg.content)]))
            # // -- Getting the contents of the table -- //
            contents = c.fetchall()
            # // -- getting how many rows there are -- //
            total_rows = len(contents)
            # // -- getting how mayn elements there are --//
            total_elements = len(contents[0])
            # // -- making a list of 0, to then figure out the longest char for table formating -- //
            longest_char_list = [0]*total_elements
            # // -- itterating through the elemens of each row, row is the changing varible -- //
            for e in range(total_elements):
                for r in range(total_rows):
                    longest_char_list[e] = len(str(contents[r][e])) if len(str(contents[r][e])) > longest_char_list[e] else longest_char_list[e]
            # // -- creating a message to print the table -- //
            c_msg = ''
            for row in contents:
                index = 0
                for element in row:
                    # // -- dividing the message into parts -- //
                    if (index != 0) : c_msg += ' | '
                    c_msg += "{}".format(element).ljust(longest_char_list[index])
                    index += 1
                c_msg += "\n"
            # // -- Confirmation Embed -- //
            while len(c_msg) > 1800:
                c_embed = discord.Embed(title = "SQL Table Of {}".format(table_dict[int(in_msg.content)]),
                        description = "```"+c_msg[:1800]+"```",
                        colour = self.colour
                        )
                c_msg = c_msg[1800:]
                await ctx.send(embed = c_embed)
            c_embed = discord.Embed(title = "SQL Table Of {}".format(table_dict[int(in_msg.content)]),
                    description = "```"+c_msg[:1800]+"```",
                    colour = self.colour
                    )
        except Exception as error:
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'add_to_server_database',error)
            # // -- Notify The User -- //
            c_embed = discord.Embed(title = "An Error Occured",
                description = 'Error : {}\n---\n{}'.format(error,self.join_us_msg),
                colour = self.colour
                )
        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
        await ctx.send(file = c_file, embed = c_embed)
        return



    @commands.command(name = 'update_server_database_table',
                      aliases = ['update_server_db_table','usdbt'])
    @is_admin()
    async def update_server_database_table(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'update_server_database_table')

        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        
        try:
            conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
            c = conn.cursor()
            c.execute("""SELECT name FROM sqlite_master
                    WHERE type='table'
                    ORDER BY name;""")
            my_tables = c.fetchall()
            index = 1
            table_dict = {}
            c_msg = ''
            sql_c_msg = 'UPDATE '
            for table in my_tables:
                table_dict[index] = table[0]
                c_msg += "{} : {}\n".format(index,table[0])
                index += 1
            c_embed = discord.Embed(title = "Please Select The Number Of The Table You Wish To Add To",
                description = c_msg,
                colour = self.colour
                )
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await ctx.send(file = c_file, embed = c_embed)
            
            in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
            c.execute("SELECT * FROM {}".format(table_dict[int(in_msg.content)]))
            current = c.fetchall()
            sql_c_msg += " {} SET ".format(table_dict[int(in_msg.content)])
            c.execute("PRAGMA table_info({});".format(table_dict[int(in_msg.content)]))
            collumns = c.fetchall()
            c_embed = discord.Embed(title = "Please Type The Database ID You Want To Update",
                colour = self.colour
                )
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            c_out_msg = await ctx.send(file = c_file, embed = c_embed)
            
            in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
            sql_c_msg_end_part = ' WHERE db_ID = {};'.format(in_msg.content)
            index = 0
            elm = int(in_msg.content)-1
            for collumn in collumns:                
                if collumn[1] == 'db_ID':
                    continue
                
                if index != 0:
                    sql_c_msg += ','
                index += 1
                                
                if collumn[1] == 'author_ID':
                    sql_c_msg += " author_ID = {} ".format(ctx.author.id)
                    continue
                
                c_tip = self.command_tip(str(collumn[1]))
                c_embed = discord.Embed(title = "Please Type The {}".format(collumn[1]),
                    description = "{}\n---\nCurrently : {}".format(c_tip,current[elm][index]),
                    colour = self.colour
                    )
                c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
                await c_out_msg.edit(embed = c_embed)
                in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                if "VARCHAR" in collumn[2]:
                    sql_c_msg += ' {} = "{}" '.format(collumn[1], in_msg.content)
                else : sql_c_msg += ' {} = {} '.format(collumn[1], in_msg.content)
            sql_c_msg += sql_c_msg_end_part
            c.execute(sql_c_msg)
            conn.commit()
            conn.close()
            c_embed = discord.Embed(title = "Everything Went Well Sucessfully",
                description = "You Wrote : `{}`".format(sql_c_msg),
                colour = self.colour
                )
            
        except Exception as error:
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'add_to_server_database',error)
            # // -- Notify The User -- //
            c_embed = discord.Embed(title = "An Error Occured",
                description = 'Error : {}\n---\n{}'.format(error,self.join_us_msg),
                colour = self.colour
                )
        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
        await ctx.send(file = c_file, embed = c_embed)
        return


    
def setup(bot):
    bot.add_cog(Server_SQL(bot))
