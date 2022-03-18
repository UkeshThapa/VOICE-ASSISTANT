import time
import sqlite3 as db
from pynput.keyboard import Controller as key_controller
from pynput.keyboard import Key
from features.listening import Listen 

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

