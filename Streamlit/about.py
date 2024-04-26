import streamlit as st
import json
import requests
from streamlit_lottie import st_lottie

def app():
    # Set page title and layout
    #st.set_page_config(page_title="Perclias - About", layout="wide")
    st.markdown("""
                <style>
                input[type=text], input[type=password] {
                background-color: #e6f2ff;
                color: #003366;
                border: 3px solid #99ccff;
                border-radius: 4px;
                padding: 8px 12px;
                }
                </style>
                """, unsafe_allow_html=True)   
    # Title and introduction
    st.title("About🏥:violet[Perclias AI]")
    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    def load_lottieFile(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
        st.markdown("Perclias is a conversational AI assistant designed to assist patients and healthcare professionals in managing clinical information and providing personalized healthcare solutions. The project leverages Large Language Models and vector databases to capture and analyze patient-doctor conversations, generate summaries, and provide tailored recommendations based on identified symptoms and medical history.")
    lottie_login = load_lottieFile("About_Us.json")
    st_lottie(lottie_login, height=300, key="login_animation")    
    # Project Scope
    with st.container():
        st.header("Project Overview")
        with st.expander("Scope:"):
            st.markdown("""
            Perclias is a conversational AI assistant designed to assist patients and healthcare professionals in managing clinical information and providing personalized healthcare solutions. The project will leverage Large Language Models and vector databases to capture and analyze patient-doctor conversations, generate summaries, and provide tailored recommendations based on the identified symptoms and medical history.
            
            The project will involve the following key components:
            - **Voice Recording and Transcription:** Perclias will record and transcribe patient-doctor conversations using speech recognition technology.
            - **Conversation Summarization:** The transcribed conversations will be processed using a Large Language Model to generate concise summaries, highlighting key points and medical information.
            - **Symptom Identification and Analysis:** The summaries will be analyzed to identify relevant symptoms, medical conditions, and potential diagnoses.
            - **Recommendation Generation:** Based on the identified symptoms and medical history, Perclias will provide personalized recommendations, treatment options, and self-care advice.
            """)
    
    # Problem Statement
    with st.container():
        st.header("Problem Statement")
        with st.expander("Current Challenges and Opportunities:"):
            st.markdown("""
            **Current Challenges:**
            - *Inefficient Information Management:* Manual capture and organization of patient-doctor conversations can be time-consuming and prone to errors, leading to inefficiencies in healthcare delivery.
            - *Limited Personalization:* Providing personalized healthcare recommendations based on individual patient symptoms and medical history is challenging, particularly in high-volume healthcare settings where time constraints are prevalent.
            - *Communication Barriers:* Language barriers, medical jargon, and limited consultation time often impede effective communication between patients and healthcare professionals, hindering the quality of care provided.
            
            **Opportunities:**
            - *Enhanced Patient Care:* By streamlining the capture and analysis of patient-doctor conversations, Perclias can assist healthcare professionals in providing more personalized and accurate care, ultimately leading to better patient outcomes.
            - *Increased Efficiency:* Automating the process of summarizing conversations and generating recommendations can save valuable time for healthcare professionals, allowing them to allocate their resources more effectively and focus on critical tasks.
            - *Improved Accessibility:* Perclias can empower patients by providing clear and understandable summaries of their medical information, facilitating better self-care and informed decision-making. Additionally, it can help overcome communication barriers by providing multilingual support and simplifying medical terminology.
            """)
    st.balloons()

if __name__ == "__main__":
    app()