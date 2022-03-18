# from neuralintents import GenericAssistant
# import pickle
# import json

# def function_for_greetings():
#     print("You triggered the greetings intent!")
#     # Some action you want to take

# def function_for_stocks():
#     print("You triggered the stocks intent!")
#     # Some action you want to take

# mappings = {'greeting' : function_for_greetings, 'stocks' : function_for_stocks}


# with open('../test_model_words.pkl', 'rb') as words:
#     words = pickle.load(words)

# # load label encoder object
# with open('../test_model_classes.pkl', 'rb') as classes:
#     classes = pickle.load(classes)

# assistant = GenericAssistant('../json file/intents.json',intent_methods=mappings,model_name="test_model")
# assistant.load_model(model_name='../test_model')
# with open("..//json file//intents.json") as file:
#     data = json.load(file)
# assistant.request('Hello')
# assistant._get_response(ints="..//json file//intents.json",intents_json=data)




# import pickle
# from google_auth_oauthlib.flow import InstalledAppFlow
# scopes =['https://www.googleapis.com/auth/calendar']
# flow = InstalledAppFlow.from_client_secrets_file("..\package\client_secret.json",scopes=scopes)
# credentials = flow.run_console()
# pickle.dump(credentials,open("..\\package\\tokens_tasks.pkl","wb"))
# print(credentials)


# import pickle
# from google_auth_oauthlib.flow import InstalledAppFlow
# scopes =['https://www.googleapis.com/auth/tasks.readonly']
# flow = InstalledAppFlow.from_client_secrets_file("..\package\client_secret.json",scopes=scopes)
# credentials = flow.run_console()
# pickle.dump(credentials,open("..\\package\\tokens_tasks.pkl","wb"))
# print(credentials)





import sqlite3 as db
from datetime import datetime
# def init():
#     conn = db.connect('..//Database//spent.db')
#     cur = conn.cursor()
#     sql = '''

#         create table if not exists expenses(
#             amount real,
#             category text,
#             date text
#         )

#     '''
#     cur.execute(sql)
#     conn.commit

# init()

# def add_expense():
#     conn = db.connect('..//Database//spent.db')
#     cur = conn.cursor()
#     sql = """
#             INSERT INTO expenses VALUES(
#                 110,
#                'food',
#                '2018-02-19'

#             )
    
#     """
#     cur.execute(sql)
#     conn.commit

# add_expense()

# def view_expense(category):
#     date = str(datetime.now())
#     conn = db.connect('..//Database//spent.db')
#     cur = conn.cursor()
#     sql = '''
#         SELECT * FROM expenses where category = '{}'
        
#     '''.format(category)
#     for row in cur.execute(sql):
#         print(row)
    
# view_expense('pen')

# print(view_expense('food'))
# # init()
# # add_expense(110,'transport')

# from datetime import datetime
# from functools import total_ordering
# import sqlite3 as db

# con = db.connect('..//Database//spent.db')
# cur = con.cursor()

# # Create table
# # cur.execute('''CREATE TABLE stocks
# #                (date text, category text, price real)''')

# category='co'
# price = 12
# date = "2006-01-06"
# # Insert a row of data
# cur.execute("INSERT INTO stocks VALUES ('{}','{}',{})".format(date,category,price))

# # Save (commit) the changes
# con.commit()

# # We can also close the connection if we are done with it.
# # Just be sure any changes have been committed or they will be lost.
# con.close()
# # date = "2006-01-05"
# # sum = 0

# for date,category,price in cur.execute("SELECT * FROM stocks where date = '{}'".format(date)):
#     print(f'category: {category}')
#     print(f'price: {price}')
#     sum = sum + price
#     print(sum)


import time
def create_db():
    con = db.connect('..//Database//spent.db')
    cur = con.cursor()

    # Create table
    cur.execute('''CREATE TABLE expenses
                   (date text, category text, price real)''')
    con.commit()
    con.close()



def add_expenses():
    category=input(f'category: ')
    price = int(input(f'price: '))
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    try:
        con = db.connect('..//Database//spent.db')
        cur = con.cursor()
        print('Adding the Items')
        time.sleep(0.4)
        cur.execute("INSERT INTO expenses VALUES ('{}','{}',{})".format(date,category,price))
        print('Items has been added')
        con.commit()
        con.close()
    except:
        print('Database not found ')
        time.sleep(0.4)
        print('creating the database...')
        time.sleep(0.4)
        create_db()
        print('Database has been created')
        con = db.connect('..//Database//spent.db')
        cur = con.cursor()
        cur.execute("INSERT INTO expenses VALUES ('{}','{}',{})".format(date,category,price))
        con.commit()
        con.close()

def view_total():
    con = db.connect('..//Database//spent.db')
    cur = con.cursor()
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    sum = 0
    for date,category,price in cur.execute("SELECT * FROM expenses where date = '{}'".format(date)):
        sum = sum + price
    print(f"Total expenses for toady is Rs {sum}")

def detail_expenses():
    con = db.connect('..//Database//spent.db')
    cur = con.cursor()
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    for date,category,price in cur.execute("SELECT * FROM expenses where date = '{}'".format(date)):
        print(f'category: {category}')
        print(f'price: {price}') 

add_expenses()