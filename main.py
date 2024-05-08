# Gupta Neelesh Kumar, 374371, Variant 1

# The following program can take commands:
# To show picture: "show picture", "show photo", "show pictures", "picture", "image", "images", "photo"
# To save picture: "download picture", "download", "save picture", "save"
# To name the breed: "name breed", "name"
# To exit: "exit", "stop"


import time
import requests
import pyttsx3
import json
from vosk import Model, KaldiRecognizer
import pyaudio

engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


model = Model("vosk-model-small-en-us-0.15") # use model vosk-model-small-en-in-0.4 if it has difficulty in recognizing
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
                frames_per_buffer=2048)  # To adjust Buffer
stream.start_stream()


def listen():
    start_time = time.time()
    while True:
        data = stream.read(4096)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            return result.get("text", "")
        if time.time() - start_time > 5:  # 5 seconds timeout
            return ""


def fetch_dog_image():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    if response.status_code == 200:
        data = response.json()
        image_url = data["message"]
        print("Here's a random dog image: " + image_url)
        speak("Here's a random dog image.")
        return image_url
    else:
        speak("Error fetching dog image")
        return None


def save_image(url):
    if url:
        response = requests.get(url)
        if response.status_code == 200:
            filename = url.split("/")[-1]
            with open(filename, 'wb') as f:
                f.write(response.content)
            speak("Image saved as " + filename)
        else:
            speak("Failed to save the image.")
    else:
        speak("No image URL provided.")


def name_the_breed(url):
    if url:
        breed = url.split("/")[-2]
        speak("The breed of the dog is " + breed)
    else:
        speak("No image URL provided to determine the breed.")


# Main function
def main():
    speak("Voice assistant started. I can 'show picture', 'download picture', 'name the breed', or 'exit'.")
    image_url = None
    while True:
        print("Say something...")
        command = listen()
        print("You said: ", command)
        if command:
            if any(word in command for word in
                   ["show picture", "show photo", "show pictures", "picture", "image", "images", "photo"]):
                image_url = fetch_dog_image()
            elif any(word in command for word in ["download picture", "download", "save picture", "save"]):
                if image_url:
                    save_image(image_url)
                else:
                    speak("No image to download. Please ask for a picture first.")
            elif any(word in command for word in ["name breed", "name"]):
                if image_url:
                    name_the_breed(image_url)
                else:
                    speak("No image to determine the breed. Please ask for a picture first.")
            elif any(word in command for word in ["exit", "stop"]):
                speak("Exiting.")
                break
            else:
                speak("Command not recognized.")
        else:
            speak("No input recognized. Please try again.")


if __name__ == "__main__":
    main()
