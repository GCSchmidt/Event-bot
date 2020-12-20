import discord
import os
import time
from datetime import datetime
from replit import db
import sqlite3

client = discord.Client()

conn = sqlite3.connect('test.db')
print("Opened database successfully")
cursor = conn.cursor()

#Create tables
conn.execute('''CREATE TABLE IF NOT EXISTS Events
         (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
         NAME           TEXT     NOT NULL,
         Date           TEXT     NOT NULL,
         Reminder       TEXT     NOT NULL);''')
print("Event Table created successfully")

conn.execute('''CREATE TABLE IF NOT EXISTS Bday_table
         (ID INTEGER PRIMARY KEY NOT NULL,
         Date           TEXT     NOT NULL,
         Reminder       TEXT     );''')
print("Bday Table created successfully")

conn.close()


#formats user id to @ them
def at_user(id):
    out = "<@"+id+">"
    return out

#add event
def add_event(event_name, event_date, event_remider):
  
  conn = sqlite3.connect('test.db')
  cursor = conn.cursor()
  
  conn.execute("INSERT INTO Events (NAME, Date, Reminder) VALUES(?, ?, ?)", 
                                                  (event_name, event_date, event_remider)) 
  conn.commit()
  cursor.close()

#add bday
def add_bday(id, bday_date, bday_remider):
  
  conn = sqlite3.connect('test.db')
  cursor = conn.cursor()
  
  conn.execute("INSERT INTO Bday_table (id, Date, Reminder) VALUES(?, ?, ?)", 
                                                  (id, bday_date, bday_remider)) 
  conn.commit()
  cursor.close()

#show all events
def show_all():
  out = "Events: \n"
  names = []
  dates = []
  ids = []
  #SQL
  conn = sqlite3.connect('test.db')
  cursor = conn.cursor()
  cursor.execute('''Select Name from Events;''') 
  names = cursor.fetchall();

  cursor.execute('''Select Date from Events;''') 
  dates = cursor.fetchall(); 

  conn.commit()
  cursor.close()

  conn = sqlite3.connect('test.db')
  cursor = conn.cursor()

  for i in range(len(names)):
    str_name = names[i][0]
    str_date = dates[i][0]
    out = out + str_name + ": " + str_date + "\n"
  
  out = out + "\n" + "Birthdays: \n"

  cursor.execute('''Select ID from Bday_table;''') 
  ids = cursor.fetchall();

  cursor.execute('''Select Date from Bday_table;''') 
  dates = cursor.fetchall(); 
  
  conn.commit()
  cursor.close()

  for i in range(len(ids)):
    member = client.get_user(int(ids[i][0]))
    str_name = member.name
    str_date = dates[i][0]
    out = out + str_name + ": " + str_date + "\n"
  return out
  
#delete event given event Name
def delete_event(event_name):
  sql = 'DELETE FROM Events WHERE name=?'
  conn = sqlite3.connect('test.db')
  cursor = conn.cursor()
  cursor.execute(sql, (event_name,))
  conn.commit()

#deletBday given userid
def delete_bday(id):
  sql = 'DELETE FROM Bday_table WHERE id=?'
  conn = sqlite3.connect('test.db')
  cursor = conn.cursor()
  cursor.execute(sql, (id,))
  conn.commit()
  out = "Deleted Birthday"
  return out

#Delete all Replit DB
def delete_all_Replit_DB():
  all_keys = db.keys()
  for key in all_keys:
    del db[key]  
  print("All deleted")

#Delete all events
def delete_all():
  out = "All events deleted!"
  
  conn = sqlite3.connect('test.db')
  cursor = conn.cursor()
  cursor.execute('''Delete from Events;''')  

  conn.commit()
  cursor.close()

  return out

def today():
  current_date = datetime.today().date()
  out = "Things happening today \n \nEvents: \n"
  names = []
  dates = []
  ids = []
  #SQL
  conn = sqlite3.connect('test.db')
  cursor = conn.cursor()
  cursor.execute('''Select Name from Events;''') 
  names = cursor.fetchall();

  cursor.execute('''Select Date from Events;''') 
  dates = cursor.fetchall(); 

  conn.commit()
  cursor.close()

  conn = sqlite3.connect('test.db')
  cursor = conn.cursor()

  for i in range(len(names)):
    str_name = names[i][0]
    str_date = dates[i][0]
    date_time_obj = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
    i_date = date_time_obj.date()
    if i_date == current_date:
      out = out + str_name + "\n"
  
  out = out + "\n" + "Birthdays: \n"

  cursor.execute('''Select ID from Bday_table;''') 
  ids = cursor.fetchall();

  cursor.execute('''Select Date from Bday_table;''') 
  dates = cursor.fetchall(); 
  
  conn.commit()
  cursor.close()

  for i in range(len(ids)):
    member = client.get_user(int(ids[i][0]))
    str_name = member.name
    str_date = dates[i][0]
    date_time_obj = datetime.strptime(str_date, '%d/%m/%Y')
    
    i_date = date_time_obj.date()

    if (int(i_date.day) == int(current_date.day)) and (int(i_date.month) == int(current_date.month)):
      out = out + str_name + "\n"

  return out

#boot up
@client.event
async def on_ready():
    print('We have logged on as {0.user}'.format(client))

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

    #Get current date and time
    if msg.startswith('$Time?'):
        current_time = time.asctime( time.localtime(time.time()))
        await message.channel.send(current_time)

    #Add event command
    if msg.startswith('$Event'):

        event_arr = msg.split(", ");

        #get event parameters
        event_name = event_arr[1]
        event_date =  event_arr[2]
        event_remider =  event_arr[3]
        event_date_obj = datetime.strptime(event_date, '%d/%m/%Y %H:%M:%S')
        event_remider_obj = datetime.strptime(event_remider, '%d/%m/%Y %H:%M:%S')
        add_event(event_name, event_date_obj, event_remider_obj)

        await message.channel.send("Your event named: " + event_name + " that will occur on " + event_date + " has been added.")

    #Add Bday command
    if msg.startswith('$Bday'):
        event_arr = msg.split(",");
        bday_id = event_arr[1][4:-1]
        member = await message.guild.fetch_member(int(bday_id))
        bday_name = member.name
        event_date =  event_arr[2][1:]
        event_dt_obj = datetime.strptime(event_date, '%d/%m/%Y')
        add_bday(int(bday_id), event_date, "0")
        await message.channel.send("Bday of " + at_user(bday_id) +" has been added.")

    #View all events command
    if msg.startswith('$All'):
      out = show_all()
      await message.channel.send(out)
        
    #Delete event command
    if msg.startswith('$DeleteEvent'):
      del_arr = msg.split(", ")
      event_name = del_arr[1]
      delete_event(event_name)
      await message.channel.send("Event " + event_name + " has been removed")
    
    #Delete Bday command
    if msg.startswith('$DeleteBday'):
        event_arr = msg.split(",");
        bday_id = event_arr[1][4:-1]
        member = client.get_user(int(bday_id))
        bday_name = member.name
        delete_bday(int(bday_id))
        await message.channel.send("Birthday of " + bday_name +" has been removed.")


    #Delete all events command
    if msg.startswith('$DeleteAll'):
      out = delete_all()
      await message.channel.send(out)

    #Show todays events
    if msg.startswith('$Today'):
      out = today()
      await message.channel.send(out)

#Token
client.run(os.getenv('TOKEN'))
