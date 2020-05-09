import os
import sys
import datetime
import pyttsx3
import speech_recognition as sr
import wikipedia
import wolframalpha
import webbrowser
import smtplib
import json
import random
import subprocess
import time
from time import ctime
import requests
import cv2
from pygame import mixer

engine = pyttsx3.init('sapi5')

client = wolframalpha.Client('Get your own key')

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices) - 2].id)


def talk(audio):
    print('Jessie: ' + audio)
    engine.say(audio)
    engine.runAndWait()


def greetMe():
    CurrentHour = int(datetime.datetime.now().hour)
    if CurrentHour >= 0 and CurrentHour < 12:
        talk('Good Morning!')

    elif CurrentHour >= 12 and CurrentHour < 18:
        talk('Good Afternoon!')

    elif CurrentHour >= 18 and CurrentHour != 0:
        talk('Good Evening!')


greetMe()

talk('Hi, It\'s Jessie')
talk('What can I do for you?')


def GivenCommand():
    k = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        k.pause_threshold = 1
        audio = k.listen(source)
    try:
        Input = k.recognize_google(audio, language='en-in')
        print('Me: ' + Input + '\n')

    except sr.UnknownValueError:
        talk('Sorry! I didn\'t get that! Try typing it here!')
        Input = str(input('Command: '))

    return Input


if __name__ == '__main__':

    while True:

        Input = GivenCommand()
        Input = Input.lower()

        #Opening websites
        if 'open google' in Input:
            talk('sure')
            webbrowser.open('www.google.co.in')

        elif 'open gmail' in Input:
            talk('sure')
            webbrowser.open('www.gmail.com')
            
        elif 'open youtube' in Input:
            talk('sure')
            webbrowser.open('www.youtube.com')

        #Holding Conversations
        elif "what\'s up" in Input or 'how are you' in Input:
            setReplies = ['Just doing some stuff!', 'I am good!', 'Nice!', 'I am amazing and full of power']
            talk(random.choice(setReplies))
       
        elif "who are you" in Input or 'where are you' in Input or 'what are you' in Input:
            setReplies = [' I am Jessie, your virtual assistant', 'In your system', 
                            'I am a virtual personal assistant to help make your tasks easier']
            talk(random.choice(setReplies))
        
        elif "what is the time" in Input or "time" in Input or "date" in Input:
            talk(ctime())
        
        #Send an email
        elif 'email' in Input:
            talk('Who is the recipient? ')
            recipient = GivenCommand()

            if 'me' in recipient:
                try:
                    talk('What should I say? ')
                    content = GivenCommand()

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login("Your_Username", 'Your_Password')
                    server.sendmail('Your_Username', "Recipient_Username", content)
                    server.close()
                    talk('Email sent!')

                except:
                    talk('Sorry ! I am unable to send your message at this moment!')
        
        #Stop the program
        elif 'nothing' in Input or 'abort' in Input or 'stop' in Input:
            talk('okay')
            talk('Bye, have a good day.')
            sys.exit()

        elif 'hello' in Input:
            talk('hey')

        elif 'bye' in Input:
            talk('Bye, have a great day.')
            sys.exit()

        #Opens Webcam
        elif "click a picture" in Input or "selfie" in Input:
            talk('Press q to quit')
            cap=cv2.VideoCapture(0)
            while True:
                ret,frame=cap.read()

                if ret==False:
                    continue

                cv2.imshow("Video Capture",frame)
                
                #Wait for Key Pressed- 'q' then the loop will stop
                key_pressed=cv2.waitKey(1) & 0xFF
                if key_pressed==ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
        
        #Play music
        elif "play music" in Input:
            mixer.init()
            mixer.music.load('tune.mp3')
            mixer.music.play()
            time.sleep(28)

        #Open Picture
        elif "open photos" in Input:
            img=cv2.imread('picture.jpg')
            cv2.imshow("Picture",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        #Create a list
        elif "create a list" in Input or "make a list" in Input:
            talk("Creating a list")
            talk("How many items in list? ")
            Input=GivenCommand()
            n=int(Input)
            with open("List.txt",'w', encoding='utf-8') as f:
                for i in range(n):
                    talk('Item {}'.format(i+1))
                    Input=GivenCommand()
                    Input +='\n'
                    f.write(Input)
            f.close()
            time.sleep(10)

        # Open system apps
        elif "open calculator" in Input: 
            subprocess.Popen('C:\\Windows\\System32\\calc.exe')
            talk("Opening Calculator")
        
        elif "open notepad" in Input:
            subprocess.Popen('C:\\Windows\\System32\\notepad.exe')
            talk('Opening Notepad')

        # Tell me a joke
        elif "tell me a joke" in Input:
            url="http://api.icndb.com/jokes/random"
            r=requests.get(url)
            joke=json.loads(r.content)
            j=joke['value']['joke']
            talk(j)

        # Search for a location
        elif "where is" in Input:
            Input = Input.split(" ")
            location_url = "https://www.google.com/maps/place/" + str(Input[2])
            talk("Opening Google Maps")
            webbrowser.open(location_url)
            time.sleep(20)  

        # Check the weather
        elif "what is the weather in" in Input:
            api_key = "9cdedbfe1ab9f8b235bec19928f63509"
            weather_url = "http://api.openweathermap.org/data/2.5/weather?"
            Input = Input.split(" ")
            location = str(Input[5])
            url = weather_url + "appid=" + api_key + "&q=" + location 
            js = requests.get(url).json() 
            if js["cod"] != "401": 
                weather = js["main"] 
                temp = weather["temp"] 
                hum = weather["humidity"] 
                desc = js["weather"][0]["description"]
                resp_string = " The temperature " + str(temp)+" Kelvin. " + "The humidity is " + str(hum) + " and The weather description is "+ str(desc)
                talk(resp_string)

        # Random Fact
        elif "tell me a fact" in Input:
            url="https://uselessfacts.jsph.pl/random.json?language=en"
            f=requests.get(url).json()
            fact=f['text']
            talk(str(fact))

        # Show images of Mars Rover NASA
        elif "show me images of mars" in Input:
            DEMO_KEY="q6Qzoy7WYZxnzVUFQpH4DzKd9SxL0mS2djz6gdPR"
            url="https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key="+DEMO_KEY
            m=requests.get(url).json()
            no=random.randint(0,855)
            mars=m['photos'][no]
            mars_img=mars['img_src']
            webbrowser.open(mars_img)

        # COVID-19 Tracker
        elif "tell me about coronavirus" or "tell me about corona virus" in Input:
            covid_url="https://api.covid19api.com/summary"
            covid_js=requests.get(covid_url).json()
            data=covid_js["Global"]
            
            total_cases=data["TotalConfirmed"]
            total_deaths=data["TotalDeaths"]
            total_recovered=data["TotalRecovered"]

            talk('Total Cases: '+ str(total_cases))
            talk('Total Deaths: '+ str(total_deaths))
            talk('Total Recovered: '+ str(total_recovered))
        
        elif "corona virus in " in Input:
            Input = Input.split(" ")
            country_url="https://api.covid19api.com/country/" + str(Input[-1])
            covid_js=requests.get(country_url).json()
            data=covid_js[-1]
            cn_confirmed=data["Confirmed"]
            cn_deaths=data["Deaths"]
            cn_recovered=data["Recovered"]
            cn_active=data["Active"]

            talk('Confirmed Cases: '+ str(cn_confirmed))
            talk('Total Deaths: '+ str(cn_deaths))
            talk('Total Recovered: '+ str(cn_recovered))
            talk('Active Cases: '+ str(cn_active))
                      

        else:
            Input = Input
            talk('Searching...')
            try:
                try:
                    res = client.Input(Input)
                    outputs = next(res.outputs).text
                    talk('Alpha says')
                    talk('Gotcha')
                    talk(outputs)

                except:
                    outputs = wikipedia.summary(Input, sentences=3)
                    talk('Gotcha')
                    talk('Wikipedia says')
                    talk(outputs)


            except:
                    talk("searching on google for " + Input)
                    say = Input.replace(' ', '+')
                    webbrowser.open('https://www.google.co.in/search?q=' + Input)


        time.sleep(3)
        talk('Next Command! Please!')

