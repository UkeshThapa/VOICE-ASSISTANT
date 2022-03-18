import pickle
import os
import time
import sqlite3 as db 
import random
from datetime import *
from bs4 import BeautifulSoup
import subprocess
from features.speaker import Speaks as sp
from features.listening import Listen 
from conversations.helper import writer
from conversations.helper import create_db
import conversations.constants as c
from requests_html import HTMLSession
from googleapiclient.discovery import build
import datefinder

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
    
    def hello():
        sp(random.choice(c.hello_message)).speak()
        print("Hello")


    def Exit():
        sp(random.choice(c.close)).speak()
        exit()


    def name():
        sp(random.choice(c.name_message)).speak()

    def weather():
        session = HTMLSession()
        search = 'temperature in us'
        url = f'https://www.google.com/search?q={search}'
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        weather = soup.find('span', {'id': 'wob_dc'}).text
        temp = soup.find('span', {'id':'wob_tm'}).text
        sp(f"Current weather is {weather} and {temp} degree celsius").speak()

    def news():
        session = HTMLSession()
        url = f'https://kathmandupost.com/headlines'
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        news = soup.find('article', class_="article-image")
        prime_news =  news.h3.text
        sp(f"{prime_news}").speak()

    
    def age():
        today = date.today()
        birth= date(2022,2,22)
        age = today- birth
        sp(f"I'm {age.days} days old").speak()


    def createNote():
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
            
        
    
    def events():
        credentials = pickle.load(open(".\\package\\tokens_events.pkl","rb"))
        service = build('calendar', 'v3', credentials=credentials)
        result = service.calendarList().list().execute()
        calendar_id=result['items'][-1]['id']
        result= service.events().list(calendarId =calendar_id).execute()
        event=result['items']
        length = len(event)
        sp("Can you tell me time").speak()
        search = Listen.record_audio()
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

    
    def tasks():
        credentials = pickle.load(open(".\\package\\tokens_tasks.pkl","rb"))
        service = build('tasks', 'v1', credentials=credentials)
        tasks_id = 'MDgyNTExNDMwNTUzODQ1NjE2NDQ6MDow'
        res = service.tasks().list(
            tasklist=tasks_id,
            showCompleted=False
        ).execute()
        tasks = res.get('items')
        length = len(tasks)
        sp("Can you tell me time").speak()
        search = Listen.record_audio()
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
        con = db.connect('D:/Vibes Bee/Voice assistant/Database/spent.db')
        cur = con.cursor()
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        sum = 0
        for date,category,price in cur.execute("SELECT * FROM expenses where date = '{}'".format(date)):
            sum = sum + price
        sp(f"Total expenses for toady is Rs {sum}").speak()



    def detail_expenses():
        con = db.connect('D:/Vibes Bee/Voice assistant/Database/spent.db')
        cur = con.cursor()
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        for date,category,price in cur.execute("SELECT * FROM expenses where date = '{}'".format(date)):
            sp(f'category : {category}').speak()
            sp(f'price: {price}').speak() 


