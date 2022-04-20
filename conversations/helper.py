import time
import sqlite3 as db
from pynput.keyboard import Controller as key_controller
from pynput.keyboard import Key
from features.listening import Listen 
import datefinder
from datetime import timedelta

# Taking Notes function
def writer():
    save_file = []
    while(1):
        data = Listen.record_audio()
        save_file.append(data)
        if 'save' in data:
            break
        else:
            keyboard = key_controller()
            for x in data:
                keyboard.type(x)
                time.sleep(0.1)
        keyboard.press(Key.enter)
    final_file = "\n".join(save_file[:-1])
    return final_file


def create_db():
    con = db.connect('D:/Vibes Bee/Voice assistant/Database/spent.db')
    cur = con.cursor()

    # Create table
    cur.execute('''CREATE TABLE expenses
                (date text, category text, price real)''')
    con.commit()
    con.close()


def create_event(start_time_str,title_events,duration,description=None,location=None):
        matches = list(datefinder.find_dates(start_time_str))
        if len(matches):
           start_time = matches[0]
           end_time = start_time + timedelta(hours=duration)

        event = {
          'summary': title_events,
          'location': 'kathmandu',
          'description': description,
          'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kathmandu',
          },
          'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kathmandu',
          },
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'email', 'minutes': 24 * 60},
              {'method': 'popup', 'minutes': 10},
            ],
          },
        }

        return event
