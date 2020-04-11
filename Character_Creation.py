import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import os
import sqlite3

class Character_Creation(commands.Cog):
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

    @commands.command(name = 'create_character',
                      aliases = ['create_char','create'])
    async def create_character(self,ctx):
        # // -- Log The Commands Use -- //
        await self.log_command(ctx,'create_character')

        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == channel))

        def header_embed(dic, i):
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> General Information About Your Character <:Crypt_Keeper:694324654227062825>",
                            description = dic[i][1],
                            colour = self.colour)
            c_embed.add_field(name = "Name :", value = dic[0][0], inline = True)
            c_embed.add_field(name = "Concept :", value = dic[1][0], inline = True)
            c_embed.add_field(name = "Sire :", value = dic[2][0], inline = True)

            c_embed.add_field(name = "\u200b", value = "\u200b", inline = False)
            
            c_embed.add_field(name = "Player :", value = ctx.author.name, inline = True)
            c_embed.add_field(name = "Ambition :", value = dic[3][0], inline = True)
            c_embed.add_field(name = "Clan :", value = dic[4][0], inline = True)

            c_embed.add_field(name = "\u200b", value = "\u200b", inline = False)

            c_embed.add_field(name = "Chronicle :", value = ctx.guild.name, inline = True)
            c_embed.add_field(name = "Predator :", value = dic[5][0], inline = True)
            c_embed.add_field(name = "Generation :", value = dic[6][0], inline = True)

            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")

            return c_embed

        def attributes_embed(dic, msg):
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Attribute Information About Your Character <:Crypt_Keeper:694324654227062825>",
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

        def skills_embed(dic, msg):
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Skill Information About Your Character <:Crypt_Keeper:694324654227062825>",
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

        def age_embed(dic,i):
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> General Information About Your Character <:Crypt_Keeper:694324654227062825>",
                            description = dic[i][1],
                            colour = self.colour)
            c_embed.add_field(name = "True Age :", value = dic[0][0], inline = True)
            c_embed.add_field(name = "Apparent Age :", value = dic[1][0], inline = True)
            c_embed.add_field(name = "\u200b", value = "\u200b", inline = False)
            c_embed.add_field(name = "Data of Birth :", value = dic[2][0], inline = True)
            c_embed.add_field(name = "Date of Death :", value = dic[3][0], inline = True)
            c_embed.add_field(name = "\u200b", value = "\u200b", inline = False)
            c_embed.add_field(name = "Picture Link :", value = dic[4][0], inline = True)
            
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")

            return c_embed
                                                    
        try:
            sql_command = "INSERT INTO char_table VALUES( NULL, {}, 0, 0, 0, 0, 0 ".format(ctx.author.id)
            for channel in ctx.guild.channels:
                if str(ctx.author.id) == channel.name:
                    msg = await channel.send(ctx.author.mention)
                    await msg.delete()
                    return
            conn = sqlite3.connect(os.getcwd() + '/servers/' + str(ctx.guild.id) + '/Server_Database.db')
            c = conn.cursor()
            c.execute('SELECT room_ID FROM ichannel_table WHERE title = "CHAR-CREATE-CATEGORY"')
            room_id = c.fetchone()
            channel = await ctx.guild.create_text_channel(name = "{}".format(ctx.author.id),category = ctx.guild.get_channel(int(room_id[0])))
            msg = await channel.send(ctx.author.mention)
            await msg.delete()
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Welcome To The Crypt {} <:Crypt_Keeper:694324654227062825>".format(ctx.author.name),
                description = """__Welcome to the character creator:__
     This is a online sheet that will be used for **{}!** I will ask that you try to post **__at least 1 message here per 5 minuets__** to confirm that you are still here and not have been staked through the heart. If 5 minuets have gone by without anything said by you the user, all previous information will be lost and you will have to start from scratch. **__It is recommend that you first make sure that your character is 100% correct with the staff of {}__** before continuing on. This will help this process go as fast as possible, but in the event that you haven't this channel will remain open for a staff member to check off on your hard work! 

     If you do happen to time out, please ask a staff member to delete this channel and then type `$create_character` again to be able to start over. If you ever lose place of this channel typing `$create_character` again will ping you to this channel.

     **__When you are ready to continue, please type anything in this channel and we will begin with creating your VTM V5 character!__**""".format(ctx.guild.name,ctx.guild.name),
                colour = self.colour
                )
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c2_file = discord.File("resources/VTM_LOGO.jpg", filename="VTM_LOGO.jpg")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            c_embed.set_image(url = "attachment://VTM_LOGO.jpg") 
            await channel.send(files = [c_file,c2_file], embed = c_embed)
            in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)

            info_dic = {0: ["None","Please Enter Your Characters **__Name__**.\n Link for more details : [Fantasy_Name_Generator_Vampires](https://www.fantasynamegenerators.com/vampire-names.php)"],
                        1: ["None","Please Enter the **__Concept__** Of Your Character.\n Link for more details : [RPG_Forms_Concepts](https://forum.rpg.net/index.php?threads/give-me-your-vampire-character-concepts.304718/)"],
                        2: ["None","Please Enter Your Characters **__Sire__**.\n Link for more details : [Fantasy_Name_Generator_Vampires](https://www.fantasynamegenerators.com/vampire-names.php)"],
                        3: ["None","Please Enter the **__Ambition__** Of Your Character.\n Link for more details : [RPG_Forms_Ambitions](https://forum.rpg.net/index.php?threads/give-me-your-vampire-character-concepts.304718/)"],
                        4: ["None","Please Enter Your Characters **__Clan__**.\n Link for more details : [Whitewolf_Clans](https://whitewolf.fandom.com/wiki/Clan_(VTM))"],
                        5: ["None","Please Enter Your Characters **__Predator Type__**.\n Link for more details : [Whitewolf_Predator_Types](https://whitewolf.fandom.com/wiki/Predator_Type_(VTM))"],
                        6: ["None","Please Enter Your Characters **__Generation__**.\n Link for more details : [Whitewold_Generations](https://whitewolf.fandom.com/wiki/Generation)"],
                        7: [" "," "]}
            index = 0
            c_embed = discord.Embed(title = "Loading...",colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            refresh_c_msg = await channel.send(file = c_file, embed = c_embed)
            while index < 7:
                c_embed = header_embed(info_dic,index)
                await refresh_c_msg.edit(embed = c_embed)
                in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
                sql_command += ', "{}"'.format(in_msg.content.replace('"','').replace("'",''))
                info_dic[index][0] = in_msg.content
                index += 1
                if index == 5:
                    sql_command += ', "{}"'.format(ctx.guild.name)
            c_embed = header_embed(info_dic,index)
            await refresh_c_msg.edit(embed = c_embed)
            # // -- Attributes -- //
            info_dict = {"STRENGTH":1,
                         "DEXTERITY":1,
                         "STAMINA":1,
                         "CHARISMA":1,
                         "MANIPULATION":1,
                         "COMPOSURE":1,
                         "INTELLIGENCE":1,
                         "WITS":1,
                         "RESOLVE":1,
                         4:1,
                         3:3,
                         2:4}
            c_embed = discord.Embed(title = "Loading...",colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            refresh_c_msg = await channel.send(file = c_file, embed = c_embed)
            e_msg = "Please **__Write Out The Attribute__** You Want To Give **4 Points** To"
            points = 4
            while info_dict[2] > 0:
                c_embed = attributes_embed(info_dict, e_msg)
                await refresh_c_msg.edit(embed = c_embed)
                in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
                if in_msg.content.upper() in info_dict:
                    info_dict[in_msg.content.upper()] = points
                    info_dict[points] = info_dict[points]-1
                    if info_dict[points] == 0:
                        points = points-1
                        e_msg = "Please **__Write Out The Attribute__** You Want To Give **{} Points** To".format(points)
            e_msg = ''
            c_embed = attributes_embed(info_dict, e_msg)
            await refresh_c_msg.edit(embed = c_embed)
            sql_command += ", {}, {}, {}, {}, {}, {}, {}, {}, {}".format(
                info_dict["STRENGTH"],info_dict["DEXTERITY"],info_dict["STAMINA"],
                info_dict["CHARISMA"],info_dict["MANIPULATION"],info_dict["COMPOSURE"],
                info_dict["INTELLIGENCE"],info_dict["WITS"],info_dict["RESOLVE"])
            # // -- POINTS FOR THE SKILLS -- //
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Skill Spread <:Crypt_Keeper:694324654227062825>",
                            description = """Please **__Write Out The Skill-Spread__** You Want:
`JACK OF ALL TRADES` : **__1__** Skill at **3**, **__8__** Skills at **2**, **__10__** Skills at **1**
`BALANCED` : **__3__** Skills at **3**, **__5__** Skills at **2**, **__7__** Skills at **1 **
`SPECIALIST` : **__1__** Skill at **4**,  **__3__** Skills at **3**, **__3__** Skills at **2**, **__3__** Skills at **1**""",
                            colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await channel.send(file = c_file, embed = c_embed)
            while True:
                in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
                if in_msg.content.upper() == "JACK OF ALL TRADES":
                    point_dict = {3:1,2:8,1:10}
                    points = 3
                    break
                elif in_msg.content.upper() == "BALANCED":
                    point_dict = {3:3,2:5,1:7}
                    points = 3
                    break
                elif in_msg.content.upper() == "SPECIALIST":
                    point_dict = {4:1,3:3,2:3,1:3}
                    points = 4
                    break
            # // -- SKILLS -- //
            e_msg = "Please **__Write Out The Skill__** You Want To Give **{} Points** To".format(points)
            info_dict2 = {"ATHLETICS":0,
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
            c_embed = discord.Embed(title = "Loading...",colour = self.colour)
            c2_embed = discord.Embed(title = "Loading...",colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            c2_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c2_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            refresh_c_msg = await channel.send(file = c_file, embed = c_embed)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            refresh_c2_msg = await channel.send(file = c_file, embed = c2_embed)                
            while point_dict[1] > 0:
                c_embed, c2_embed = skills_embed(info_dict2, e_msg)
                await refresh_c_msg.edit(embed = c_embed)
                await refresh_c2_msg.edit(embed = c2_embed)
                in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
                if in_msg.content.upper() in info_dict2:
                    info_dict2[in_msg.content.upper()] = points
                    point_dict[points] = point_dict[points]-1
                    if point_dict[points] == 0:
                        points = points-1
                        e_msg = "Please **__Write Out The Skill__** You Want To Give **{} Points** To".format(points)
            e_msg = ''
            c_embed, c2_embed = skills_embed(info_dict2, e_msg)
            await refresh_c_msg.edit(embed = c_embed)
            await refresh_c2_msg.edit(embed = c2_embed)
            for key in info_dict2:
                sql_command += ", {}".format(info_dict2[key])
            # // -- Specialities -- //
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Skill Spread <:Crypt_Keeper:694324654227062825>",
                            description = """Please **__Write Out Your Specialities__** :
Specialities are not stored in the database due to there random and creative nature. Please try to format your specialities in a readable formate, a good idea would be to write them as :

**Skill** : speciality
**Skill2** : speciality2
and so on and so on...

This is going to be a future reference for **you** to look back and read, so try your best! Link for more details : [Reddit_VTM_V5_Specialities](https://www.reddit.com/r/WhiteWolfRPG/comments/b9dris/vampire_fifth_edition_skill_specialties/)""",
                            colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await channel.send(file = c_file, embed = c_embed)
            in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
            sql_command += ', "{}"'.format(in_msg.content.replace('"','').replace("'",''))
            # // -- Health, Will, humanity, hunger -- //
            sql_command += ', {}, {}, 7, 1'.format(info_dict["STAMINA"]+3,info_dict["COMPOSURE"]+info_dict["RESOLVE"])
            # // -- Discilpline -- //
            c_embed = discord.Embed(title = "Loading...",colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            refresh_c_msg = await channel.send(file = c_file, embed = c_embed)
            input_list_of_lists = [[0,"None","None","None","None","None","None"],
                                   [0,"None","None","None","None","None","None"],
                                   [0,"None","None","None","None","None","None"],
                                   [0,"None","None","None","None","None","None"],
                                   [0,"None","None","None","None","None","None"],
                                   [0,"None","None","None","None","None","None"]]
            points = 0
            e_msg = ""
            for i in range(6):
                e2_msg = """How many points do you have in your **discipline 1**? Please type **only the number, not the word.**

If **__0, then the discipline step will be over__**"""
                c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Discipline(s) <:Crypt_Keeper:694324654227062825>",
                                        description = (e_msg+'---\n'+e2_msg), colour = self.colour)
                c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
                await refresh_c_msg.edit(embed = c_embed)
                in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
                points = int(in_msg.content)
                if points == 0:
                    break
                input_list_of_lists[i][0] = points
                c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Discipline(s) <:Crypt_Keeper:694324654227062825>",
                                        description = "What Is The Name Of This Discipline?", colour = self.colour)
                c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
                await refresh_c_msg.edit(embed = c_embed)
                in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
                input_list_of_lists[i][1] = in_msg.content
                e_msg += ("**" + in_msg.content + "** : " + "<:closed_dot:696077251854336062>"*points+"<:open_dot:696077251829170236>"*(5-points)+'\n')
                for x in range(points):
                    e2_msg = "What Is The Name Of {}'s {} Power".format(input_list_of_lists[i][1],x)
                    c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Discipline(s) <:Crypt_Keeper:694324654227062825>",
                                        description = (e_msg+'---\n'+e2_msg), colour = self.colour)
                    c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
                    await refresh_c_msg.edit(embed = c_embed)
                    in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
                    input_list_of_lists[i][2+x] = in_msg.content
                    e_msg += "**{}** : {}\n".format(x+1,in_msg.content)
            for d_list in input_list_of_lists:
                sql_command += ', {}, "{}", "{}", "{}", "{}", "{}", "{}"'.format(d_list[0],d_list[1],d_list[2],d_list[3],d_list[4],d_list[5],d_list[6])
            # // -- Resonance -- //
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Resonance <:Crypt_Keeper:694324654227062825>",
                            description = """Please **__Write Out Your Resonance__** :
`Animal`
`Choleric`
`Melancholy`
`Phlegmatic`
`Sanguine`
Link for more details : [Whitewolf_Resonance](https://whitewolf.fandom.com/wiki/Blood_Resonance)""",
                            colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await channel.send(file = c_file, embed = c_embed)
            in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
            sql_command += ', "{}"'.format(in_msg.content.replace('"','').replace("'",''))
            # // -- Tenets -- //
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Tenets <:Crypt_Keeper:694324654227062825>",
                            description = """Please **__Write Out {}'s Tenets__**.
This should be somewhere on the server, and if you have not read them yet you should!""".format(ctx.guild.name),
                            colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await channel.send(file = c_file, embed = c_embed)
            in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
            sql_command += ', "{}"'.format(in_msg.content.replace('"','').replace("'",''))
            # // -- TouchStone -- //
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Touchstones & Convictions <:Crypt_Keeper:694324654227062825>",
                            description = """Please **__Write Out Your Touchstone & Convictions__** :
Touchstones & Convictions are not stored in the database due to there random and creative nature. Please try to format your Touchstone & Convictions in a readable formate, a good idea would be to write them as :

**Touchstone1** : Conviction1
**Touchstone2** : Conviction2
and so on and so on...

This is going to be a future reference for **you** to look back and read, so try your best! Link for more details : [Whitewolf_Touchstone](https://whitewolf.fandom.com/wiki/Touchstone_(VTR)) [Whitewolf_Conviction](https://whitewolf.fandom.com/wiki/Conviction_(VTM))""",
                            colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await channel.send(file = c_file, embed = c_embed)
            in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
            sql_command += ', "{}"'.format(in_msg.content.replace('"','').replace("'",''))
            # // -- Bane -- //
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Clan Bane <:Crypt_Keeper:694324654227062825>",
                            description = """Please **__Write Out Your Clan's Bane__** :
If you don't know your clans bane, click the link here and copy paste : [Second_City_Banes](https://secondcity.miraheze.org/wiki/Clan_Banes)""",
                            colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await channel.send(file = c_file, embed = c_embed)
            in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
            sql_command += ', "{}"'.format(in_msg.content.replace('"','').replace("'",''))
            # // -- Merits -- //
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Merits <:Crypt_Keeper:694324654227062825>",
                            description = """Please **__Write Out Your Merits__** :
Merits are not stored in the database due to there random and creative nature. Please try to format your Merits in a readable formate, a good idea would be to write them as :

**Merits1** : cost1 : extra_info
**Merits2** : cost2 : extra_info
and so on and so on...

This is going to be a future reference for **you** to look back and read, so try your best! Still finding a good help link""",
                            colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await channel.send(file = c_file, embed = c_embed)
            in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
            sql_command += ', "{}"'.format(in_msg.content.replace('"','').replace("'",''))
            # // -- Flaws -- //
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Flaws <:Crypt_Keeper:694324654227062825>",
                            description = """Please **__Write Out Your Flaws__** :
Flaws are not stored in the database due to there random and creative nature. Please try to format your Flaws in a readable formate, a good idea would be to write them as :

**Flaws1** : cost1 : extra_info
**Flaws2** : cost2 : extra_info
and so on and so on...

This is going to be a future reference for **you** to look back and read, so try your best! Still finding a good help link""",
                            colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await channel.send(file = c_file, embed = c_embed)
            in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
            sql_command += ', "{}"'.format(in_msg.content)
            # // -- Blood Potency -- //
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Blood Potency <:Crypt_Keeper:694324654227062825>",
                            description = """Please **__Type The Number, DO NOT WRITE OUT THE WORD__**""",
                            colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await channel.send(file = c_file, embed = c_embed)
            in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
            sql_command += ', {}'.format(in_msg.content.replace('"','').replace("'",''))
            # // -- EXP -- //
            sql_command += ', 0, 0'
            # //-- AGE --//
            info_dic = {0: ["None","Please Enter Your Characters **__True Age__**."],
                        1: ["None","Please Enter the **__Apparent Age__** Of Your Character."],
                        2: ["None","Please Enter Your Characters **__Date of Birth__**."],
                        3: ["None","Please Enter the **__Date of Death__** Of Your Character."],
                        4: ["None","Please Enter Your Characters **__picture link__**."],
                        5: [" "," "]}
            index = 0
            c_embed = discord.Embed(title = "Loading...",colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            refresh_c_msg = await channel.send(file = c_file, embed = c_embed)
            while index < 5:
                c_embed = age_embed(info_dic,index)
                await refresh_c_msg.edit(embed = c_embed)
                in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
                sql_command += ', "{}"'.format(in_msg.content.replace('"','').replace("'",''))
                info_dic[index][0] = in_msg.content
                index += 1
            c_embed = age_embed(info_dic,index)
            await refresh_c_msg.edit(embed = c_embed)
            # // -- Back Story -- //
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Back Story <:Crypt_Keeper:694324654227062825>",
                            description = """This can be edited later, character limit is 1800 characters""",
                            colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await channel.send(file = c_file, embed = c_embed)
            in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
            sql_command += ', "{}"'.format(in_msg.content.replace('"','').replace("'",''))
            # // -- Notes -- //
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Notes <:Crypt_Keeper:694324654227062825>",
                            description = """This can be edited later, character limit is 1800 characters""",
                            colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await channel.send(file = c_file, embed = c_embed)
            in_msg = await self.bot.wait_for('message', timeout=300.0, check = check_message)
            sql_command += ', "{}"'.format(in_msg.content.replace('"','').replace("'",''))
            # // -- its over... its done... -- //
            sql_command += ");"
            c.execute(sql_command)
            conn.commit()
            conn.close()
            c_embed = discord.Embed(title = "<:Crypt_Keeper:694324654227062825> Welcome To The Crypt <:Crypt_Keeper:694324654227062825>",
                            description = "Do `$character_select` to make this character active\n{}".format(self.join_us_msg),
                            colour = self.colour)
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif")
            await ctx.send(file = c_file, embed = c_embed)
            
            
        except Exception as error:
            # // -- Log The Commands Use -- //
            await self.error_log_command(ctx,'create_character',error)
            c_embed = discord.Embed(title = "An Error Occured",
                description = 'Error : {}\n---\n{}'.format(error,self.join_us_msg),
                colour = self.colour
                )
            c_file = discord.File("resources/Crypt_Keeper.gif", filename="Crypt_Keeper.gif")
            c_embed.set_thumbnail(url = "attachment://Crypt_Keeper.gif") 
            await ctx.send(file = c_file, embed = c_embed)
        return
            
    

def setup(bot):
    bot.add_cog(Character_Creation(bot))
