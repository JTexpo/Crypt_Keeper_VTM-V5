import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import os
import sqlite3
import random

def is_char():
    def predicate(ctx):
        conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
        c = conn.cursor()
        c.execute("SELECT player_id FROM char_table")
        chars = c.fetchall()
        for char in chars:
            if (ctx.author.id in char) : return True
        return False
    return commands.check(predicate)

class Character_Manager(commands.Cog):
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

    

    @commands.command(name = 'active_character',
                     aliases = ['active'])
    @is_char()
    async def active_character(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'active_character')
       
        def check_message(message):
           return ((message.author == ctx.author) and (message.channel == ctx.channel))
       
        try:
            conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
            c = conn.cursor()
            c.execute('SELECT db_ID,name,active_char FROM char_table WHERE player_id = {}'.format(ctx.author.id))
            contentsTuple = c.fetchall()
            def f(t):
                if type(t) == list or type(t) == tuple:
                    return [f(i) for i in t]
                return t
            contents = f(contentsTuple)
            # // -- getting how many rows there are -- //
            total_rows = len(contents)
            # // -- getting how mayn elements there are --//
            total_elements = len(contents[0])
            # // -- making a list of 0, to then figure out the longest char for table formating -- //
            longest_char_list = [2,4,6]
            # // -- itterating through the elemens of each row, row is the changing varible -- //
            for e in range(total_elements):
                for r in range(total_rows):
                    longest_char_list[e] = len(str(contents[r][e])) if len(str(contents[r][e])) > longest_char_list[e] else longest_char_list[e]
            # // -- creating a message to print the table -- //
            c_msg = ''
            c_msg += "ID".ljust(longest_char_list[0]) + ' | ' + "name".ljust(longest_char_list[1]) + ' | ' "active".ljust(longest_char_list[2]) + '\n'
            for row in contents:
                index = 0
                for element in row:
                    # // -- dividing the message into parts -- //
                    if (index != 0) : c_msg += ' | '
                    c_msg += "{}".format(element).ljust(longest_char_list[index])
                    index += 1
                c_msg += "\n"
           
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Please Select Your Character's ID <:Crypt_Keeper:694324654227062825>",
                description = "```"+c_msg+"```",
                colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await ctx.send(file = c_file, embed = c_embed)
            for row in contents:
                row[2] = 0
            while True:
                in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                for row in contents:
                    if int(in_msg.content) == int(row[0]):
                        row[2] = 1
                        for char in contents:
                            c.execute("UPDATE char_table SET active_char = {} WHERE db_ID = {}".format(char[2],char[0]))
                        conn.commit()
                        conn.close()
                        c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Switched Character to {} <:Crypt_Keeper:694324654227062825>".format(row[1]),
                                        description = "",
                        colour = self.colour)
                        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
                        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
                        await ctx.send(file = c_file, embed = c_embed)
                        return
        except Exception as error:
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'active_character',error)
            # // -- Notify The User -- //
            c_embed = discord.Embed(title = "An Error Occured",
               description = 'Error : {}\n---\n{}'.format(error,self.join_us_msg),
               colour = self.colour
               )
        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
        await ctx.send(file = c_file, embed = c_embed)
        return
       
    @commands.command(name = 'update_character',
                         aliases = ['edit_character'])
    @is_char()
    async def update_character(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'update_character')
        
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Please Type The Numbder Of What You Would Like To Edit<:Crypt_Keeper:694324654227062825>",
           description = """**1** : Appearance 
**2** : Attributes
**3** : Backstory
**4** : Bane
**5** : Discipline
**6** : Experience / Spent Experience 
**7** : Flaws
**8** : General Information
**9** : Merits
**10** : Notes
**11** : Resonance
**12** : Skills
**13** : Specialities
**14** : Tenents
**15** : Touchstones & Convictions
**16** : Willpower/Health/Humanity/Hunger
""",
           colour = self.colour)
        
        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
        await ctx.send(file = c_file, embed = c_embed)
        in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
        if int(in_msg.content) == 1: await self.manage_appearance(ctx)
        elif int(in_msg.content) == 2: await self.manage_attributes(ctx)
        elif int(in_msg.content) == 3: await self.manage_field(ctx,'backstory')
        elif int(in_msg.content) == 4: await self.manage_field(ctx,'ban')
        elif int(in_msg.content) == 5: await self.manage_discipline(ctx)
        elif int(in_msg.content) == 6: await self.manage_experience(ctx)
        elif int(in_msg.content) == 7: await self.manage_field(ctx,'flaws')
        elif int(in_msg.content) == 8: await self.manage_general(ctx)
        elif int(in_msg.content) == 9: await self.manage_field(ctx,'merits')
        elif int(in_msg.content) == 10: await self.manage_field(ctx,'notse')
        elif int(in_msg.content) == 11: await self.manage_field(ctx,'resonance')
        elif int(in_msg.content) == 12: await self.manage_skills(ctx)
        elif int(in_msg.content) == 13: await self.manage_field(ctx,'specialties')
        elif int(in_msg.content) == 14: await self.manage_field(ctx,'tenents')
        elif int(in_msg.content) == 15: await self.manage_field(ctx,'touchstones')
        elif int(in_msg.content) == 16: await self.manage_whhh(ctx)
        
    async def manage_appearance(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'manage_appearance')
        
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        
        def appearance_embed(dic,msg, name):
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Appearance Information About {} <:Crypt_Keeper:694324654227062825>".format(name),
                            description = msg,
                            colour = self.colour)
            c_embed.add_field(name = "True Age :", value = dic["TRUE_AGE"], inline = True)
            c_embed.add_field(name = "Apparent Age :", value = dic["APPARENT_AGE"], inline = True)
            c_embed.add_field(name = "\u200b", value = "\u200b", inline = False)
            c_embed.add_field(name = "Data of Birth :", value = dic["DATE_OF_BIRTH"], inline = True)
            c_embed.add_field(name = "Date of Death :", value = dic["DATE_OF_DEATH"], inline = True)
            c_embed.add_field(name = "\u200b", value = "\u200b", inline = False)
            c_embed.add_field(name = "Picture Link :", value = dic["PICTURE"], inline = True)
            
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")

            return c_embed

        app_dict = {"TRUE_AGE" : "",
                    "APPARENT_AGE" : "",
                    "DATE_OF_BIRTH" : "",
                    "DATE_OF_DEATH" : "",
                    "PICTURE" : ""
                    }
        try:
            conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
            c = conn.cursor()
            
            sql_cmd = 'SELECT db_ID, name'
            for key in app_dict:
                sql_cmd += ', {}'.format(key.lower())
            sql_cmd += ' FROM char_table WHERE player_id = {} AND active_char = 1'.format(ctx.author.id)
            c.execute(sql_cmd)
            char = c.fetchone()
            
            index = 2
            for key in app_dict:
                app_dict[key] = char[index]
                index += 1

            c_embed = discord.Embed(title = "Loading...",colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            refresh_c_msg = await ctx.send(file = c_file, embed = c_embed)
            while True:
                e_msg = "Please Write The **Name Of The Appearance** You Wish To Edit.\n`If you are done type 0`"
                c_embed = appearance_embed(app_dict, e_msg, char[1])
                await refresh_c_msg.edit(embed = c_embed)
                in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                if in_msg.content.upper() in att_dict:
                    e_msg = "Please **Write The New** **__{}__**.\n`If you are done type 0`".format(in_msg.content.upper())
                    c_embed = appearance_embed(app_dict, e_msg, char[1])
                    await refresh_c_msg.edit(embed = c_embed)
                    in_msg2 = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                    try :
                        if int(in_msg2.content) == 0:
                            break
                    except:
                        pass
                    app_dict[in_msg.content.upper()] = in_msg2
                try:
                    if int(in_msg.content) == 0:
                        break
                except:
                    pass
            sql_cmd = 'UPDATE char_table SET'
            comma = False
            for key in app_dict:
                if comma == True:
                    sql_cmd += ','
                comma = True
                sql_cmd += ' {} = {}'.format(key.lower(),app_dict[key])
            sql_cmd += ' WHERE db_ID = {}'.format(char[0])
            c.execute(sql_cmd)
            conn.commit()
            conn.close()
            c_embed = discord.Embed(title = "Everything Was Changed successfully",
                    colour = self.colour)
        except Exception as error:
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'manage_appearance',error)
            # // -- Notify The User -- //
            c_embed = discord.Embed(title = "An Error Occured",
                description = 'Error : {}\n---\n{}'.format(error,self.join_us_msg),
                colour = self.colour
                )
        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
        await ctx.send(file = c_file, embed = c_embed)
        return


    
    async def manage_attributes(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'manage_attributes')
        
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        
        def attributes_embed(dic,msg, name):
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Attribute Information About {} <:Crypt_Keeper:694324654227062825>".format(name),
                            description = msg,
                            colour = self.colour)
            c_embed.add_field(name = "Strength :", value = ("<:closed_dot:696077251854336062>"*dic["STRENGTH"]+"<:open_dot:696077251829170236>"*(5-dic["STRENGTH"])), inline = True)
            c_embed.add_field(name = "Charisma :", value = ("<:closed_dot:696077251854336062>"*dic["CHARISMA"]+"<:open_dot:696077251829170236>"*(5-dic["CHARISMA"])), inline = True)
            c_embed.add_field(name = "Intelligence :", value = ("<:closed_dot:696077251854336062>"*dic["INTELLIGENCE"]+"<:open_dot:696077251829170236>"*(5-dic["INTELLIGENCE"])), inline = True)
            c_embed.add_field(name = "\u200b", value = "\u200b", inline = False)
            c_embed.add_field(name = "Dexterity :", value = ("<:closed_dot:696077251854336062>"*dic["DEXTERITY"]+"<:open_dot:696077251829170236>"*(5-dic["DEXTERITY"])), inline = True)
            c_embed.add_field(name = "Manipulation :", value = ("<:closed_dot:696077251854336062>"*dic["MANIPULATION"]+"<:open_dot:696077251829170236>"*(5-dic["MANIPULATION"])), inline = True)
            c_embed.add_field(name = "Wits :", value = ("<:closed_dot:696077251854336062>"*dic["WITS"]+"<:open_dot:696077251829170236>"*(5-dic["WITS"])), inline = True)
            c_embed.add_field(name = "\u200b", value = "\u200b", inline = False)
            c_embed.add_field(name = "Stamina :", value = ("<:closed_dot:696077251854336062>"*dic["STAMINA"]+"<:open_dot:696077251829170236>"*(5-dic["STAMINA"])), inline = True)
            c_embed.add_field(name = "Composure :", value = ("<:closed_dot:696077251854336062>"*dic["COMPOSURE"]+"<:open_dot:696077251829170236>"*(5-dic["COMPOSURE"])), inline = True)
            c_embed.add_field(name = "Resolve :", value = ("<:closed_dot:696077251854336062>"*dic["RESOLVE"]+"<:open_dot:696077251829170236>"*(5-dic["RESOLVE"])), inline = True)

            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")

            return c_embed
            
        att_dict = {"STRENGTH":1,
            "DEXTERITY":1,
            "STAMINA":1,
            "CHARISMA":1,
            "MANIPULATION":1,
            "COMPOSURE":1,
            "INTELLIGENCE":1,
            "WITS":1,
            "RESOLVE":1}
        
        try:
            conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
            c = conn.cursor()
            
            sql_cmd = 'SELECT db_ID, name'
            for key in att_dict:
                sql_cmd += ', {}'.format(key.lower())
            sql_cmd += ' FROM char_table WHERE player_id = {} AND active_char = 1'.format(ctx.author.id)
            c.execute(sql_cmd)
            char = c.fetchone()
            
            index = 2
            for key in att_dict:
                att_dict[key] = char[index]
                index += 1
            
            c_embed = discord.Embed(title = "Loading...",colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            refresh_c_msg = await ctx.send(file = c_file, embed = c_embed)
            exit_loop = False
            while True:
                e_msg = "Please Write The **Name Of The Attribute** You Wish To Edit.\n`If you are done type 0`"
                c_embed = attributes_embed(att_dict, e_msg, char[1])
                await refresh_c_msg.edit(embed = c_embed)
                in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                if in_msg.content.upper() in att_dict:
                    e_msg = "Please Type The **New Number** **__{}__** should be Be.\n`If you are done type 0`".format(in_msg.content.upper())
                    while True:
                        c_embed = attributes_embed(att_dict, e_msg, char[1])
                        await refresh_c_msg.edit(embed = c_embed)
                        in_msg_2 = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                        try:
                            if int(in_msg_2.content) == 0:
                                exit_loop = True
                                break
                            elif int(in_msg_2.content) > 0 and int(in_msg_2.content) < 6:
                                break
                        except:
                            pass
                    if exit_loop == True:
                        break
                    att_dict[in_msg.content.upper()] = int(in_msg_2.content)
                try:
                    if int(in_msg.content) == 0:
                        break
                except:
                    pass
            sql_cmd = 'UPDATE char_table SET'
            comma = False
            for key in att_dict:
                if comma == True:
                    sql_cmd += ','
                comma = True
                sql_cmd += ' {} = {}'.format(key.lower(),att_dict[key])
            sql_cmd += ' WHERE db_ID = {}'.format(char[0])
            c.execute(sql_cmd)
            conn.commit()
            conn.close()
            c_embed = discord.Embed(title = "Everything Was Changed successfully",
                    colour = self.colour)
        except Exception as error:
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'manage_attribute',error)
            # // -- Notify The User -- //
            c_embed = discord.Embed(title = "An Error Occured",
                description = 'Error : {}\n---\n{}'.format(error,self.join_us_msg),
                colour = self.colour
                )
        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
        await ctx.send(file = c_file, embed = c_embed)
        return

    async def manage_discipline(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'manage_experience')
        
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))

        def make_msg(d_dic,p_dic,f_dic,msg = ''):
            for key,value in d_dic.items():
                msg += '{} : {} :'.format(key, value)
                msg += '<:closed_dot:696077251854336062>'*p_dic[key+'_P'] + "<:open_dot:696077251829170236>"*(5-p_dic[key+'_P'])
                msg += '\n'
                for i in range(5):
                    msg += '**{}** : {}\n'.format(i+1,f_dic[key+'_{}'.format(i+1)])
            return msg
                
        dis_name_dic = {}
        dis_point_dic = {}
        dis_field_dic = {}
        try:
            conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
            c = conn.cursor()
            
            sql_cmd = 'SELECT db_ID, name'
            for i in range(6):
                sql_cmd += ', discipline_{}'.format(i+1)
                dis_name_dic['DISCIPLINE_{}'.format(i+1)] = 0
            sql_cmd += ' FROM char_table WHERE player_id = {} AND active_char = 1'.format(ctx.author.id)
            c.execute(sql_cmd)
            char = c.fetchone()
            
            index = 2
            for key in dis_name_dic:
                dis_name_dic[key] = char[index]
                index += 1

            sql_cmd = 'SELECT db_ID, name'
            for i in range(6):
                sql_cmd += ', discipline_{}_p'.format(i+1)
                dis_point_dic['DISCIPLINE_{}_P'.format(i+1)] = 0
            sql_cmd += ' FROM char_table WHERE player_id = {} AND active_char = 1'.format(ctx.author.id)
            c.execute(sql_cmd)
            char = c.fetchone()
            
            index = 2
            for key in dis_point_dic:
                dis_point_dic[key] = char[index]
                index += 1

            sql_cmd = 'SELECT db_ID, name'
            for i in range(6):
                for x in range(5):
                    sql_cmd += ', discipline_{}_{}'.format(i+1,x+1)
                    dis_field_dic['DISCIPLINE_{}_{}'.format(i+1,x+1)] = 0
            sql_cmd += ' FROM char_table WHERE player_id = {} AND active_char = 1'.format(ctx.author.id)
            c.execute(sql_cmd)
            char = c.fetchone()
            
            index = 2
            for key in dis_field_dic:
                dis_field_dic[key] = char[index]
                index += 1

            c_embed = discord.Embed(title = "Loading...",colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            refresh_c_msg = await ctx.send(file = c_file, embed = c_embed)
            exit_loop = False
            while True:
                e_msg = "Please Write The **Name Of The Discipline As Such**\n`discipline_1`\n`discipline_2`\n`discipline_#.\n`If you are done type 0`\n"
                e_msg = make_msg(dis_name_dic,dis_point_dic,dis_field_dic,e_msg)
                c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Disciplines For {} <:Crypt_Keeper:694324654227062825>".format(char[1]),
                        description = e_msg,
                        colour = self.colour)
                c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
                await refresh_c_msg.edit(embed = c_embed)
                in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                if in_msg.content.upper() in dis_name_dic:
                    while True:
                        e_msg = "Please **Type The Number** You Wish To Edit In {}. If You Want It Empty Please Write `None`\nIf You Want To Change The Name Please **Write The New Name Of The Discipline**.\n".format(in_msg.content)
                        e_msg = make_msg(dis_name_dic,dis_point_dic,dis_field_dic,e_msg)
                        c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Disciplines For {} <:Crypt_Keeper:694324654227062825>".format(char[1]),
                                description = e_msg,
                                colour = self.colour)
                        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
                        await refresh_c_msg.edit(embed = c_embed)
                        in_msg2 = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                        try:
                            if int(in_msg2.content) == 0:
                                exit_loop == True
                                break
                            elif int(in_msg2.content) > 0 and int(in_msg2.content) < 6:
                                e_msg = "Please **Wite The New Field** You Wish To Edit In {}. If You Want It Empty Please Write `None`.\n".format(in_msg.content+'_'+in_msg2.content)
                                e_msg = make_msg(dis_name_dic,dis_point_dic,dis_field_dic,e_msg)
                                c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Disciplines For {} <:Crypt_Keeper:694324654227062825>".format(char[1]),
                                        description = e_msg,
                                        colour = self.colour)
                                c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
                                await refresh_c_msg.edit(embed = c_embed)
                                in_msg3 = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                                dis_field_dic[in_msg.content.upper()+'_'+in_msg2.content] = in_msg3.content
                                points = 5
                                for i in range(5):
                                    if dis_field_dic[in_msg.content.upper()+'_'+str(i+1)].upper() == 'NONE':
                                        points -= 1
                                dis_point_dic[in_msg.content.upper()+'_P'] = points
                                break
                        except Exception as e:
                            dis_name_dic[in_msg.content.upper()] = in_msg2.content
                            break
                if exit_loop == True:
                    break
                try:
                    if int(in_msg.content) == 0:
                        break
                except:
                    pass
                
            sql_cmd = 'UPDATE char_table SET'
            comma = False
            for key in dis_name_dic:
                if comma == True:
                    sql_cmd += ','
                comma = True
                sql_cmd += ' {} = "{}"'.format(key.lower(),dis_name_dic[key])
            for key in dis_field_dic:
                sql_cmd += ', {} = "{}"'.format(key.lower(),dis_field_dic[key])
            for key in dis_point_dic:
                sql_cmd += ', {} = {}'.format(key.lower(),dis_point_dic[key])
            sql_cmd += ' WHERE db_ID = {}'.format(char[0])
            c.execute(sql_cmd)
            conn.commit()
            conn.close()
            c_embed = discord.Embed(title = "Everything Was Changed successfully",
                    colour = self.colour)
        except Exception as error:
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'manage_appearance',error)
            # // -- Notify The User -- //
            c_embed = discord.Embed(title = "An Error Occured",
                description = 'Error : {}\n---\n{}'.format(error,self.join_us_msg),
                colour = self.colour
                )
        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
        await ctx.send(file = c_file, embed = c_embed)
        return
    
        
    async def manage_experience(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'manage_experience')
        
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))

        def experience_embed(dic,msg, name):
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Experience Information About {} <:Crypt_Keeper:694324654227062825>".format(name),
                            description = msg,
                            colour = self.colour)
            c_embed.add_field(name = "Experience :", value = dic["EXPERIENCE"], inline = True)
            c_embed.add_field(name = "Spend_Experience :", value = dic["SPEND_EXPERIENCE"], inline = True)
            
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")

            return c_embed

        exp_dict = {"EXPERIENCE" : "",
            "SPEND_EXPERIENCE" : ""
            }
        
        try:
            conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
            c = conn.cursor()
            
            sql_cmd = 'SELECT db_ID, name'
            for key in exp_dict:
                sql_cmd += ', {}'.format(key.lower())
            sql_cmd += ' FROM char_table WHERE player_id = {} AND active_char = 1'.format(ctx.author.id)
            c.execute(sql_cmd)
            char = c.fetchone()
            
            index = 2
            for key in exp_dict:
                att_dict[key] = char[index]
                index += 1
            
            c_embed = discord.Embed(title = "Loading...",colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            refresh_c_msg = await ctx.send(file = c_file, embed = c_embed)
            exit_loop = False
            while True:
                e_msg = "Please Write The **Field** You Wish To Edit.\n`If you are done type 0`"
                c_embed = attributes_embed(exp_dict, e_msg, char[1])
                await refresh_c_msg.edit(embed = c_embed)
                in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                if in_msg.content.upper() in att_dict:
                    e_msg = "Please Type The **New Number** **__{}__** should be Be.\n`If you are done type 0`".format(in_msg.content.upper())
                    while True:
                        c_embed = attributes_embed(exp_dict, e_msg, char[1])
                        await refresh_c_msg.edit(embed = c_embed)
                        in_msg_2 = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                        try:
                            if int(in_msg_2.content) == 0:
                                exit_loop = True
                                break
                            elif int(in_msg_2.content) > 0:
                                break
                        except:
                            pass
                    if exit_loop == True:
                        break
                    exp_dict[in_msg.content.upper()] = int(in_msg_2.content)
                try:
                    if int(in_msg.content) == 0:
                        break
                except:
                    pass
            sql_cmd = 'UPDATE char_table SET'
            comma = False
            for key in exp_dict:
                if comma == True:
                    sql_cmd += ','
                comma = True
                sql_cmd += ' {} = {}'.format(key.lower(),exp_dict[key])
            sql_cmd += ' WHERE db_ID = {}'.format(char[0])
            c.execute(sql_cmd)
            conn.commit()
            conn.close()
            c_embed = discord.Embed(title = "Everything Was Changed successfully",
                    colour = self.colour)
        except Exception as error:
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'manage_attribute',error)
            # // -- Notify The User -- //
            c_embed = discord.Embed(title = "An Error Occured",
                description = 'Error : {}\n---\n{}'.format(error,self.join_us_msg),
                colour = self.colour
                )
        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
        await ctx.send(file = c_file, embed = c_embed)
        return
        
    
    async def manage_field(self,ctx,field):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'manage_field : {}'.format(field))
        
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))

        try:
            conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
            c = conn.cursor()
            c.execute('SELECT db_ID, name, {} FROM char_table WHERE player_id = {} AND active_char = 1'.format(field,ctx.author.id))
            char = c.fetchone()
            
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> {}'s {} <:Crypt_Keeper:694324654227062825>".format(char[1],field),
                    description = "__Currently :__\n"+char[2],
                    colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await ctx.send(file = c_file, embed = c_embed)
            in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
            c.execute('UPDATE char_table SET {} = "{}" WHERE db_ID = {}'.format(field,in_msg.content,char[0]))
            conn.commit()
            conn.close()
            c_embed = discord.Embed(title = "Everything Was Changed successfully",
                colour = self.colour)
        except Exception as error:
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'manage_field : {}'.format(field),error)
            # // -- Notify The User -- //
            c_embed = discord.Embed(title = "An Error Occured",
                description = 'Error : {}\n---\n{}'.format(error,self.join_us_msg),
                colour = self.colour
                )
        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
        await ctx.send(file = c_file, embed = c_embed)
        return
            
    async def manage_general(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'manage_general')
        
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))

        def general_embed(dic,msg,name):
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> General Information About {} <:Crypt_Keeper:694324654227062825>".format(name),
                            description = msg,
                            colour = self.colour)
            c_embed.add_field(name = "Name :", value = dic["NAME"], inline = True)
            c_embed.add_field(name = "Concept :", value = dic["CONCEPT"], inline = True)
            c_embed.add_field(name = "Sire :", value = dic["SIRE"], inline = True)

            c_embed.add_field(name = "\u200b", value = "\u200b", inline = False)
            
            c_embed.add_field(name = "Player :", value = ctx.author.name, inline = True)
            c_embed.add_field(name = "Ambition :", value = dic["AMBITION"], inline = True)
            c_embed.add_field(name = "Clan :", value = dic["CLAN"], inline = True)

            c_embed.add_field(name = "\u200b", value = "\u200b", inline = False)

            c_embed.add_field(name = "Chronicle :", value = ctx.guild.name, inline = True)
            c_embed.add_field(name = "Predator :", value = dic["PREDATOR"], inline = True)
            c_embed.add_field(name = "Generation :", value = dic["GENERATION"], inline = True)

            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")

            return c_embed

        gen_dict = {"NAME" : "",
                    "CONCEPT" : "",
                    "SIRE" : "",
                    "AMBITION" : "",
                    "CLAN" : "",
                    "PREDATOR" : "",
                    "GENERATION" : ""
                    }
        try:
            conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
            c = conn.cursor()
            
            sql_cmd = 'SELECT db_ID, name'
            for key in gen_dict:
                sql_cmd += ', {}'.format(key.lower())
            sql_cmd += ' FROM char_table WHERE player_id = {} AND active_char = 1'.format(ctx.author.id)
            c.execute(sql_cmd)
            char = c.fetchone()
            
            index = 2
            for key in gen_dict:
                app_dict[key] = char[index]
                index += 1

            c_embed = discord.Embed(title = "Loading...",colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            refresh_c_msg = await ctx.send(file = c_file, embed = c_embed)
            while True:
                e_msg = "Please Write The **Name Of The General Information** You Wish To Edit.\n`If you are done type 0`"
                c_embed = general_embed(gen_dict, e_msg, char[1])
                await refresh_c_msg.edit(embed = c_embed)
                in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                if in_msg.content.upper() in att_dict:
                    e_msg = "Please **Write The New** **__{}__**.\n`If you are done type 0`".format(in_msg.content.upper())
                    c_embed = general_embed(gen_dict, e_msg, char[1])
                    await refresh_c_msg.edit(embed = c_embed)
                    in_msg2 = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                    try :
                        if int(in_msg2.content) == 0:
                            break
                    except:
                        pass
                    gen_dict[in_msg.content.upper()] = in_msg2
                try:
                    if int(in_msg.content) == 0:
                        break
                except:
                    pass
            sql_cmd = 'UPDATE char_table SET'
            comma = False
            for key in gen_dict:
                if comma == True:
                    sql_cmd += ','
                comma = True
                sql_cmd += ' {} = {}'.format(key.lower(),gen_dict[key])
            sql_cmd += ' WHERE db_ID = {}'.format(char[0])
            c.execute(sql_cmd)
            conn.commit()
            conn.close()
            c_embed = discord.Embed(title = "Everything Was Changed successfully",
                    colour = self.colour)
        except Exception as error:
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'manage_appearance',error)
            # // -- Notify The User -- //
            c_embed = discord.Embed(title = "An Error Occured",
                description = 'Error : {}\n---\n{}'.format(error,self.join_us_msg),
                colour = self.colour
                )
        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
        await ctx.send(file = c_file, embed = c_embed)
        return
    
        
    async def manage_skills(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'manage_skills')
        
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
            
        def skills_embed(dic, msg, name):
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Skill Information About {} <:Crypt_Keeper:694324654227062825>".format(name),
                            description = msg,
                            colour = self.colour)
            c_embed.add_field(name = "Athletics",value = ("<:closed_dot:696077251854336062>"*dic["ATHLETICS"]+"<:open_dot:696077251829170236>"*(5-dic["ATHLETICS"])), inline = True)
            c_embed.add_field(name = "Animal_ken",value = ("<:closed_dot:696077251854336062>"*dic["ANIMAL_KEN"]+"<:open_dot:696077251829170236>"*(5-dic["ANIMAL_KEN"])), inline = True)
            c_embed.add_field(name = "Academics",value = ("<:closed_dot:696077251854336062>"*dic["ACADEMICS"]+"<:open_dot:696077251829170236>"*(5-dic["ACADEMICS"])), inline = True)
            c_embed.add_field(name = "\u200b", value = "\u200b", inline = False)
            c_embed.add_field(name = "Brawl",value = ("<:closed_dot:696077251854336062>"*dic["BRAWL"]+"<:open_dot:696077251829170236>"*(5-dic["BRAWL"])), inline = True)
            c_embed.add_field(name = "Etiquette",value = ("<:closed_dot:696077251854336062>"*dic["ETIQUETTE"]+"<:open_dot:696077251829170236>"*(5-dic["ETIQUETTE"])), inline = True)
            c_embed.add_field(name = "Awareness",value = ("<:closed_dot:696077251854336062>"*dic["AWARENESS"]+"<:open_dot:696077251829170236>"*(5-dic["AWARENESS"])), inline = True)
            c_embed.add_field(name = "\u200b", value = "\u200b", inline = False)
            c_embed.add_field(name = "Craft",value = ("<:closed_dot:696077251854336062>"*dic["CRAFT"]+"<:open_dot:696077251829170236>"*(5-dic["CRAFT"])), inline = True)
            c_embed.add_field(name = "Insight",value = ("<:closed_dot:696077251854336062>"*dic["INSIGHT"]+"<:open_dot:696077251829170236>"*(5-dic["INSIGHT"])), inline = True)
            c_embed.add_field(name = "Finance",value = ("<:closed_dot:696077251854336062>"*dic["FINANCE"]+"<:open_dot:696077251829170236>"*(5-dic["FINANCE"])), inline = True)
            c_embed.add_field(name = "\u200b", value = "\u200b", inline = False)
            c_embed.add_field(name = "Drive",value = ("<:closed_dot:696077251854336062>"*dic["DRIVE"]+"<:open_dot:696077251829170236>"*(5-dic["DRIVE"])), inline = True)
            c_embed.add_field(name = "Intimidation",value = ("<:closed_dot:696077251854336062>"*dic["INTIMIDATION"]+"<:open_dot:696077251829170236>"*(5-dic["INTIMIDATION"])), inline = True)
            c_embed.add_field(name = "Investigation",value = ("<:closed_dot:696077251854336062>"*dic["INVESTIGATION"]+"<:open_dot:696077251829170236>"*(5-dic["INVESTIGATION"])), inline = True)
            c_embed.add_field(name = "\u200b", value = "\u200b", inline = False)
            c_embed.add_field(name = "Firearms",value = ("<:closed_dot:696077251854336062>"*dic["FIREARMS"]+"<:open_dot:696077251829170236>"*(5-dic["FIREARMS"])), inline = True)
            c_embed.add_field(name = "Leadership",value = ("<:closed_dot:696077251854336062>"*dic["LEADERSHIP"]+"<:open_dot:696077251829170236>"*(5-dic["LEADERSHIP"])), inline = True)
            c_embed.add_field(name = "Medicine",value = ("<:closed_dot:696077251854336062>"*dic["MEDICINE"]+"<:open_dot:696077251829170236>"*(5-dic["MEDICINE"])), inline = True)
            c_embed.add_field(name = "\u200b", value = "\u200b", inline = False)

            c2_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Continued... <:Crypt_Keeper:694324654227062825>",
                            description = msg,
                            colour = self.colour)
            c2_embed.add_field(name = "Melee",value = ("<:closed_dot:696077251854336062>"*dic["MELEE"]+"<:open_dot:696077251829170236>"*(5-dic["MELEE"])), inline = True)
            c2_embed.add_field(name = "Performance",value = ("<:closed_dot:696077251854336062>"*dic["PERFORMANCE"]+"<:open_dot:696077251829170236>"*(5-dic["PERFORMANCE"])), inline = True)
            c2_embed.add_field(name = "Occult",value = ("<:closed_dot:696077251854336062>"*dic["OCCULT"]+"<:open_dot:696077251829170236>"*(5-dic["OCCULT"])), inline = True)
            c2_embed.add_field(name = "\u200b", value = "\u200b", inline = False)
            c2_embed.add_field(name = "Larceny",value = ("<:closed_dot:696077251854336062>"*dic["LARCENY"]+"<:open_dot:696077251829170236>"*(5-dic["LARCENY"])), inline = True)
            c2_embed.add_field(name = "Persuasion",value = ("<:closed_dot:696077251854336062>"*dic["PERSUASION"]+"<:open_dot:696077251829170236>"*(5-dic["PERSUASION"])), inline = True)
            c2_embed.add_field(name = "Politics",value = ("<:closed_dot:696077251854336062>"*dic["POLITICS"]+"<:open_dot:696077251829170236>"*(5-dic["POLITICS"])), inline = True)
            c2_embed.add_field(name = "\u200b", value = "\u200b", inline = False)
            c2_embed.add_field(name = "Stealth",value = ("<:closed_dot:696077251854336062>"*dic["STEALTH"]+"<:open_dot:696077251829170236>"*(5-dic["STEALTH"])), inline = True)
            c2_embed.add_field(name = "Streetwise",value = ("<:closed_dot:696077251854336062>"*dic["STREETWISE"]+"<:open_dot:696077251829170236>"*(5-dic["STREETWISE"])), inline = True)
            c2_embed.add_field(name = "Science",value = ("<:closed_dot:696077251854336062>"*dic["SCIENCE"]+"<:open_dot:696077251829170236>"*(5-dic["SCIENCE"])), inline = True)
            c2_embed.add_field(name = "\u200b", value = "\u200b", inline = False)
            c2_embed.add_field(name = "Survival",value = ("<:closed_dot:696077251854336062>"*dic["SURVIVAL"]+"<:open_dot:696077251829170236>"*(5-dic["SURVIVAL"])), inline = True)
            c2_embed.add_field(name = "Subterfuge",value = ("<:closed_dot:696077251854336062>"*dic["SUBTERFUGE"]+"<:open_dot:696077251829170236>"*(5-dic["SUBTERFUGE"])), inline = True)
            c2_embed.add_field(name = "Technology",value = ("<:closed_dot:696077251854336062>"*dic["TECHNOLOGY"]+"<:open_dot:696077251829170236>"*(5-dic["TECHNOLOGY"])), inline = True)

            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            c2_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            return c_embed, c2_embed
        
        
        skill_dict = {"ATHLETICS":0,
            "BRAWL":0,
            "CRAFT":0,
            "DRIVE":0,
            "FIREARMS":0,
            "MELEE":0,
            "LARCENY":0,
            "STEALTH":0,
            "SURVIVAL":0,
            "ANIMAL_KEN":0,
            "ETIQUETTE":0,
            "INSIGHT":0,
            "INTIMIDATION":0,
            "LEADERSHIP":0,
            "PERFORMANCE":0,
            "PERSUASION":0,
            "STREETWISE":0,
            "SUBTERFUGE":0,
            "ACADEMICS":0,
            "AWARENESS":0,
            "FINANCE":0,
            "INVESTIGATION":0,
            "MEDICINE":0,
            "OCCULT":0,
            "POLITICS":0,
            "SCIENCE":0,
            "TECHNOLOGY":0
            }
        try:
            conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
            c = conn.cursor()
            
            sql_cmd = 'SELECT db_ID, name'
            for key in skill_dict:
                sql_cmd += ', {}'.format(key.lower())
            sql_cmd += ' FROM char_table WHERE player_id = {} AND active_char = 1'.format(ctx.author.id)
            c.execute(sql_cmd)
            char = c.fetchone()
            
            index = 2
            for key in skill_dict:
                skill_dict[key] = char[index]
                index += 1
            
            c_embed = discord.Embed(title = "Loading...",colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            c2_embed = discord.Embed(title = "Loading...",colour = self.colour)
            c2_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c2_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            refresh_c_msg = await ctx.send(file = c_file, embed = c_embed)
            refresh_c2_msg = await ctx.send(file = c2_file, embed = c2_embed)
            exit_loop = False
            
            while True:
                e_msg = "Please Write The **Name Of The Skill** You Wish To Edit.\n`If you are done type 0`"
                c_embed, c2_embed = skills_embed(skill_dict, e_msg, char[1])
                await refresh_c_msg.edit(embed = c_embed)
                await refresh_c2_msg.edit(embed = c2_embed)
                in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                if in_msg.content.upper() in skill_dict:
                    e_msg = "Please Type The **New Number** **__{}__** should be Be.\n`If you are done type 0`".format(in_msg.content.upper())
                    while True:
                        c_embed, c2_embed = skills_embed(skill_dict, e_msg, char[1])
                        await refresh_c_msg.edit(embed = c_embed)
                        await refresh_c2_msg.edit(embed = c2_embed)
                        in_msg_2 = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                        try:
                            if int(in_msg_2.content) == 0:
                                exit_loop = True
                                break
                            elif int(in_msg_2.content) > 0 and int(in_msg_2.content) < 6:
                                break
                        except:
                            pass
                    if exit_loop == True:
                        break
                    skill_dict[in_msg.content.upper()] = int(in_msg_2.content)
                try:
                    if int(in_msg.content) == 0:
                        break
                except:
                    pass
            sql_cmd = 'UPDATE char_table SET'
            comma = False
            for key in skill_dict:
                if comma == True:
                    sql_cmd += ','
                comma = True
                sql_cmd += ' {} = {}'.format(key.lower(),skill_dict[key])
            sql_cmd += ' WHERE db_ID = {}'.format(char[0])
            c.execute(sql_cmd)
            conn.commit()
            conn.close()
            c_embed = discord.Embed(title = "Everything Was Changed successfully",
                colour = self.colour)
        except Exception as error:
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'manage_skills',error)
            # // -- Notify The User -- //
            c_embed = discord.Embed(title = "An Error Occured",
                description = 'Error : {}\n---\n{}'.format(error,self.join_us_msg),
                colour = self.colour
                )
        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
        await ctx.send(file = c_file, embed = c_embed)
        return
       
       
       
    async def manage_whhh(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'manage_whhh')
        
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
            
        def whhh_embed(dic, msg, name, fullhp, fullwp):
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> W tripple H for {} <:Crypt_Keeper:694324654227062825>".format(name),
                            description = msg,
                            colour = self.colour)
            c_embed.add_field(name = "Health",value = ("<:damage_box:698552233557753896>"*(fullhp-dic["HEALTH"])+ "<:close_box:698552233989636198>"*dic["HEALTH"]+"<:open_box:698552233675063349>"*(10-fullhp)), inline = False)
            c_embed.add_field(name = "Willpower",value = ("<:damage_box:698552233557753896>"*(fullwp-dic["WILLPOWER"])+ "<:close_box:698552233989636198>"*dic["WILLPOWER"]+"<:open_box:698552233675063349>"*(10-fullwp)), inline = False)
            c_embed.add_field(name = "Humanity",value = ("<:close_box:698552233989636198>"*dic["HUMANITY"]+"<:open_box:698552233675063349>"*(10-dic["HUMANITY"])), inline = False)
            c_embed.add_field(name = "Hunger",value = ("<:damage_box:698552233557753896>"*dic["HUNGER"]+"<:open_box:698552233675063349>"*(5-dic["HUNGER"])), inline = False)

            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")

            return c_embed

        whhh_dict = {"HEALTH":0,
            "WILLPOWER":0,
            "HUMANITY":0,
            "HUNGER":0}
        
        try:
            conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
            c = conn.cursor()
            
            sql_cmd = 'SELECT db_ID, name'
            for key in whhh_dict:
                sql_cmd += ', {}'.format(key.lower())
            sql_cmd += ' FROM char_table WHERE player_id = {} AND active_char = 1'.format(ctx.author.id)
            c.execute(sql_cmd)
            char = c.fetchone()

            c.execute('SELECT stamina FROM char_table WHERE player_id = {} AND active_char = 1'.format(ctx.author.id))
            fullhp = int(c.fetchone()[0])+3
            c.execute('SELECT resolve, composure FROM char_table WHERE player_id = {} AND active_char = 1'.format(ctx.author.id))
            char2 = c.fetchone()
            fullwp = int(char2[0])+int(char2[1])
            
            index = 2
            for key in whhh_dict:
                whhh_dict[key] = char[index]
                index += 1
            
            c_embed = discord.Embed(title = "Loading...",colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            refresh_c_msg = await ctx.send(file = c_file, embed = c_embed)
            exit_loop = False
            while True:
                e_msg = "Please Write The **Name Of The W tripple H** You Wish To Edit.\n`If you are done type 0`"
                c_embed = whhh_embed(whhh_dict, e_msg, char[1],fullhp,fullwp)
                await refresh_c_msg.edit(embed = c_embed)
                in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                if in_msg.content.upper() in whhh_dict:
                    e_msg = "Please Type The **New Number** **__{}__** should be Be.\n`If you are done type 0`".format(in_msg.content.upper())
                    while True:
                        c_embed = whhh_embed(whhh_dict, e_msg, char[1],fullhp,fullwp)
                        await refresh_c_msg.edit(embed = c_embed)
                        in_msg_2 = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                        try:
                            if int(in_msg_2.content) == 0:
                                exit_loop = True
                                break
                            elif int(in_msg_2.content) > 0:
                                break
                        except:
                            pass
                    if exit_loop == True:
                        break
                    whhh_dict[in_msg.content.upper()] = int(in_msg_2.content)
                try:
                    if int(in_msg.content) == 0:
                        break
                except:
                    pass
            sql_cmd = 'UPDATE char_table SET'
            comma = False
            for key in whhh_dict:
                if comma == True:
                    sql_cmd += ','
                comma = True
                sql_cmd += ' {} = {}'.format(key.lower(),whhh_dict[key])
            sql_cmd += ' WHERE db_ID = {}'.format(char[0])
            c.execute(sql_cmd)
            conn.commit()
            conn.close()
            c_embed = discord.Embed(title = "Everything Was Changed successfully",
                    colour = self.colour)
        except Exception as error:
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'manage_attribute',error)
            # // -- Notify The User -- //
            c_embed = discord.Embed(title = "An Error Occured",
                description = 'Error : {}\n---\n{}'.format(error,self.join_us_msg),
                colour = self.colour
                )
        c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
        c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
        await ctx.send(file = c_file, embed = c_embed)
        return
        
        
       
    @commands.command(name = 'rouse_check',
                      aliases = ['huner_check','rouse','hunger'])
    @is_char()
    async def rouse_check(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'rouse_check')
        try:
            conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
            c = conn.cursor()
            c.execute('SELECT db_ID, name, hunger FROM char_table WHERE player_id = {} AND active_char = 1'.format(ctx.author.id))
            char = c.fetchone()
            roll = random.randint(1,10)
            if roll <= 5:
                c_msg = "<:fail:696075528012169246> **Fail!** <:fail:696075528012169246>\nRolled : **{}**\nHunger : **{} -> {}**".format(roll,char[2],char[2]+1)
                c.execute("UPDATE char_table SET hunger = {} WHERE db_ID = {}".format(char[2]+1,char[0]))
                conn.commit()
                conn.close()
            else:
                c_msg = "<:success:696075528087666779> **Success!** <:success:696075528087666779>\nRolled : **{}** \nHunger : **{}**".format(roll,char[2])
                conn.close()
            c_embed = discord.Embed(title = "<:Vampire_Mouth:694325176292081784> It's Feeding Time For {}".format(char[1]),
                description = c_msg,
                colour = self.colour
                )
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await ctx.send(file = c_file, embed = c_embed)
        except Exception as error:
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'rouse_check',error)
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
    bot.add_cog(Character_Manager(bot))
