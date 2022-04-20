import pickle
import os
import random
import wikipedia
import subprocess
import datefinder
import sqlite3 as db 
from datetime import *
from bs4 import BeautifulSoup
import conversations.constants as c
from requests_html import HTMLSession
from features.listening import Listen 
from conversations.helper import create_event, writer
from conversations.helper import create_db
from features.speaker import Speaks as sp
from googleapiclient.discovery import build

now = datetime.now()



class Conversation:

    def greetings():
        hour = int(now.hour)
        if hour>=0 and hour<12:
            sp("Good Morning!").speak()

        elif hour>=12 and hour<18:
            sp("Good Afternoon!").speak()
        else:
            sp("Good evening!").speak()

        sp(random.choice(c.greeting)).speak()
    


    def day():
        days = now.strftime("%A, %B %d")
        sp(f"Today is {days}").speak()
    

    def time_today():
        times_today = now.strftime("%I:%M %p")
        sp(f"It's {times_today}").speak()


    def joke():
        sp(random.choice(c.joke)).speak()



    def holiday():
        session = HTMLSession()
        search = 'what is the next holiday'
        url = f'https://www.google.com/search?q={search}'
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        holiday_name = soup.find('div', class_="d9FyLd").text
        holiday_detail = soup.find('span', class_="hgKElc").text
        sp(f"{holiday_name} {holiday_detail}").speak()



    def roll_dice():
        number=['1','2','3','4','5','6']
        sp(f'Ohh you got {random.choice(number)}').speak()


    def search():
        try:
                session = HTMLSession()
                sp(f'what would you like to search').speak()
                search = input()
                # search = Listen.record_audio()
                url = f'https://www.google.com/search?q={search}'
                response = session.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                search = soup.find('div', class_="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc").text
                sp(f'This what I have found. {search}').speak()

        except:
            result = wikipedia.summary(search, sentences = 1)
            sp(f'This what I have found. {result}').speak()



    def hello():
        sp(random.choice(c.hello_message)).speak()
        print("Hello")




    def Exit():
        sp(random.choice(c.close)).speak()
        exit()




    def name():
        sp(random.choice(c.name_message)).speak()



    def weather():
        try:
            session = HTMLSession()
            search = 'temperature in us'
            url = f'https://www.google.com/search?q={search}'
            response = session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            weather = soup.find('span', {'id': 'wob_dc'}).text
            temp = soup.find('span', {'id':'wob_tm'}).text
            sp(f"Current weather is {weather} and {temp} degree celsius").speak()
                    
        except:
            sp('Sorry issue in server').speak()



    def news():
        try:
            session = HTMLSession()
            url = f'https://kathmandupost.com/headlines'
            response = session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            news = soup.find('article', class_="article-image")
            prime_news =  news.h3.text
            sp(f"{prime_news}").speak()
        
        except:
            sp('Sorry issue in server').speak()

    
    def age():
        try:
            today = date.today()
            birth= date(2022,2,22)
            age = today- birth
            sp(f"I'm {age.days} days old").speak()

        except:
            sp('Sorry I cannot tell that').speak()



    def createNote():
        try:
            sp("What do you want to write onto your note").speak()
                        # Open the notepad
            path ="C:\\Windows\\System32\\notepad.exe"
            os.startfile(path)
            print("now typing...")

            #write in notepad            
            data = writer()

            # terminate the notepad
            subprocess.call("taskkill /F /IM  notepad.exe")


            # save the notepad
            name = datetime.now().strftime("%H:%M")
            filename = str(name).replace(":","-") + "-note.txt"

            with open(filename,"w") as file:
                file.write(data)
            path_1 = ".\\" + str(filename)
            path_2 = ".\\Data_Notepad\\" + str(filename)
            os.rename(path_1,path_2)
        
        except:
            sp("sorry issue in creating the note please try again").speak()


        
    
    def events():
            credentials = pickle.load(open("D:\\Vibes Bee\\Voice assistant\\package\\tokens_events.pkl","rb"))
            service = build('calendar', 'v3', credentials=credentials)
            result = service.calendarList().list().execute()
            # calendar_id=result['items'][-1]['id']
            result= service.events().list(calendarId ='primary').execute()
            event=result['items']
            length = len(event)
            sp("Can you tell me time").speak()
            search = input("yukesh")
            now = datefinder.find_dates(search)
            now=list(now)
            now = now[0].date()
            sum=0
            list_events = []
            for i in range(length):
                data=event[i]['start']['dateTime']
                data =datetime.strptime(data, "%Y-%m-%dT%H:%M:%S%z")
                data= data.date()
                if now == data:
                    sum = sum + 1
                    list_events.append(event[i]['summary'])
            sp(f'There are {sum} total events in {search}').speak()
            data = [sp(f'{i}').speak() for i in list_events]
            sp('are some of events for {search}').speak()
        


    def create_events():
        try:
            credentials = pickle.load(open("D:\\Vibes Bee\\Voice assistant\\package\\tokens_events.pkl","rb"))
            service = build('calendar', 'v3', credentials=credentials)
            sp('Can you tell me title for event').speak()        
            title = input("Events title")
            sp('At what time you would like to start event').speak()
            start_time = input("yukesh:")
            sp('Can you tell me the duration for event').speak()
            event_durations = int(input('events time duration'))
            event= create_event(start_time,title,event_durations)
            service.events().insert(calendarId = 'primary',body=event).execute()
            sp('Successfully created the events').speak()
        
        except: 
            sp('Sorry I can not create the event. Please try again later').speak()




    def tasks():

            credentials = pickle.load(open("D:\\Vibes Bee\\Voice assistant\\package\\tokens_tasks.pkl","rb"))
            service = build('tasks', 'v1', credentials=credentials)
            tasks_id = 'MDgyNTExNDMwNTUzODQ1NjE2NDQ6MDow'
            res = service.tasks().list(
                tasklist=tasks_id,
                showCompleted=False
            ).execute()
            tasks = res.get('items')
            length = len(tasks)
            sp("Can you tell me time").speak()
            search = input("yukesh:")
            now = datefinder.find_dates(search)
            now=list(now)
            sum=0
            list_task = []
            for i in range(length):
                dates = tasks[i]['due']
                dates = datetime.strptime(dates, "%Y-%m-%dT%H:%M:%S.%fZ")
                if now[0] == dates:
                    sum = sum + 1
                    list_task.append(tasks[i]['title'])
            sp(f'There are {sum} total tasks in {search}').speak()
            data = [sp(f'{i}').speak() for i in list_task]
            sp(f'are some of task for {search}').speak()


    def create_tasks():
        try:
            credentials = pickle.load(open("D:\\Vibes Bee\\Voice assistant\\package\\tokens_tasks.pkl","rb"))
            service = build('tasks', 'v1', credentials=credentials)
            tasks_id = 'MDgyNTExNDMwNTUzODQ1NjE2NDQ6MDow'
            sp('can you tell me date for tasks to create').speak()
            tasks_time = input('yukesh:')
            tasks_time = list(datefinder.find_dates(tasks_time))
            tasks_time = tasks_time[0]
            sp('can you tell me title for task').speak()
            title = input("yukesh:")
            service.tasks().insert(
                  tasklist=tasks_id,
                  body= {
                    'due':  tasks_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    'title' : title
                    }
                    ).execute()
            sp('Successfully task is created').speak()

        except:
            sp('Sorry I can not create the task. Please try again later').speak()




    def add_expenses():
        sp('What would you like to add').speak()
        category=input(f'category: ')
        price = int(input(f'price: '))
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        try:
            con = db.connect('D:/Vibes Bee/Voice assistant/Database/spent.db')
            cur = con.cursor()
            sp('Adding the Items').speak()
            cur.execute("INSERT INTO expenses VALUES ('{}','{}',{})".format(date,category,price))
            sp('Items has been added').speak()
            con.commit()
            con.close()
        except:
            sp('Database not found to add data').speak()
            sp('creating the database').speak()
            create_db()
            sp('Database has been created').speak()
            con = db.connect('D:/Vibes Bee/Voice assistant/Database/spent.db')
            cur = con.cursor()
            cur.execute("INSERT INTO expenses VALUES ('{}','{}',{})".format(date,category,price))
            con.commit()
            con.close()


    def view_total():
        try:
            con = db.connect('D:/Vibes Bee/Voice assistant/Database/spent.db')
            cur = con.cursor()
            now = datetime.now()
            date = now.strftime('%Y-%m-%d')
            sum = 0
            for date,category,price in cur.execute("SELECT * FROM expenses where date = '{}'".format(date)):
                sum = sum + price
            sp(f"Total expenses for toady is Rs {sum}").speak()

        except:
            sp("Sorry there is issue in server").speak()


    def detail_expenses():
        try:
            con = db.connect('D:/Vibes Bee/Voice assistant/Database/spent.db')
            cur = con.cursor()
            now = datetime.now()
            date = now.strftime('%Y-%m-%d')
            for date,category,price in cur.execute("SELECT * FROM expenses where date = '{}'".format(date)):
                sp(f'category : {category}').speak()
                sp(f'price: {price}').speak() 

        except:
            sp("Sorry there is issue in server").speak()

