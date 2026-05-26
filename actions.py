import os
import webbrowser
import datetime
import requests
import re
import threading
import time
import wikipedia
import pyttsx3
import subprocess  # Opens apps without freezing your Streamlit app!

def run_timer(minutes):
    """Runs a timer in the background and speaks when finished."""
    time.sleep(minutes * 60)
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(f"Your {minutes} minute timer is up!")
    engine.runAndWait()

def execute_command(intent, user_text):
    # Force everything to lowercase so it's easier to match
    user_text = user_text.lower()

    # --- KEYWORD OVERRIDES ---
    
    # 1. Identity
    if "who are you" in user_text:
        return "I'm Siri Mini — your smart voice assistant, always ready to help!"
        
    # 2. Date and Time combined
    elif "date" in user_text:
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M %p")
        return f"It's {time_str} on {date_str}."

    # 3. Timer
    elif "timer" in user_text:
        match = re.search(r'(\d+)\s*minute', user_text)
        mins = int(match.group(1)) if match else 2
        threading.Thread(target=run_timer, args=(mins,), daemon=True).start()
        return f"Timer set for {mins} minutes. I'll notify you when it's done!"

    # 4. Open GitHub
    elif "github" in user_text or "git hub" in user_text:
        webbrowser.open("https://github.com")
        return "Opening GitHub right away."

    # 5. Open Gmail
    elif "gmail" in user_text or "mail" in user_text:
        webbrowser.open("https://mail.google.com")
        return "Opening your Gmail inbox."

    # 6. Open Notepad
    elif "notepad" in user_text or "note pad" in user_text:
        try:
            subprocess.Popen(["notepad.exe"])
            return "Opening Notepad for you."
        except:
            return "I couldn't open Notepad on this system."

    # 7. Google Maps
    elif "map" in user_text or "navigate" in user_text:
        webbrowser.open("https://maps.google.com")
        return "Opening Google Maps."

    # 8. General Questions (Wikipedia Fallback)
    elif "what is" in user_text or "who is" in user_text:
        search_query = user_text.replace("what is", "").replace("who is", "").replace("siri", "").strip()
        try:
            answer = wikipedia.summary(search_query, sentences=1)
            return answer
        except:
            return f"I couldn't find a quick answer for {search_query}, but I can search the web."


    # --- EXISTING ML INTENTS ---
    
    if intent == "open_youtube":
        # Strips out extra words so it searches cleanly
        query = user_text.replace("play", "").replace("on youtube", "").replace("search for", "").replace("siri", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        return f"Searching YouTube for '{query}'..."

    # ---------------------------------------------------------
    # CALCULATOR FIX: Calculates math AND opens the app!
    # ---------------------------------------------------------
    elif intent == "calculator":
        clean_text = user_text.replace("plus", "+").replace("minus", "-").replace("multiply", "*").replace("divide", "/")
        
        # Remove all spaces so equations stick together (e.g., "2 + 2" becomes "2+2")
        clean_text = clean_text.replace(" ", "")
        
        math_expression = re.findall(r'[\d\+\-\*\/\.]+', clean_text)
        
        # Make sure it actually found an equation with an operator (+, -, *, /)
        if math_expression and any(op in math_expression[0] for op in "+-*/"):
            try:
                result = eval(math_expression[0])
                
                # ---> NEW: Open the Windows Calculator app on the screen! <---
                subprocess.Popen(["calc.exe"])
                
                return f"The result is {result}"
            except:
                subprocess.Popen(["calc.exe"])
                return "Opened the Calculator App."
        else:
            subprocess.Popen(["calc.exe"])
            return "Opened the Calculator App."

    elif intent == "weather":
        search_query = user_text.replace(" ", "+")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        return "Opening Google to show you the weather."

    elif intent == "time":
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {now}."

    elif intent == "joke":
        return "Why don't scientists trust atoms? Because they make up everything!"

    elif intent == "open_google":
        webbrowser.open("https://www.google.com")
        return "Opened Google."
        
    return "I've completed the task for you."