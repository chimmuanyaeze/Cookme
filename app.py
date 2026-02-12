import streamlit as st
import os
import time
from PIL import Image, ImageOps
from logic.models import IngredientManager, RecipeManager
from logic.localization import LocalizationService
from services.factory import ServiceFactory

# --- Configuration ---
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'images')
INGREDIENTS_FILE = os.path.join(DATA_DIR, 'ingredients', 'ingredients.json')
RECIPES_FILE = os.path.join(DATA_DIR, 'recipes', 'recipes.json')

# --- Initialization ---
@st.cache_resource
def load_managers():
    try:
        ingredient_manager = IngredientManager(INGREDIENTS_FILE)
        recipe_manager = RecipeManager(RECIPES_FILE)
        return ingredient_manager, recipe_manager
    except FileNotFoundError as e:
        st.error(f"Error loading data: {e}")
        return None, None

@st.cache_resource
def load_services():
    try:
        return (
            ServiceFactory.get_ai_service("real"),
            ServiceFactory.get_stt_service("real"),
            ServiceFactory.get_tts_service("real")
        )
    except Exception as e:
        st.error(f"Failed to load real services, falling back to mock: {e}")
        return (
            ServiceFactory.get_ai_service("mock"),
            ServiceFactory.get_stt_service("mock"),
            ServiceFactory.get_tts_service("mock")
        )

ingredient_manager, recipe_manager = load_managers()
with st.spinner("Loading Voice Models... (This may take a moment)"):
    ai_service, stt_service, tts_service = load_services()

if not ingredient_manager or not recipe_manager:
    st.stop()

localization_service = LocalizationService(ingredient_manager)

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "listening_active" not in st.session_state:
    st.session_state.listening_active = False
if "timer_end_time" not in st.session_state:
    st.session_state.timer_end_time = None
if "page" not in st.session_state:
    st.session_state.page = "splash"
if "selected_recipe_id" not in st.session_state:
    st.session_state.selected_recipe_id = None
if "voice_paused" not in st.session_state:
    st.session_state.voice_paused = False

def navigate_to(page, recipe_id=None):
    st.session_state.page = page
    if recipe_id:
        st.session_state.selected_recipe_id = recipe_id
    if page == "cooking" or page == "recipe":
        st.session_state.current_step = 0 # Reset step when starting cooking or viewing new recipe
    st.rerun()

# --- Custom CSS ---
# --- Theme Management ---
def get_css(theme):
    if theme == "Dark":
        bg_color = "#0f172a" # Slate 900
        text_color = "#f1f5f9" # Slate 100
        card_bg = "#1e293b" # Slate 800
        card_border = "1px solid #E76F51"
        step_box_bg = "#1e293b"
        step_box_text = "#f1f5f9"
        highlight_bg = "#334155" # Slate 700
    else:
        bg_color = "#f8fafc" # Slate 50
        text_color = "#1B3B5A" # Deep Blue
        card_bg = "#ffffff"
        card_border = "1px solid #e0e0e0"
        step_box_bg = "#ffffff"
        step_box_text = "#1B3B5A"
        highlight_bg = "#fff8f5"

    return f"""
<style>
    /* Global Styles */
    .stApp {{
        background-color: {bg_color};
        color: {text_color} !important;
    }}
    
    p, li, div, span, h1, h2, h3, h4, h5, h6 {{
        color: {text_color} !important; 
    }}

    /* Card Styles */
    div[data-testid="stVerticalBlock"] > div > div > div[data-testid="stVerticalBlock"] {{
        background-color: {card_bg};
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border: {card_border};
    }}

    /* Cooking Step Box */
    .step-box {{
        background-color: {step_box_bg};
        color: {step_box_text};
        border-left: 6px solid #E76F51;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    
    .highlighted-step {{
         border: 2px solid #E76F51;
         background-color: {highlight_bg};
    }}
    
    /* Timer */
    .timer-box {{
        background-color: #2A9D8F;
        color: white !important; 
        padding: 15px; 
        border-radius: 8px; 
        text-align: center; 
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    .timer-box h3 {{
        color: white !important;
    }}
</style>
"""


# --- UI Layout ---
st.set_page_config(
    page_title="AI Cooking Assistant",
    page_icon="🍳",
    layout="wide"
)

# --- Sidebar: Settings ---
st.sidebar.title("Settings ⚙️")
languages = {
    "English": "english",
    "Igbo": "igbo",
    "Yoruba": "yoruba",
    "Hausa": "hausa"
}
selected_language_label = st.sidebar.selectbox("Choose Ingredient Language", list(languages.keys()))
selected_language_code = languages[selected_language_label]

st.sidebar.divider()
st.sidebar.subheader("App Theme 🎨")
selected_theme = st.sidebar.radio("Theme", ["Light", "Dark"], index=0)
st.markdown(get_css(selected_theme), unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.subheader("Voice Assistant 🎙️")
enable_voice = st.sidebar.toggle("Enable Voice Mode")
mode = "Manual"
if enable_voice:
    mode = st.sidebar.radio("Voice Mode", ["Manual (Push-to-Talk)", "Hands-Free (Continuous)"], horizontal=True)

# --- Main Area ---
# st.title("🍳 AI Cooking Assistant") # Moved to render functions

def render_splash():
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h1 style="font-size: 3em;">Welcome to AI Cooking Assistant 🍳</h1>
        <p style="font-size: 1.5em; color: #666;">Your smart kitchen companion for delicious meals.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("Enter Kitchen 🚀", use_container_width=True, type="primary"):
            navigate_to("home")

# Helper for consistent image sizing
def load_and_resize_image(image_path, size=(600, 400)):
    try:
        img = Image.open(image_path)
        # Handle RGBA -> RGB if necessary for saving, but for display it's fine.
        # ImageOps.fit crops to center to enforce aspect ratio
        img = ImageOps.fit(img, size, Image.Resampling.LANCZOS)
        return img
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

def render_home():
    st.title("🏠 Recipe Library")
    
    # Search
    search_query = st.text_input("🔍 Search recipes...", "").lower()
    
    recipes = recipe_manager.get_all_recipes()
    filtered_recipes = [r for r in recipes if search_query in r.name.lower() or search_query in r.category.lower()]
    
    if not filtered_recipes:
        st.info("No recipes found matching your search.")
        return

    # Grid Display
    cols = st.columns(3)
    for i, recipe in enumerate(filtered_recipes):
        with cols[i % 3]:
            # Card Container
            with st.container():
                st.markdown(f"### {recipe.name}")
                image_name = recipe.media.get("image")
                if image_name:
                    image_path = os.path.join(ASSETS_DIR, image_name)
                    if os.path.exists(image_path):
                        # Use helper to resize
                        img = load_and_resize_image(image_path, size=(600, 400))
                        if img:
                            st.image(img, width="stretch")
                
                st.caption(f"⏱️ {recipe.estimated_time_minutes} min | ⚡ {recipe.difficulty}")
                if st.button(f"Cook {recipe.name}", key=f"btn_{recipe.id}"):
                    navigate_to("recipe", recipe.id)
                st.markdown("---")

def render_recipe(selected_recipe):
    if st.button("← Back to Recipes"):
        navigate_to("home")
        
    st.title(f"🍳 {selected_recipe.name}")

    # Recipe Header
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"## {selected_recipe.name}")
        st.caption(f"📍 Origin: {selected_recipe.origin.get('country', 'Unknown')} | {selected_recipe.origin.get('region', '')} - {selected_recipe.origin.get('ethnic_group', '')}")
        st.caption(f"📂 Category: {selected_recipe.category} | ⚡ Difficulty: {selected_recipe.difficulty}")
        st.caption(f"⏱️ Time: {selected_recipe.estimated_time_minutes} mins | 🍽️ Serves: {selected_recipe.serving_size}")

    with col2:
        # Load Image
        image_name = selected_recipe.media.get("image")
        if image_name:
             image_path = os.path.join(ASSETS_DIR, image_name)
             if os.path.exists(image_path):
                 # Larger size for detail view
                 img = load_and_resize_image(image_path, size=(800, 500))
                 if img:
                     st.image(img, width="stretch")
             else:
                 st.info(f"Image not found: {image_name}")
        else:
             st.info("No image available")

    # --- Interactive Companion (within Recipe Page) ---
    if enable_voice:
        with st.expander("💬 Interactive Companion History", expanded=True):
            st.markdown("Here you can see your conversation with the assistant.")
            with st.container(height=300):
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

    st.markdown("---")

    # Ingredients Section
    st.subheader("🛒 Ingredients")
    
    cols = st.columns(2)
    for i, ingredient in enumerate(selected_recipe.ingredients):
        col = cols[i % 2]
        localized_name = localization_service.localize_ingredient(ingredient.ingredient_id, selected_language_code)
        
        # Unique key for checklist
        key = f"ing_{selected_recipe.id}_{ingredient.ingredient_id}"
        
        with col:
             # Use Streamlit's native checkbox for better state management
             is_checked = st.checkbox(
                 f"{localized_name} ({ingredient.quantity} {ingredient.unit})",
                 key=key,
                 help="Optional" if ingredient.optional else "Required"
             )
             if ingredient.optional:
                 st.caption("(Optional)")

    st.markdown("---")

    # Steps Section (Preview)
    with st.expander("View Cooking Steps Preview"):
         st.subheader("🔥 Cooking Steps (Preview)")
         for i, step in enumerate(selected_recipe.steps):
             with st.container():
                 st.markdown(f"**Step {step.step_number}**: {step.instruction}")

    st.markdown("---")
    
    # Start Cooking Validation
    if st.button("🚀 Start Cooking", type="primary", use_container_width=True):
        missing_ingredients = []
        for ing in selected_recipe.ingredients:
            if not ing.optional:
                # Checkbox key format: f"ing_{selected_recipe.id}_{ing.ingredient_id}"
                key = f"ing_{selected_recipe.id}_{ing.ingredient_id}"
                if not st.session_state.get(key, False):
                    # Get localized name for the warning
                    name = localization_service.localize_ingredient(ing.ingredient_id, selected_language_code)
                    missing_ingredients.append(name)
        
        if missing_ingredients:
            st.error(f"⚠️ You must have the following ingredients to start: {', '.join(missing_ingredients)}")
        else:
            navigate_to("cooking")

def render_cooking(selected_recipe):
    st.title(f"🔥 Cooking: {selected_recipe.name}")
    
    # Progress Bar
    progress = (st.session_state.current_step + 1) / len(selected_recipe.steps)
    st.progress(progress, text=f"Step {st.session_state.current_step + 1} of {len(selected_recipe.steps)}")
    
    # Current Step Display
    current_step_index = st.session_state.current_step
    if 0 <= current_step_index < len(selected_recipe.steps):
        step = selected_recipe.steps[current_step_index]
        
        st.markdown(f"""
        <div style="background-color: {'#1e293b' if st.session_state.get('theme', 'Light') == 'Dark' else '#1B3B5A'}; color: white; padding: 40px; border-radius: 15px; text-align: center; margin: 20px 0; box-shadow: 0 10px 20px rgba(0,0,0,0.15);">
            <h2 style="color: #E76F51; margin-bottom: 20px;">Step {step.step_number}</h2>
            <p style="font-size: 1.8em; line-height: 1.4; color: white !important;">{step.instruction}</p>
            <br>
            <p style="color: #bdc3c7;"><i>💡 Tip: {step.tip if step.tip else 'No tips for this step.'}</i></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("🎉 Cooking Complete! Enjoy your meal.")
        if st.button("Finish & Return Home"):
            navigate_to("home")
        return

    # Navigation Buttons
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("⬅️ Previous Step", disabled=(current_step_index == 0), use_container_width=True):
            st.session_state.current_step -= 1
            st.rerun()
            
    with col_next:
        if current_step_index < len(selected_recipe.steps) - 1:
            if st.button("Next Step ➡️", type="primary", use_container_width=True):
                st.session_state.current_step += 1
                st.rerun()
        else:
             if st.button("Finish Cooking 🏁", type="primary", use_container_width=True):
                 st.balloons()
                 st.success("You finished the recipe!")
                 time.sleep(2)
                 navigate_to("home")

    if st.button("Exit Cooking Mode"):
        navigate_to("recipe", selected_recipe.id)

# --- Timer Display ---
if st.session_state.timer_end_time:
    remaining_time = st.session_state.timer_end_time - time.time()
    if remaining_time > 0:
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        st.markdown(f"""
        <div class="timer-box">
            <h3 style="color: white; margin:0;">⏳ Timer: {minutes:02d}:{seconds:02d}</h3>
        </div>
        """, unsafe_allow_html=True)
        # Force rerun to update timer (simple polling)
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.timer_end_time = None
        st.success("🔔 TIMER DONE!")
        # Optional: Play sound here if desired
        if enable_voice:
             tts_service.speak("Time is up!")



# --- Page Routing ---
if st.session_state.page == "splash":
    render_splash()

elif st.session_state.page == "home":
    render_home()

elif st.session_state.page == "recipe":
    # Get recipe from ID
    recipe_id = st.session_state.selected_recipe_id
    selected_recipe = recipe_manager.get_recipe(recipe_id)
    
    if selected_recipe:
        render_recipe(selected_recipe)
    else:
        st.error("Recipe not found.")
        if st.button("Go Home"):
            navigate_to("home")

elif st.session_state.page == "cooking":
    recipe_id = st.session_state.selected_recipe_id
    selected_recipe = recipe_manager.get_recipe(recipe_id)
    if selected_recipe:
        render_cooking(selected_recipe)
    else:
         navigate_to("home")




# --- Voice Logic (Sidebar) ---
# Logic moved to sidebar to stay persistent and visible without scrolling
if enable_voice:
    with st.sidebar:
        st.divider()
        st.subheader("🎙️ Voice Controls")
        
        if mode == "Manual (Push-to-Talk)":
            # Audio Input
            audio_value = st.audio_input("Speak")
            text_input = st.chat_input("Type command...")
            user_text = None
            
            if "last_audio_hash" not in st.session_state:
                st.session_state.last_audio_hash = None
    
            if audio_value:
                 audio_bytes = audio_value.read()
                 import hashlib
                 audio_hash = hashlib.md5(audio_bytes).hexdigest()
                 
                 if audio_hash != st.session_state.last_audio_hash:
                     st.session_state.last_audio_hash = audio_hash
                     
                     with st.spinner("Listening..."):
                         transcribed = stt_service.transcribe(audio_bytes)
                         if transcribed and not transcribed.startswith("Error"):
                             user_text = transcribed
                         else:
                             st.warning("Could not understand audio.")
            
            if text_input:
                user_text = text_input
    
            if user_text:
                st.session_state.messages.append({"role": "user", "content": user_text})
                # Prepare Context
                selected_recipe = None
                if st.session_state.selected_recipe_id:
                     selected_recipe = recipe_manager.get_recipe(st.session_state.selected_recipe_id)

                context_data = {
                    "recipe": selected_recipe,
                    "step_index": st.session_state.current_step
                }
                ai_response = ai_service.generate_response(user_text, context_data=context_data)
                
                # Check for Timer Tag
                import re
                timer_match = re.search(r'\[TIMER:\s*(\d+)\]', ai_response)
                if timer_match:
                    minutes = int(timer_match.group(1))
                    st.session_state.timer_end_time = time.time() + (minutes * 60)
                    ai_response = ai_response.replace(timer_match.group(0), "").strip()
    
                if "next" in user_text.lower():
                     if selected_recipe and st.session_state.current_step < len(selected_recipe.steps) - 1:
                         st.session_state.current_step += 1
                elif "previous" in user_text.lower() and st.session_state.current_step > 0:
                        st.session_state.current_step -= 1
                
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                audio_out = tts_service.speak(ai_response)
                if audio_out and audio_out != b"played_locally":
                    st.audio(audio_out, format="audio/mp3", autoplay=True)
                st.rerun()
    
        elif mode == "Hands-Free (Continuous)":
            st.info("Status: " + ("🟢 Listening" if st.session_state.listening_active else "🔴 Stopped"))
            
            col_start, col_stop = st.columns(2)
            if col_start.button("START 🟢", use_container_width=True):
                st.session_state.listening_active = True
                st.rerun()
            if col_stop.button("STOP 🔴", use_container_width=True):
                st.session_state.listening_active = False
                st.rerun()
                
            if st.session_state.listening_active:
                status_placeholder = st.empty()
                status_placeholder.info("🎧 Listening...")
                
                if hasattr(stt_service, 'listen_and_transcribe'):
                    text = ""
                    try:
                        text = stt_service.listen_and_transcribe()
                    except Exception as e:
                        status_placeholder.error(f"Error: {e}")
                        time.sleep(3)
                    
                    if text:
                        status_placeholder.success(f"Heard: '{text}'")
                        
                        # Status check for Pause
                        if st.session_state.voice_paused:
                            status_placeholder.warning("⏸️ Paused. Say 'Continue'...")
                            
                            if "continue" in text.lower() or "resume" in text.lower():
                                st.session_state.voice_paused = False
                                tts_service.speak("Resuming assistant.")
                                time.sleep(1)
                                st.rerun()
                            elif "stop" in text.lower() or "exit" in text.lower():
                                st.session_state.listening_active = False
                                st.session_state.voice_paused = False
                                tts_service.speak("Stopping assistant.")
                                st.rerun()
                            else:
                                time.sleep(1)
                                st.rerun()

                        # ACTIVE LISTENING COMMANDS
                        else:
                            if "stop" in text.lower() or "exit" in text.lower():
                                st.session_state.listening_active = False
                                tts_service.speak("Stopping.")
                                st.rerun()
                                
                            if "pause" in text.lower():
                                st.session_state.voice_paused = True
                                tts_service.speak("Paused.")
                                st.rerun()
    
                            valid_triggers = ["cooking assistant", "assistant", "next", "previous", "repeat", "ingredient", "shopping", "hello", "hi", "thank", "start", "begin"]
                            
                            if any(trigger in text.lower() for trigger in valid_triggers):
                                status_placeholder.info("🤖 Processing...")
                                st.session_state.messages.append({"role": "user", "content": text})
                                
                                # Get Context - REFRESH
                                selected_recipe = None
                                if st.session_state.selected_recipe_id:
                                    selected_recipe = recipe_manager.get_recipe(st.session_state.selected_recipe_id)

                                # Start Cooking Command
                                if ("start" in text.lower() or "begin" in text.lower()) and "timer" not in text.lower():
                                    if selected_recipe:
                                        st.session_state.page = "cooking"
                                        st.session_state.current_step = 0
                                        step1 = selected_recipe.steps[0]
                                        response_text = f"Starting {selected_recipe.name}. Step 1: {step1.instruction}"
                                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                                        tts_service.speak(response_text)
                                        st.rerun()
                                    else:
                                        status_placeholder.warning("Please select a recipe first.")
                                        tts_service.speak("Please select a recipe first.")
                                
                                context_data = {
                                    "recipe": selected_recipe,
                                    "step_index": st.session_state.current_step
                                }
                                ai_response = ai_service.generate_response(text, context_data=context_data)
                                
                                # Check for Timer Tag
                                import re
                                timer_match = re.search(r'\[TIMER:\s*(\d+)\]', ai_response)
                                if timer_match:
                                    minutes = int(timer_match.group(1))
                                    st.session_state.timer_end_time = time.time() + (minutes * 60)
                                    ai_response = ai_response.replace(timer_match.group(0), "").strip()

                                if "next" in text.lower():
                                    if selected_recipe and st.session_state.current_step < len(selected_recipe.steps) - 1:
                                        st.session_state.current_step += 1
                                elif "previous" in text.lower() and st.session_state.current_step > 0:
                                    st.session_state.current_step -= 1
                                    
                                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                                
                                # Speak response (blocking)
                                tts_service.speak(ai_response)
                                
                                time.sleep(1)
                                st.rerun()
                            else:
                                status_placeholder.warning(f"Ignored: '{text}'")
                                time.sleep(1)
                                st.rerun()
                    else:
                        # No speech detected or timeout
                        time.sleep(0.5)
                        st.rerun()
                else:
                    st.error("STT Service does not support continuous listening.")
