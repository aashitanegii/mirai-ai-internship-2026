import streamlit as st
import speech_recognition as sr

st.set_page_config(
    page_title="Speech Recognition",
    page_icon="🎤",
    layout="centered"
)

st.title("🎤 Speech Recognition App")
st.write("Convert your speech into text using Google's Speech Recognition API.")

recognizer = sr.Recognizer()

if st.button("🎙️ Start Listening"):

    try:
        with sr.Microphone() as source:
            st.info("Listening... Please speak.")

            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

            st.success("Processing speech...")

            text = recognizer.recognize_google(audio)

            st.subheader("📝 Recognized Text")
            st.write(text)

    except sr.WaitTimeoutError:
        st.error("No speech detected. Please try again.")

    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand the audio.")

    except sr.RequestError:
        st.error("Could not connect to the Speech Recognition service.")

    except Exception as e:
        st.error(f"Error: {e}")