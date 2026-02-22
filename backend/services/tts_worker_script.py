import sys
import pyttsx3
import argparse

def generate_speech(text, gender, output_file):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        target_voice = None
        gender = gender.lower()
        
        # 1. Precise Name Matching
        for voice in voices:
            name = voice.name.lower()
            if gender == "male":
                if "david" in name:
                    target_voice = voice
                    break
            else: # female
                if "zira" in name:
                    target_voice = voice
                    break
                elif "hazel" in name and not target_voice:
                    target_voice = voice
                    
        # 2. Heuristic
        if not target_voice and voices:
            count = len(voices)
            if gender == "male":
                target_voice = voices[0]
            else:
                target_voice = voices[1] if count > 1 else voices[0]
        
        if target_voice:
            engine.setProperty('voice', target_voice.id)
            
        print(f"Generating audio for '{text}'...")
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        print("Done.")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--gender", default="female")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    
    generate_speech(args.text, args.gender, args.output)
