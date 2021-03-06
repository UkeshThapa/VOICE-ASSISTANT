import time
from neuralintents import GenericAssistant
from conversations.conversation import Conversation
import pickle



def main():
    
    mapping = {
        'greeting'        : Conversation.hello,
        'goodbye'         : Conversation.Exit,
        'age'             : Conversation.age,
        'day'             : Conversation.day,
        'time'            : Conversation.time_today,
        'joke'            : Conversation.joke,
        'holiday'         : Conversation.holiday,
        'name'            : Conversation.name,
        'roll_dice'       : Conversation.roll_dice,
        'search'          : Conversation.search,
        'weather'         : Conversation.weather,
        'news'            : Conversation.news,
        'create_Note'     : Conversation.createNote,
        'create_events'   : Conversation.create_events,
        'create_tasks'    : Conversation.create_tasks,
        'tasks'           : Conversation.tasks,
        'events'          : Conversation.events,
        'add_expenses'    : Conversation.add_expenses,
        'sum_expenses'    : Conversation.view_total,
        'detail_expenses' : Conversation.detail_expenses

    }

    try:
        with open('./save_model/test_model_words.pkl', 'rb') as words:
            words = pickle.load(words)

        # load label encoder object
        with open('./save_model/test_model_classes.pkl', 'rb') as classes:
            classes = pickle.load(classes)

        assistant = GenericAssistant('./json file/intents.json',intent_methods=mapping)
        assistant.load_model(model_name='./save_model/test_model')

    except:
        assistant= GenericAssistant(".//json file//intents.json",intent_methods=mapping,model_name="./save_model/test_model")
        assistant.train_model()
        assistant.save_model()

    Conversation.greetings()
    time.sleep(1)


    while True:
        data = input(f'yukesh: ')
        assistant.request(data)
        

if __name__ == "__main__":
    main()
