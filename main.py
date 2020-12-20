import discord
import os 
import time
from datetime import datetime
from replit import db

client = discord.Client()


def check_DB():
  return 0

def at_user(id):
  out = "<@"+id+">"
  return out


def get_event_id():
  keys = db.keys()
  out = len(keys)
  return out


def add_event(id, event_name, event_date_obj, event_remider_obj):
  if id in db:
    print("Invalid")
  else:
    db[id] = [event_name, event_date_obj, event_remider_obj]

def delete_event(id):
  out = ""
  keys = db.keys()
  if len(keys) > id: 
    out = db[id] 
    del db[id]
  return out

  
#boot up
@client.event
async def on_ready():
  print('We have logged on as {0.user}'.format(client))
  all_keys = db.keys()
  print(all_keys)

#responses
@client.event
async def on_message(message):
  #bot message
  if message.author == client.user:
    return
  
  msg = message.content
  
  #hello
  if msg.startswith('$Hello'):
    await message.channel.send("Wazzup")
  
  #Time
  if msg.startswith('$Time?'):
    current_time = time.asctime( time.localtime(time.time()))
    await message.channel.send(current_time)

  #Set event 
  if msg.startswith('$Event'):
    
    event_arr = msg.split(",");
    
    # 0 - command
    # 1 - event name 
    # 2 - event date

    #get event parameters
    event_name = event_arr[1]
    event_date =  event_arr[2][1:]
    event_remider =  event_arr[3][1:]
    event_date_obj = datetime.strptime(event_date, '%d/%m/%Y %H:%M:%S')
    event_remider_obj = datetime.strptime(event_remider, '%d/%m/%Y %H:%M:%S')
    event_id = get_event_id()


    #add to DB
    add_event(event_id, event_name, event_date, event_remider)

    #notification
    print("Your event named: " + event_name + " that will occur on " + event_date + " has been added.")

    await message.channel.send("Your event named: " + event_name + " that will occur on " + event_date + " has been added. Event ID: " + event_id)

#Set Bday
  if msg.startswith('$Bday'):
    
    event_arr = msg.split(",");
    
    # 0 - command
    # 1 - bday user id 
    # 2 - bday date

    bday_id = event_arr[1][4:-1]
    print("bday_id: ", bday_id)
    member = await message.guild.fetch_member(int(bday_id))
    bday_name = member.name
    event_date =  event_arr[2][1:]
    event_dt_obj = datetime.strptime(event_date, '%d/%m/%Y')

    print("bday_name: ", bday_name)
    print("Member: ", member)

    await message.channel.send("Bday of " + at_user(bday_id) +" has been added.")

#Delete evet
  if msg.startswith('$Delete'):

    del_arr = msg.split(", ")
    del_id = int(del_arr[1])
    deleted_event_name = delete_event(del_id)[0]
    await message.channel.send("Event : " + deleted_event_name + " has been removed")



#Objects



#Token
client.run(os.getenv('TOKEN'))




