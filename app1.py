import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
import base64
import os
import re
import json
import requests
from streamlit_lottie import st_lottie
from dotenv import load_dotenv
import boto3
import datetime

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

#initialize openai client
def setup_openai_client(api_key):
    return openai.OpenAI(api_key=api_key)
client = setup_openai_client(api_key=openai_api_key)


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_lottieFile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
    
#function to transcribe audio to text
def transcribe_audio(client, audio_path):
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1",file=audio_file) 
        return transcript.text
    
# taking resposne from Openai
def fetch_ai_response(client, input_text):
    messages = [{"role": "user","content": "You are a helpful healthcare assistant named Perclias AI. You will only respond in English and provide information relevant to the user's healthcare concerns."},
    {"role": "user", "content": input_text}
    ]
    response = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=messages)
    return response.choices[0].message.content

#convert text to audio
def text_to_audio(client, text, audio_path):
    response=client.audio.speech.create(model="tts-1",voice="nova",input=text)
    response.stream_to_file(audio_path)

# Extract Symptoms from the conversation
def extract_symptoms(text):
    symptom_pattern = r"(?:possible symptoms include|symptoms may include|symptoms are|symptoms may be|symptoms can be|symptoms could be):\s*([^.]+)"
    match = re.search(symptom_pattern, text, re.IGNORECASE)
    if match:
        symptoms = [symptom.strip() for symptom in match.group(1).split(",")]
        return symptoms
    else:
        return []

# Generate summary and diagnosis
def generate_summary_and_diagnosis(conversation_text):
    messages = [
        {"role": "system", "content": "You are a healthcare assistant. Start with reason for visit in first line than in seperate lines mention(patient name, medical history, background, previous medications, test results, family history, allergies, current medications.) and than Summarize the conversation in paragraph and than provide a bullet list of possible symptoms using only the word Possible Symptoms."},
        {"role": "user", "content": conversation_text}
    ]
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.chat.completions.create(model="gpt-3.5-turbo-1106", messages=messages)
    return response.choices[0].message.content # type: ignore

#text cards function
def create_text_card(text, title="Response"):
    logo_path = "logo.jpg"
    card_html = f"""
    <div style="display: flex; align-items: center; background-color: #f8f8f8; border-radius: 10px; padding: 20px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);">
        <img src="data:image/png;base64,{get_base64_image(logo_path)}" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; margin-right: 20px;">
        <div>
            <h4 style="margin-top: 0; color: #333;">{title}</h4>
            <p style="color: #666; white-space: pre-wrap;">{text}</p>
        </div>
    </div>
    <br>
    """
    st.markdown(card_html, unsafe_allow_html=True)
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_image

def auto_play_audio(audio_file):
    with open(audio_file, "rb") as audio_file:
        audio_bytes = audio_file.read()
        base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
        audio_html = f'<audio src="data:audio/mp3;base64,{base64_audio}" controls autoplay></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)


def save_to_s3(summary_and_diagnosis, patient_name, s3_client, bucket_name):
    file_name = f"{patient_name}.txt"
    s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=summary_and_diagnosis)
    return file_name


def main():
    
    st.sidebar.title("")
    

    st.title("🏥:violet[Perclias AI]")
    st.header("Your Healthcare🩺 Companion")
    lottie_login = load_lottieFile("login.json")
    st_lottie(lottie_login, height=100, key="login_animation")

    st.subheader("Hi there👋! Click on the voice recorder to interact with me. ")

    #check if api key is there
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = setup_openai_client(api_key=openai_api_key)
    
    audio_source = st.radio("How would you like to interact with me?", ["Record Audio", "Upload Audio"])
    audio_file = None

    #recorded_audio = audio_recorder()
    if audio_source == "Record Audio":
        st.write("🎤 Click on the voice recorder to record your audio.")
        recorded_audio = audio_recorder(key="recorder")
        if recorded_audio:
            audio_file = "audio.mp3"
            with open(audio_file,"wb") as f:
                f.write(recorded_audio)

        if recorded_audio:
            audio_file = "audio.mp3"
            with open(audio_file, "wb") as f:
                f.write(recorded_audio)
    
    else:
        st.write("📁 Upload an audio file to interact with me.")
        uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])
        if uploaded_file is not None:
            audio_file = "audio.mp3"
            with open(audio_file, "wb") as f:
                f.write(uploaded_file.getbuffer())
    
    audio_played = False

    if audio_file:
        client = setup_openai_client(os.getenv("OPENAI_API_KEY"))
        if client:    
            transcribed_text=transcribe_audio(client, audio_file)
            create_text_card(transcribed_text,"Audio Transcription")
            summary_and_diagnosis = generate_summary_and_diagnosis(transcribed_text)
            create_text_card(summary_and_diagnosis, "Summary and Diagnosis")
            if not audio_played:
                response_audio_file = "audio_reponse.mp3"
                text_to_audio(client, summary_and_diagnosis, response_audio_file)
                auto_play_audio(response_audio_file)
                audio_played = True 

            st.write("---")
            symptoms = extract_symptoms(summary_and_diagnosis)
            if symptoms:
                st.subheader("<span style='color:black;'>Possible Symptoms:</span>")
                for symptom in symptoms:
                    st.write(f"<span style='color:black;'>- {symptom}</span>", unsafe_allow_html=True)
            else:
                st.write("response.")

            #ai_response = fetch_ai_response(client,transcribed_text)
            response_audio_file = "audio_reponse.mp3"
            text_to_audio(client,summary_and_diagnosis,response_audio_file)
            #auto_play_audio(response_audio_file)
            #st.write(summary_and_diagnosis,"AI Response")
            edited_response = st.text_area("Edit Perclias Response", summary_and_diagnosis, height=200)
            patient_name = st.text_input("Enter Patient Name:")
            if st.button("Save Edited Response"):
                if not patient_name:
                    st.warning("Please enter the patient's name.")
                else:
                    summary_and_diagnosis = edited_response
                    create_text_card(summary_and_diagnosis, "Summary and Diagnosis")
            
            # Save the edited response to an S3 bucket
                s3 = boto3.client('s3',
                                  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                                  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
                bucket_name = os.getenv("S3_BUCKET_NAME")
                #file_name = save_to_s3(summary_and_diagnosis, s3, bucket_name)
                #file_name = "edited_response.txt"
                file_name = f"{patient_name}.txt" 
                s3.put_object(Bucket=bucket_name, Key=file_name, Body=summary_and_diagnosis)
                st.success(f"Edited response saved to S3 bucket: {bucket_name}/{file_name}")
if __name__ == "__main__":
    main()