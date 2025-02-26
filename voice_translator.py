import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from pydub import AudioSegment
from io import BytesIO

# Function to record voice
def record_voice(file_path=None):
    recognizer = sr.Recognizer()
    
    if file_path:
        # Process uploaded file
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
    else:
        # Use microphone if no file is provided
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            st.info("Listening for your voice...")
            audio = recognizer.listen(source)
    
    try:
        st.info("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        st.success(f"📝 You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Could not understand audio")
    except sr.RequestError:
        st.error("API unavailable")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    return None

# Function to translate text
def translate_text(text, target_language):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language).text
    st.success(f"🌍 Translated: {translated_text}")
    return translated_text

# Function to convert text to speech
def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("output.mp3")
    audio = AudioSegment.from_mp3("output.mp3")
    audio.play()
    os.remove("output.mp3")

# Streamlit UI
st.title("🗣️ Voice Translator App")

# Select target language
language_options = {
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese": "zh-cn",
    "Urdu": "ur"
}
target_lang = st.selectbox("Select language:", list(language_options.keys()))

# Upload audio file
uploaded_file = st.file_uploader("Upload an audio file (WAV, MP3, etc.)", type=["wav", "mp3", "flac"])

if uploaded_file:
    st.write(f"File uploaded: {uploaded_file.name}")
    # Convert uploaded file to WAV format (if it's not already)
    audio_data = uploaded_file.read()
    audio = AudioSegment.from_file(BytesIO(audio_data))
    audio.export("uploaded_audio.wav", format="wav")

    # Process uploaded file
    text = record_voice(file_path="uploaded_audio.wav")
    
    if text:
        # Translate and convert to speech
        translated_text = translate_text(text, language_options[target_lang])
        text_to_speech(translated_text, language_options[target_lang])
else:
    st.info("Upload a file or speak to record voice.")
