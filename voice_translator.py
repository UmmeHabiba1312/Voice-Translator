import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play

# Function to record voice
def record_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Increased duration
        st.info("Listening for your voice...")
        audio = recognizer.listen(source)
        print("Audio captured")

    try:
        print("Recognizing speech...")
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
    play(audio)
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

# Option for uploading an audio file (for when microphone isn't available)
audio_file = st.file_uploader("Or Upload an Audio File", type=["wav", "mp3"])

if audio_file is not None:
    # Save the uploaded file
    with open("uploaded_audio.wav", "wb") as f:
        f.write(audio_file.getbuffer())

    # Process the uploaded audio file
    recognizer = sr.Recognizer()
    with sr.AudioFile("uploaded_audio.wav") as source:
        audio = recognizer.record(source)
    
    try:
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        st.success(f"📝 You said: {text}")
        # Translate and convert text to speech
        if text:
            translated_text = translate_text(text, language_options[target_lang])
            text_to_speech(translated_text, language_options[target_lang])
    except sr.UnknownValueError:
        st.error("Could not understand audio")
    except sr.RequestError:
        st.error("API unavailable")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Record and process voice (when microphone is available)
elif st.button("🎙️ Record Voice"):
    text = record_voice()
    if text:
        translated_text = translate_text(text, language_options[target_lang])
        text_to_speech(translated_text, language_options[target_lang])
