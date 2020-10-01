import discord
from discord.ext import commands
from discord import Role, Member, Guild
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
spreadsheet_client = gspread.authorize(creds)
sheet = spreadsheet_client.open("NAME_OF_GOOGLE_SHEET").sheet1

#data = sheet.get_all_records() !!! to get every value in spread, aka get all member names

#Represents the Client, anything to do with client use 'bot'
bot = commands.Bot(command_prefix='!',description='very very cool')

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    await bot.process_commands(message) 


#Adds the role within Guild that is "@'d"
@bot.command()
async def enroll(message, role: Role):
    member = message.author
    await member.add_roles(role)


@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    reaction_message = await bot.get_channel(Channel_ID).fetch_message(Message_ID)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        member: discord.PermissionOverwrite(read_messages=True) #might have to remove or idk
        }
    if payload.message_id == reaction_message.id:
        verification_channel = await guild.create_text_channel('verification',overwrites=overwrites) #now send message in channel telling them to verify
        welcome_channel = bot.get_channel(verification_channel.id)
        
    if verification_channel:   
        await welcome_channel.send(embed=discord.Embed(title="Type your first name and last initial", description='Ex. Hudson C', color=0x7289da)) 
        users_first_and_last_name = await bot.wait_for('message', check=lambda message: message.author == member)
        if users_first_and_last_name:
            await welcome_channel.send("Thanks " + users_first_and_last_name.content + ", our mod's will verify you shortly")
            cell_list = sheet.append_row([users_first_and_last_name.content], table_range='A1')
            sheet.update_cells(cell_list) 

bot.run('TOKEN')
