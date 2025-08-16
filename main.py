import json
import pyttsx3
import speech_recognition as sr
from automation import get_school_info  # Assuming it's still used for any specific info extraction
from ai_response import get_response  # Assuming this is your AI response handler
import os

# Text-to-speech setup
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    # Optional: Print to console for debugging
    print(f"JARVIS: {text}")  # Remove or comment in production
    engine.say(text)
    engine.runAndWait()

# Speech recognition
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return "Error with Speech Recognition service."

# Hybrid response
def get_final_answer(query):
    local_answer = get_school_info(query)
    if local_answer:
        return local_answer
    return get_response(query)

# MAIN LOOP
print("✅ JARVIS 2.0 Ready!")
speak("Hello! I am GYAN — your Guided Youth Assistance Network. How can I help you today?")
while True:
    user_input = listen()
    if user_input:
        print(f"👤 You: {user_input}")
        # Check if the query matches school data first
        answer = get_final_answer(user_input)
        if not answer:
            answer = get_response(user_input)
        
        if answer:
            speak(answer)
        else:
            speak("I couldn't find any information related to that.")
        
    # Exit command to stop the assistant
    if "exit" in user_input.lower() or "stop" in user_input.lower():
        speak("Goodbye!")
        break
