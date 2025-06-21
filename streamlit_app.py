import streamlit as st
import pandas as pd
from datetime import datetime
import os
import speech_recognition as sr

# CSV file to save stories
CSV_FILE = "anonymous_stories.csv"

# Function to save story to CSV
def save_story(text):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "story": text.strip()
    }
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    else:
        df = pd.DataFrame([entry])
    df.to_csv(CSV_FILE, index=False)

# Function to transcribe audio
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data, language="hi-IN")

# ==== Streamlit UI ====
st.set_page_config(page_title="I Am Shakti", layout="centered")

st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color:#b30059;'>🩷 I Am Shakti</h1>
        <h4>Tell Your Story Without Fear | अपनी पहचान गुप्त रखें</h4>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Audio input
st.subheader("🎤 बोलकर लिखें (Speak in Hindi)")
uploaded_audio = st.file_uploader("Upload your Hindi voice message (WAV only)", type=["wav"])

if uploaded_audio:
    st.info("Transcribing your audio...")
    try:
        text = transcribe_audio(uploaded_audio)
        st.text_area("Transcribed Text", text, height=150)
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")

# Text story input
st.subheader("✍️ अपनी कहानी खुद लिखें")
story = st.text_area("यहाँ लिखें (Write your story here)", height=300)
if st.button("📤 Submit / सबमिट करें"):
    if story.strip():
        save_story(story)
        st.success("✅ आपकी कहानी सुरक्षित रूप से सेव हो गई है। धन्यवाद!")
    else:
        st.error("⚠️ कृपया खाली कहानी सबमिट न करें।")

st.markdown("---")
st.caption("🔐 आपकी कहानी सिर्फ आपकी है — नाम, पता या कोई जानकारी संग्रह नहीं की जाती।")
st.caption("🌸 आप अकेली नहीं हैं — हम सब आपकी आवाज़ हैं।")

