
# import json
# import nltk
# import numpy
# import tflearn
# import tensorflow
# from nltk.stem.lancaster import LancasterStemmer
# from tensorflow.python.framework import ops
# from tensorflow import keras
# import talos
# from keras import Sequential
# from keras.layers import Dense, Dropout
# from  keras.optimizer_v1 import SGD
# from keras.models import load_model


# nltk.download('punkt', quiet=True)
# nltk.download('wordnet', quiet=True)

# # Activate the Lancaster function
# stemmer = LancasterStemmer()

# with open("..//json file//intents.json") as file:
#     data = json.load(file)

# print(data["intents"])

# words = []
# labels = []
# docs_x = []
# docs_y =[]

# for intent in data["intents"]:
#     for pattern in intent["patterns"]:
#         wrds = nltk.word_tokenize(pattern)
#         words.extend(wrds)
#         docs_x.append(pattern)
#         docs_y.append(intent['tag'])


#         if intent['tag'] not in labels:
#             labels.append(intent['tag'])


# words = [stemmer.stem(w.lower()) for w in words if w != ['!', '?', ',', '.']]
# words = sorted(list(set(words)))
# labels = sorted(labels)

# training = []
# output = []

# out_empty  = [0 for _ in range (len(labels))]

# for x, doc in enumerate(docs_x):
#     bag = []
#     wrds = [stemmer.stem(w.lower()) for w in doc]

#     for w in words:
#         if w in wrds:
#             bag.append(1)
#         else:
#             bag.append(0)

#     output_row = out_empty[:]
#     output_row[labels.index(docs_y[x])]=1

#     training.append(bag)
#     output.append(output_row)

# training = numpy.array(training)
# output = numpy.array(output)

# ops.reset_default_graph()


# model = Sequential()
# model.add(Dense(128, input_shape=(len(training[0]),), activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(64, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(len(output[0]), activation='softmax'))

# sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
# model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# model.fit(training, output, epochs=200, batch_size=16,verbose=1)



# net = tflearn.input_data(shape=[None,len(training[0])])
# net = tflearn.fully_connected(net,128)
# net = tflearn.fully_connected(net,activation="relu")
# net = tflearn.fully_connected(net,8)
# net = tflearn.fully_connected(net,len(output[0]),activation="softmax")
# net =tflearn.regression(net)


# model = tflearn.DNN(net)

# model.fit(training,output,n_epoch=200,batch_size=8,show_metric=True)
# model.save("model.tflearn")




# import json 
# import numpy as np 
# import tensorflow as tf
# from tensorflow import keras
# from keras.models import Sequential
# from keras.layers import Dense, Embedding, GlobalAveragePooling1D
# from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
# from sklearn.preprocessing import LabelEncoder



# with open('..//json file//intents.json') as file:
#     data = json.load(file)
    
# training_sentences = []
# training_labels = []
# labels = []
# responses = []


# for intent in data['intents']:
#     for pattern in intent['patterns']:
#         training_sentences.append(pattern)
#         training_labels.append(intent['tag'])
#     responses.append(intent['responses'])
    
#     if intent['tag'] not in labels:
#         labels.append(intent['tag'])
        
# num_classes = len(labels)



# lbl_encoder = LabelEncoder()
# lbl_encoder.fit(training_labels)
# training_labels = lbl_encoder.transform(training_labels)


# vocab_size = 1000
# embedding_dim = 16
# max_len = 20
# oov_token = "<OOV>"

# tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
# tokenizer.fit_on_texts(training_sentences)
# word_index = tokenizer.word_index
# sequences = tokenizer.texts_to_sequences(training_sentences)
# padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)


# model = Sequential()
# model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
# model.add(GlobalAveragePooling1D())
# model.add(Dense(16, activation='relu'))
# model.add(Dense(16, activation='relu'))
# model.add(Dense(num_classes, activation='softmax'))

# model.compile(loss='sparse_categorical_crossentropy', 
#               optimizer='adam', metrics=['accuracy'])

# model.summary()


# epochs = 500
# history = model.fit(padded_sequences, np.array(training_labels), epochs=epochs)


# model.save("chat_model")


# import pickle

# # to save the fitted tokenizer
# with open('tokenizer.pickle', 'wb') as handle:
#     pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
# # to save the fitted label encoder
# with open('label_encoder.pickle', 'wb') as ecn_file:
#     pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)



import json 
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder

import colorama 
colorama.init()
from colorama import Fore, Style, Back

import random
import pickle

with open("..//json file//intents.json") as file:
    data = json.load(file)


def chat():
    # load trained model
    model = keras.models.load_model('chat_model')

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    max_len = 20
    
    while True:
        print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end="")
        inp = input()
        if inp.lower() == "quit":
            break

        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                             truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])

        for i in data['intents']:
            if i['tag'] == tag:
                print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , np.random.choice(i['responses']))

        # print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,random.choice(responses))

print(Fore.YELLOW + "Start messaging with the bot (type quit to stop)!" + Style.RESET_ALL)
chat()