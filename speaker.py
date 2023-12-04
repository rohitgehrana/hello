# Import statements moved outside the loop
from openai import OpenAI
import os
import pygame
from datetime import date, datetime
import requests
import tempfile
from io import BytesIO
from pydub import AudioSegment
import speech_recognition as sr
import RPi.GPIO as GPIO
import time



# Additional imports
from pydub import AudioSegment

# Set your OpenAI API key as an environment variable
api_key = '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'
os.environ["OPENAI_API_KEY"] = api_key

# Initialize Pygame and OpenAI client outside the loop
pygame.init()
client = OpenAI()

# AI BRAIN
user_conversation = [
    {"role": "system", "content": "Your name is Alfa and you are a human-like robot whose work is to communicate with humans. You can remember names."}
]

today_date = date.today()
formatted_date = today_date.strftime("%Y-%m-%d")
date_str = f"Todays date is {formatted_date}"
memory_date = {"role": "system", "content": date_str}
user_conversation.append(memory_date)

current_time = datetime.now().strftime("%H:%M:%S")
time_str = f"Todays time is {current_time}"
memory_time = {"role": "system", "content": time_str}
user_conversation.append(memory_time)


base_url = "http://api.openweathermap.org/data/2.5/weather"
params = {'q': "Aligarh", 'appid': "801be14c2efc7b5f99aa63fb4459aa48"}

try:
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

    data = response.json()
    
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    temp = f"Weather in Aligarh is {weather_description} and Temperature is {int(temperature-273.15)}°C"
    user_conversation.append({"role": "system", "content": temp})
    
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    pass

listener = sr.Recognizer()


GPIO.setmode(GPIO.BCM)
mic_gpio_pin = 7
GPIO.setup(mic_gpio_pin, GPIO.IN)



# LOOP
while True:
    def take_command():
        try:
            with sr.Microphone(device_index=mic_gpio_pin) as source:
                print('Listening...')
                audio = listener.listen(source)
                command = listener.recognize_google(audio)
                command = command.lower()
                if 'alexa' in command:
                    command = command.replace('alpha', '')
                    print(command)
                    return command
                else:
                    take_command()
        except sr.UnknownValueError:
            print("Sorry, I did not hear your request. Please repeat.")
            take_command()
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")
            take_command()

    # USER PROMPT
    
    prompt = take_command()

    # MEMORIES HOUSE
    user_conversation.append({"role": "user", "content": prompt})

    # THOUGHTS HOUSE
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=user_conversation)
    response_message = response.choices[0].message.content
    user_conversation.append({"role": "assistant", "content": response_message})

    print(response_message)



    # ... (your existing code)

    # TEXT TO SPEECH CORNER
    response_audio = client.audio.speech.create(model="tts-1", voice="alloy", input=response_message)

    # Convert audio content to BytesIO
    audio_data = BytesIO(response_audio.content)

    # Load the audio data into pydub
    audio = AudioSegment.from_file(audio_data, format="mp3")

    # Save audio to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_filename = temp_file.name
    audio.export(temp_filename, format="wav")
    temp_file.close()

    pygame.mixer.init()

    # Load the temporary WAV file as a pygame Sound object
    sound = pygame.mixer.Sound(temp_filename)

    # Play the audio
    sound.play()

    # Wait for the sound to finish playing
    pygame.time.wait(int(sound.get_length() * 1000))  # Convert seconds to milliseconds

    # Cleanup
    pygame.mixer.quit()
