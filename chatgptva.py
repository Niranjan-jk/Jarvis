# Python program to translate
# speech to text and text to speech
import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv

# Load your environment variables
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

import openai
openai.api_key = OPENAI_KEY

# Function to convert text to speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Initialize the recognizer
r = sr.Recognizer()

def record_text():
    # Loop in case of errors
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("I'm listening")
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                return MyText
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occurred")

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5
    )
    message = response.choices[0].message['content']
    messages.append({"role": "assistant", "content": message})
    return message

# messages = [{"role": "user", "content": "Please act like Jarvis from Iron man."}]
messages = [
    {"role": "system", "content": "You are now connected to your AI assistant, Jarvis."},
    {"role": "user", "content": "Jarvis, provide me with a weather update for today."},
    {"role": "assistant", "content": "Of course, sir. The weather forecast for today is as follows..."},
    {"role": "user", "content": "Thank you, Jarvis. Can you also schedule a meeting for 2 PM?"},
    {"role": "assistant", "content": "Certainly, sir. Your meeting is scheduled for 2 PM."},
    {"role": "user", "content": "Jarvis, play some relaxing music, please."},
    {"role": "assistant", "content": "As you wish, sir. Playing relaxing music now."}
]

while True:
    user_input = record_text()
    messages.append({"role": "user", "content": user_input})
    response = send_to_chatGPT(messages)
    SpeakText(response)
    print("User: ", user_input)
    print("Assistant: ", response)
