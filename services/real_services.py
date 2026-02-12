import io
import time
import os
from services.interfaces import AIService, STTService, TTSService
from gtts import gTTS
try:
    import speech_recognition as sr
    HAS_SR = True
except ImportError:
    HAS_SR = False
    print("SpeechRecognition not found. STT will be disabled.")

class GTTSService(TTSService):
    def speak(self, text: str) -> bytes:
        """Converts text to audio using Google Text-to-Speech and plays it locally."""
        try:
            print(f"Generating TTS for: {text}")
            tts = gTTS(text=text, lang='en')
            # Save to a temporary file for pygame to play
            temp_file = "temp_speech.mp3"
            tts.save(temp_file)
            
            # Initialize pygame mixer
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            pygame.mixer.quit()
            
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
            return b"played_locally" # Return specific indicator or empty bytes since we played it
        except Exception as e:
            print(f"TTS Error: {e}")
            return b""

class WhisperSTTService(STTService):
    def __init__(self, model_size="base"):
        if HAS_SR:
            print(f"Initializing SpeechRecognition (Google Web Speech API)...")
            self.recognizer = sr.Recognizer()
        else:
            print("STT disabled due to missing library.")

    def transcribe(self, audio_data: bytes) -> str:
        """Converts audio bytes to text using Google Web Speech API."""
        if not HAS_SR:
             return "Error: STT library not available."

        try:
            # Create a file-like object from bytes
            audio_file = io.BytesIO(audio_data)
            
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            # Recognize using Google Web Speech API (free, reliable for short audio)
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "" # Could not understand audio
        except sr.RequestError as e:
            print(f"STT API Error: {e}")
            return ""
        except Exception as e:
            print(f"STT Error: {e}")
            return ""

    def listen_and_transcribe(self):
        """Listens to the microphone and transcribes."""
        if not HAS_SR:
            return "Error: STT not available"
            
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            try:
                # Listen with a timeout to prevent hanging forever
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing audio...")
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.WaitTimeoutError:
                return "" # No speech detected
            except sr.UnknownValueError:
                return "" # Unintelligible
            except Exception as e:
                print(f"Listening Error: {e}")
                return ""

class RuleBasedAIService(AIService):
    def generate_response(self, prompt: str, context_data: dict = None) -> str:
        """Generates a response based on keywords and current context (recipe/step)."""
        prompt = prompt.lower()
        
        # Default responses if no context
        if not context_data:
             if "hello" in prompt or "hi" in prompt:
                return "Hello! I am your cooking assistant. Please select a recipe to get started."
             return "Please select a recipe so I can help you cook!"

        recipe = context_data.get("recipe") # This might be the Recipe object
        current_step_index = context_data.get("step_index", 0)
        
        if not recipe:
             return "I don't see a recipe selected yet."

        # Ingredients Query
        if "ingredient" in prompt or "shopping" in prompt or "what do i need" in prompt:
            # Create a summary of ingredients
            # Assuming 'recipe' is the Recipe object from models.py
            # If it were a dict, we'd access differently. app.py passes the object.
            ingredients_list = ", ".join([f"{ing.quantity} {ing.unit} of {ing.ingredient_id}" for ing in recipe.ingredients])
            return f"You need: {ingredients_list}."

        # Navigation / Step Queries
        steps_count = len(recipe.steps)
        
        if "next" in prompt or "after" in prompt:
            if current_step_index + 1 < steps_count:
                 import random
                 
                 # Safety Checks
                 instruction = recipe.steps[current_step_index + 1].instruction
                 safety_warning = ""
                 
                 # Define dangerous keywords and their corresponding actions
                 danger_map = {
                     "cut": "cutting", "chop": "chopping", "slice": "slicing", "knife": "using a knife",
                     "boil": "cooking with hot water", "hot": "handling hot items", "fire": "using fire",
                     "heat": "heating", "stove": "using the stove", "oven": "using the oven",
                     "fry": "frying", "oil": "cooking with hot oil",
                     "blend": "blending"
                 }
                 
                 found_actions = []
                 for keyword, action in danger_map.items():
                     if keyword in instruction.lower():
                         found_actions.append(action)
                 
                 if found_actions:
                     # Pick the first detected action for the warning or generic if complex
                     action = found_actions[0]
                     safety_warning = f"⚠️ CAUTION: Be careful while {action}! "
                 
                 # Encouragement
                 encouragements = [
                     "You are doing great!", "Good job!", "Keep it up!", 
                     "You're a chef in the making!", "Doing excellent so far!"
                 ]
                 encouragement = f" {random.choice(encouragements)}" if random.random() < 0.3 else ""
                 
                 return f"{safety_warning}Moving to step {current_step_index + 2}: {instruction}{encouragement}"
            else:
                return "You are at the last step. Enjoy your meal!"

        elif "previous" in prompt or "back" in prompt or "last step" in prompt:
             if current_step_index > 0:
                 return f"Going back to step {current_step_index}: {recipe.steps[current_step_index - 1].instruction}"
             else:
                 return "You are at the first step."

        elif "repeat" in prompt or "say again" in prompt or "current step" in prompt or "what is the step" in prompt:
             if 0 <= current_step_index < steps_count:
                 instruction = recipe.steps[current_step_index].instruction
                 
                 # Safety Checks (Simplified for repeat)
                 danger_keywords = ["cut", "chop", "slice", "knife", "boil", "hot", "fire", "heat", "stove", "oven", "fry", "oil", "blend"]
                 safety_warning = ""
                 if any(k in instruction.lower() for k in danger_keywords):
                      safety_warning = "Remember to be careful! "

                 return f"{safety_warning}Step {current_step_index + 1}: {instruction}"
             else:
                 return "I couldn't find the current step."

        # General Greetings
        elif "hello" in prompt or "hi" in prompt:
            return f"Hello! We are cooking {recipe.name}. We are on step {current_step_index + 1}."


        elif "thank" in prompt:
            return "You are welcome! Happy cooking."

        # Timer Logic
        elif "timer" in prompt and ("set" in prompt or "start" in prompt):
            # Extract time
            import re
            match = re.search(r'(\d+)\s*(minute|min)', prompt)
            if match:
                 minutes = int(match.group(1))
                 return f"[TIMER: {minutes}] Okay, setting a timer for {minutes} minutes."
            else:
                 return "I can set a timer for you. Just say 'Set a timer for 10 minutes'."

        else:
            return f"I'm not sure. We are currently on step {current_step_index + 1} of {recipe.name}. You can say 'Next Step', 'Repeat', or 'Ingredients'."
