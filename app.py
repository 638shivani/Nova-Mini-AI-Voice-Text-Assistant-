import streamlit as st
import joblib
from engine import record_audio, transcribe, speak
from actions import execute_command

# 1. Page Configuration
st.set_page_config(page_title="Siri Mini", layout="centered")

if 'task_history' not in st.session_state:
    st.session_state.task_history = []

# 2. Refined CSS for the UI, Chat Bubbles, and Tabs
st.markdown("""
<style>
    /* Deep dark background */
    .stApp { background-color: #050505 !important; }
    h1, h2, h3, p, div, span, .stMarkdown, .stText { color: #ffffff !important; }
    
    /* Center the custom titles */
    .header-container { text-align: center; margin-top: 20px; margin-bottom: 30px; }
    .main-title { font-size: 2.2rem; font-weight: 700; letter-spacing: 2px; margin-bottom: 0px; }
    .sub-title { font-size: 0.8rem; font-weight: 500; letter-spacing: 3px; color: #888888 !important; margin-top: 5px; }
    
    /* The Siri Glowing Orb */
    .ring-container { display: flex; justify-content: center; align-items: center; margin: 40px 0; }
    .outer-ring {
        width: 160px; height: 160px; border-radius: 50%;
        background-color: #111111; border: 2px solid #222222;
        box-shadow: 0 0 35px rgba(74, 144, 226, 0.5), 0 0 60px rgba(201, 75, 184, 0.3); 
        display: flex; justify-content: center; align-items: center;
    }
    .inner-dot {
        width: 60px; height: 60px; border-radius: 50%;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #c94bb8 100%);
        box-shadow: 0 0 20px rgba(201, 75, 184, 0.6);
    }

    /* Styled Pill Button (Voice) */
    .stButton > button {
        background-color: #2c2c2e !important; color: white !important;
        border-radius: 30px !important; border: 1px solid #444 !important;
        padding: 10px 20px !important; font-weight: 600 !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5) !important;
    }
    .stButton > button:hover {
        background-color: #3a3a3c !important; border: 1px solid #777 !important;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1) !important;
    }

    /* Expander */
    .streamlit-expander { background-color: #151515 !important; border: 1px solid #333 !important; border-radius: 10px; }
    
    /* Chat Bubble CSS */
    .chat-container { display: flex; flex-direction: column; gap: 8px; margin-bottom: 25px; }
    
    .user-bubble { 
        background-color: #121826; padding: 12px 18px; border-radius: 8px; 
        border-left: 4px solid #3b82f6; color: #e2e8f0; font-size: 0.95rem;
    }
    
    .intent-tag-container { display: flex; justify-content: flex-end; margin-top: -12px; margin-bottom: 2px; }
    .intent-tag { 
        background-color: #2d1b4e; color: #a78bfa; font-size: 0.7rem; 
        padding: 4px 12px; border-radius: 15px; border: 1px solid #4c1d95; font-weight: 600; letter-spacing: 1px;
    }
    
    .ai-bubble { 
        background-color: #061c13; padding: 12px 18px; border-radius: 8px; 
        border-left: 4px solid #10b981; color: #6ee7b7; font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. Load ML Models
@st.cache_resource
def load_ml_models():
    vec = joblib.load('vectorizer.pkl')
    classifier = joblib.load('intent_model.pkl')
    return vec, classifier

vectorizer, clf = load_ml_models()

# 4. Custom UI Layout (Orb and Header)
st.markdown("""
    <div class="header-container">
        <div class="main-title">SIRI MINI</div>
        <div class="sub-title">AI VOICE ASSISTANT</div>
    </div>
    <div class="ring-container">
        <div class="outer-ring">
            <div class="inner-dot"></div>
        </div>
    </div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ What can I do?"):
    st.write(f"**Available Tasks:** {', '.join(clf.classes_)}, set timer, search wiki, github, gmail, notepad, date/time, map")

# --- NEW: The Shared "Brain" Function ---
def process_user_command(user_text):
    """Handles intent prediction, execution, and UI history update."""
    st.write("Analyzing intent...")
    text_vec = vectorizer.transform([user_text])
    intent = clf.predict(text_vec)[0]
    
    action_response = execute_command(intent, user_text)
    speak(action_response)
    
    st.session_state.task_history.append({
        "Command": user_text, 
        "Action": intent,
        "Response": action_response
    })

# 5. --- NEW: The Dual Input Interface (Tabs) ---
tab1, tab2 = st.tabs(["🎤 Voice Command", "⌨️ Text Command"])

# TAB 1: Voice Input
with tab1:
    if st.button("🎙️ Start Recording", use_container_width=True):
        with st.status("Hardware Active: Listening...", expanded=True) as status:
            audio_file = record_audio(duration=4)
            if audio_file:
                st.write("Transcribing via Whisper...")
                user_text = transcribe(audio_file)
                st.info(f"You said: {user_text}")
                
                if user_text:
                    process_user_command(user_text)
                    status.update(label="Task Complete!", state="complete", expanded=False)
                else:
                    st.error("Audio captured, but Whisper could not understand the words.")
                    status.update(label="Failed", state="error", expanded=False)
            else:
                st.error("Failed to capture audio from the hardware microphone.")
                status.update(label="Hardware Error", state="error", expanded=False)

# TAB 2: Text Input
with tab2:
    # Use a form so the user can just hit "Enter" on their keyboard to submit
    with st.form(key="text_input_form", clear_on_submit=True):
        typed_text = st.text_input("Type your command below:", placeholder="e.g., What is the weather in Hubballi?")
        submit_button = st.form_submit_button("Send 💬", use_container_width=True)
        
        if submit_button and typed_text:
            with st.spinner("Processing your command..."):
                process_user_command(typed_text)
                st.rerun() # Refreshes the page instantly to show the new chat history

# 6. The Task History Display 
st.markdown("---")

if st.session_state.task_history:
    for item in reversed(st.session_state.task_history):
        display_intent = item['Action']
        command_lower = item['Command'].lower()
        
        if "timer" in command_lower: display_intent = "set_timer"
        elif "date" in command_lower: display_intent = "date_time"
        elif "who are you" in command_lower: display_intent = "personality"
        elif "what is" in command_lower or "who is" in command_lower: display_intent = "search_wiki"
        elif "github" in command_lower or "git hub" in command_lower: display_intent = "open_github"
        elif "gmail" in command_lower or "mail" in command_lower: display_intent = "open_gmail"
        elif "notepad" in command_lower or "note pad" in command_lower: display_intent = "open_notepad"
        elif "map" in command_lower or "navigate" in command_lower: display_intent = "open_maps"
        elif "joke" in command_lower: display_intent = "joke_fun"
            
        st.markdown(f"""
        <div class="chat-container">
            <div class="user-bubble">
                🗣️ <strong>You:</strong> {item['Command']}
            </div>
            <div class="intent-tag-container">
                <div class="intent-tag">⚡ {display_intent}</div>
            </div>
            <div class="ai-bubble">
                🤖 <strong>Siri:</strong> {item['Response']}
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No tasks completed yet. Use the Voice or Text tabs above to start!")