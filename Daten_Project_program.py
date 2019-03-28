'''
Chatbot that detects user tone and recommends corresponding activities. Uses IBM Watson's Conversation
and Tone Analyzer.

Authors: Prajakta Gaydhani (pag3862)

References : Conversation and Tone Analyser Integration Example by Watson Developer Cloud.
             URL : https://github.com/watson-developer-cloud/python-sdk/tree/master/examples/conversation_tone_analyzer_integration
'''



from watson_developer_cloud import ConversationV1
from watson_developer_cloud import ToneAnalyzerV3
import csv
import random
from tkinter import *
from PIL import Image, ImageTk

import tkinter.scrolledtext as tkst







def getNBooks(books,detected_tone):
    print(detected_tone)
    genresToAvoid = []
    genresToTake = []
    if detected_tone == "anger" or detected_tone == "disgust":
        genresToAvoid = ["Romance", "Horror", "Dystopia"]
        genresToTake = ["Comedy", "Self-help", "Fantasy"]
    elif detected_tone == "sadness":
        genresToAvoid = ["Dystopia", "Horror", "Science"]
        genresToTake = ["Comedy", "Drama", "Fantasy"]
    elif detected_tone == "fear":
        genresToAvoid = ["Horror", "War", "Thriller"]
        genresToTake = ["Comedy", "Drama", "Children"]
    else:
        genresToAvoid = ["Horror", "War", "Thriller"]
        genresToTake = ["Comedy", "Drama", "Children"]

    print(genresToAvoid, genresToTake)
    temp = random.randint(0, len(books)//2)
    size = 2
    temp_list = []
    for i in range(temp,len(books)):
        if (books[i][2].find(genresToTake[0]) != -1 or books[i][2].find(genresToTake[1]) != -1 or books[i][2].find(genresToTake[1]) != -1)\
                and (books[i][2].find(genresToAvoid[0]) == -1) and (books[i][2].find(genresToAvoid[1]) == -1) and (books[i][2].find(genresToAvoid[2]) == -1) :
            if len(temp_list) >= size:
                return temp_list
            else:
                str = books[i][0] + " by " +books[i][1]
                temp_list.append(str)


def getNMovies(movies,detected_tone):
    genresToAvoid = []
    genresToTake = []
    if detected_tone == "anger" or detected_tone == "disgust":
        genresToAvoid = ["Romance", "Horror", "War"]
        genresToTake = ["Comedy", "Adventure", "Animation"]
    elif  detected_tone == "sadness" :
        genresToAvoid = ["Romance", "Horror", "War"]
        genresToTake = ["Comedy", "Drama", "Fantasy"]
    elif  detected_tone == "fear" :
        genresToAvoid = [ "Horror", "War", "Thriller"]
        genresToTake = ["Comedy", "Drama", "Children"]
    else:
        genresToAvoid = [ "Horror", "War", "Thriller"]
        genresToTake = ["Comedy", "Drama", "Children"]



    temp = random.randint(0, len(movies) // 2)
    size = 2
    temp_list = []
    for i in range(temp, len(movies)):
        if (movies[i][1].find(genresToTake[0]) != -1 or movies[i][1].find(genresToTake[1]) != -1 or movies[i][1].find(genresToTake[2]) != -1)\
                and (movies[i][1].find(genresToAvoid[0]) == -1) and (movies[i][1].find(genresToAvoid[1]) == -1) and (movies[i][1].find(genresToAvoid[2]) == -1):
            if len(temp_list) >= size:
                return temp_list
            else:
                temp_list.append(movies[i][0])


def getPMovies(movies):
    temp = random.randint(0, len(movies) // 2)
    size = 2
    temp_list = []
    for i in range(temp, len(movies)):
        if (movies[i][1].find("Comedy") != -1 or movies[i][1].find("Adventure") != -1 or movies[i][1].find("Fantasy") != -1 or movies[i][1].find("Romance") or movies[i][1].find("Drama") != -1) \
                and (movies[i][1].find("War") == -1) and (movies[i][1].find("Horror") == -1) and (movies[i][1].find("sex") == -1) \
                and (movies[i][0].find("sex") == -1):
            if len(temp_list) >= size:
                return temp_list
            else:
                temp_list.append(movies[i][0])


def getPBooks(books):
    temp = random.randint(0, len(books)//2)
    size = 2
    temp_list = []
    for i in range(temp,len(books)):
        if (books[i][2].find("Comedy") != -1 or books[i][2].find("Romance") != -1 or books[i][2].find("Fantasy") != -1 or books[i][2].find("Thriller") != -1)\
                and (books[i][2].find("Dystopia") == -1) and (books[i][2].find("Horror") == -1) \
                and (books[i][2].find("sex") == -1) and (books[i][1].find("sex") == -1) :
            if len(temp_list) >= size:
                return temp_list
            else:
                str = books[i][0] + " by " +books[i][1]
                temp_list.append(str)



def getJoke(jokes):
    temp = random.randint(0,len(jokes)-1)
    return jokes[temp]


def getShoppingWebsite():
    shopping = ["https://www.amazon.com/gp/movers-and-shakers", "https://www.urbanoutfitters.com/", "https://www.macys.com/", "http://www.asos.com/",
                "http://www.hm.com/us/","https://www.zara.com/us/","https://www.bloomingdales.com/"]
    temp = random.randint(0,len(shopping)-1)
    return shopping[temp]


def initUser():
    return {
        'user' : {
            'tone' : {
                'emotion' : {
                    'current' : None
                }
            }
        }
    }


def updateEmotionTone(user, emotionTone):
    maxScore = 0
    primaryEmotion = None
    primaryEmotionScore = None

    for tone in emotionTone['tones']:
        if tone['score'] > maxScore:
            maxScore = tone['score']
            primaryEmotion = tone['tone_name'].lower()
            primaryEmotionScore = tone['score']

    if maxScore <= THRESHOLD:
        primaryEmotion = 'neutral'
        primaryEmotionScore = None

    user['tone']['emotion']['current'] = primaryEmotion


def updateUserTone(conversationPayload, toneAnalyserPayload):
    emotionTone = None

    if 'context' not in conversationPayload:
        conversationPayload['context'] = {}

    if 'user' not in conversationPayload:
        conversationPayload['context'] = initUser()

    user = conversationPayload['context']['user']

    if toneAnalyserPayload and toneAnalyserPayload['document_tone']:
        for toneCategory in toneAnalyserPayload['document_tone']['tone_categories']:
            if toneCategory['category_id'] == EMOTION_TONE_LABEL:
                emotionTone = toneCategory

    updateEmotionTone(user,emotionTone)

    conversationPayload['context']['user'] = user

    return conversationPayload



def startRecommendations(payload, root) :


    tone = tone_analyser.tone(text = payload['input']['text'])
    conversation_payload = updateUserTone(payload, tone)
    response = conversation.message(workspace_id=workspace_id, message_input = {'text':payload['input']['text']})
    tone_response = conversation.message(workspace_id=workspace_id, message_input=conversation_payload['input'],context=conversation_payload['context'])




    if tone_response['intents'][0]['intent'] == "Goodbye" or tone_response['intents'][0]['intent'] == "thank":
        stuff = response['output']['text'][0]
        tt = tkst.ScrolledText(root, height=4, width=65, bg = 'LightSkyBlue1')
        tt.insert(INSERT, stuff)
        root.create_window(250, y1 + 50, window=tt)
        print(response['output']['text'])
        return False
    elif tone_response['intents'][0]['intent'] == 'Negative_Consolation':
        global emotion
        emotion = conversation_payload['context']['user']['tone']['emotion']['current']
        joke = getJoke(jokes)
        print(response['output']['text'], joke)
        stuff = response['output']['text'][0] +  "\n" + joke
        tt = tkst.ScrolledText(root, height = 4, width = 65, bg = 'LightSkyBlue1')
        tt.insert(INSERT, stuff)
        root.create_window(250, y1+ 50, window=tt)
        txt = "Your reaction to the joke?"
    elif tone_response['intents'][0]['intent'] == 'Positive_Consolation':
        joke = getJoke(jokes)
        print(response['output']['text'], joke)
        stuff = response['output']['text'][0] + "\n" + joke
        tt = tkst.ScrolledText(root, height=4, width=65, bg = 'LightSkyBlue1')
        tt.insert(INSERT, stuff)
        root.create_window(250, y1 + 50, window=tt)
        txt = "Your reaction to the joke?"
    else:
        stuff = response['output']['text'][0]
        print(response['output']['text'])
        tt = tkst.ScrolledText(root, height=4, width=65, bg = 'LightSkyBlue1')
        tt.insert(INSERT,stuff)
        root.create_window(250, y1 + 50, window=tt)
        if tone_response['intents'][0]['intent'] == 'Laugh':
            txt = "Respond with Yes or No."
        elif tone_response['intents'][0]['intent'] == 'Greeting':
            txt = "Tell us about your day!"
        elif tone_response['intents'][0]['intent'] == 'moreRecco':
            txt = "Type More for more options or Thanks/Bye to end."
        else:
            txt = ""



    if (tone_response['intents'][0]['intent'] == 'Yes' or tone_response['intents'][0]['intent'] == 'moreRecco') and emotion != "p":
        book_list = getNBooks(books,emotion)
        movie_list = getNMovies(movies,emotion)
        print("Check out these books ",book_list)
        print("Some good movies ",movie_list)
        stuff = "Check out these books " + book_list[0] + " , " + book_list[1] + "\n" + "Some good movies " + movie_list[0]+ " , " + movie_list[1]
        tt = tkst.ScrolledText(root, height=4, width=65, bg = 'LightSkyBlue1')
        tt.insert(INSERT, stuff)
        root.create_window(250, y1 + 50, window=tt)
        txt = "Type More for more options or Thanks/Bye to end."



    if (tone_response['intents'][0]['intent'] == 'Yes' or tone_response['intents'][0]['intent'] == 'moreRecco') and emotion == "p":
        book_list = getPBooks(books)
        movie_list = getPMovies(movies)
        print("Check out these books ", book_list)
        print("Some good movies ", movie_list)
        print("Or we can go shopping!!!! Check out this cool website!", getShoppingWebsite())
        stuff = "Check out these books " + book_list[0] + " , " + book_list[1] + "\n" + "Some good movies " + movie_list[0]+ " , " + movie_list[1] + "\n" +\
        "OR we can go shopping!!!! Check out this cool website!" + getShoppingWebsite()
        tt = tkst.ScrolledText(root, height=5, width=65, bg = 'LightSkyBlue1')
        tt.insert(INSERT, stuff)
        root.create_window(250, y1 + 50, window=tt)
        txt = "Type More for more options or Thanks/Bye to end."

    global text1
    text1 = txt


def setInputText(text,root):
    print(text)
    payload['input']['text'] = text
    flag = startRecommendations(payload, root)
    if flag == False:
        return
    else:
        global y_value
        y_value = y_value + 110
        global y1
        y1 = y1  + 110
        EntryGUI(root)




def EntryGUI(root):
        image = Image.open("mark.jpeg")
        img = image.resize((20, 20), Image.ANTIALIAS)
        img.save('resized_image.jpg')

        Photo = ImageTk.PhotoImage(img)
        l1 = Label(root, image = Photo)
        l1.image = Photo

        root.create_window(775, y_value, window=l1)

        l2 = Label(root,text="", width = 50)
        l1.bind("<Enter>", lambda e: l2.configure(text=text1))
        l1.bind("<Leave>", lambda e: l2.configure(text=" "))

        root.create_window(700, y_value + 20, window = l2)



        e1 = Entry(root, bg = 'LightSkyBlue1')
        root.create_window(650, y_value, window=e1)
        e1.bind('<Return>',lambda e : setInputText(e1.get(),root))








jokes = []
with open('funjokes.csv') as fileptr:
    next(fileptr, None)
    readCSV = csv.reader(fileptr)
    for row in readCSV:
        jokes.append(row[1])

books = []
with open('cleanedBooksData.csv') as fileptr:
    next(fileptr, None)
    readCSV = csv.reader(fileptr)
    for row in readCSV:
        temp = []
        temp.append(row[1])
        temp.append(row[2])
        temp.append(row[3])
        books.append(temp)

movies = []
with open('movies.csv') as fileptr:
    next(fileptr, None)
    readCSV = csv.reader(fileptr)
    for row in readCSV:
        temp = []
        temp.append(row[1])
        temp.append(row[2])
        movies.append(temp)

emotion = "p"
y_value = 75
y1 = 75
text1 = "Start conversation with greeting!"


EMOTION_TONE_LABEL = 'emotion_tone'
THRESHOLD = 0.5


conversation = ConversationV1(username="6e7f1115-0c0a-4de1-958f-0b2775d67a20", password="vDvC7T7VxjHo", version="2017-04-25")
tone_analyser = ToneAnalyzerV3(username="5f400c71-48f3-47b8-840c-53d7e1611b77", password="3djj2OCvWd4n",
                               url="https://gateway.watsonplatform.net/tone-analyzer/api", version="2017-04-25")


workspace_id = "b3f9b097-f794-4dd9-8575-8fdb7180e1db"



payload = {'workspace_id' : workspace_id,
           'input' : {
               'text' : ""
           }}



root = Tk()
root.title("Mood-Based Activity Recommendation System")
frame=Frame(root,width=900,height=1000,bg='white')
frame.grid(row=0,column=0)
canvas=Canvas(frame,bg='white',width=900,height=1000,scrollregion=(0,0,900,1500))

vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)



canvas.config( yscrollcommand=vbar.set)

label = Label(text = 'Mood-Based Activity Recommendation System', justify = CENTER,font=("Comic Sans", 26),fg='OrangeRed2')
canvas.create_window(400, 20, window = label)


EntryGUI(canvas)

canvas.pack()
root.mainloop()
