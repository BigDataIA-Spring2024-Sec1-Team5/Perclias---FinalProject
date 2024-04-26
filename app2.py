import streamlit as st
from pathlib import Path
import google.generativeai as genai
import os
import textwrap
import json
import requests
from streamlit_lottie import st_lottie
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from .env
load_dotenv()

# Retrieve the API key from environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_lottieFile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
    
# Function to load OpenAI model and get responses
def get_gemini_response(image):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    prompt = """Being a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.
Give output in the below format detailed analysis, finding reports, recommendation, treatment suggestions
Responsibilities:
1. Detailed Analysis: Carefully examine the provided medical image and identify any abnormalities, potential diseases, or health concerns that may be present.
2. Finding Reports: Based on your analysis, provide a detailed report outlining your findings, including any relevant medical terminology and explanations.
3. Recommendation and Next Steps: Suggest any further tests, examinations, or consultations that may be necessary to confirm or rule out your findings.
4. Treatment Suggestions: If applicable, provide recommendations for appropriate treatment options or management strategies for the identified condition.

Important Notes:
1. Scope of Response: Your response should be comprehensive and address all the responsibilities mentioned above, providing a thorough and professional assessment of the medical image.
2. Clarity of Image: Assume that the provided medical image is of high quality and clarity, allowing for a detailed analysis.
3. Disclaimer: Please note that your recommendations are based on your expertise as a medical practitioner, but the final diagnosis and treatment decisions should be made by the patient's primary healthcare provider."""

    response = model.generate_content([prompt, image])
    return response.text

def app():
    st.header("Medical Image Analysis")
    lottie_login = load_lottieFile("Medical_Image.json")
    st_lottie(lottie_login, height=300, key="login_animation")
    uploaded_file = st.file_uploader("Upload a medical image...", type=["jpg", "jpeg", "png"])
    image = ""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

    submit = st.button("Analyze Image")

    if submit:
        response = get_gemini_response(image)
        st.subheader("Medical Image Analysis")
        st.write(response)