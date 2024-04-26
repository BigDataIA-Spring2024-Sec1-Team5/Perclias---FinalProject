import os
import streamlit as st
import boto3
from pinecone import Pinecone
import openai
import re
import json
import requests
from streamlit_lottie import st_lottie
import numpy as np
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores.pinecone import Pinecone as PineconeVectorStore
from dotenv import load_dotenv

load_dotenv(verbose=True,override=True)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_lottieFile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def extract_relevant_symptoms(text):
    print("Extracting relevant symptoms from the text...")
    relevant_symptoms = []
    symptom_pattern = r"Possible symptoms to consider:\s*([^.]+)"
    match = re.search(symptom_pattern, text, re.IGNORECASE)
    if match:
        symptoms = [symptom.strip() for symptom in match.group(1).split(",")]
        relevant_symptoms = symptoms
        print(f"Extracted {len(relevant_symptoms)} relevant symptoms.")
        return relevant_symptoms
    else:
        # Try a different pattern if the first one doesn't match
        symptom_pattern = r"Symptoms:\s*([^.]+)"
        match = re.search(symptom_pattern, text, re.IGNORECASE)
        if match:
            symptoms = [symptom.strip() for symptom in match.group(1).split(",")]
            relevant_symptoms = symptoms
            print(f"Extracted {len(relevant_symptoms)} relevant symptoms.")
            return relevant_symptoms
        else:
            # Try a different pattern for the provided text
            symptom_pattern = r"Possible symptoms to consider:\n([^.]+)"
            match = re.search(symptom_pattern, text, re.IGNORECASE)
            if match:
                symptoms = [symptom.strip() for symptom in match.group(1).split("\n")]
                relevant_symptoms = symptoms
                print(f"Extracted {len(relevant_symptoms)} relevant symptoms.")
                return relevant_symptoms
            else:
                print("No relevant symptoms found in the text.")
                return []

def generate_diagnosis(descriptive_texts):
     openai.api_key = os.getenv("OPENAI_API_KEY")
     combined_text = " ".join(descriptive_texts)
     response = openai.chat.completions.create(
          model="gpt-3.5-turbo-0125",
          messages=[
               {"role": "system", "content": "You are a helpful medical assistant."},
               {"role": "user", "content": f"Based on the symptoms '{combined_text}', what are the top 5 possible diseases, a small description, their symptoms, home remedies if any, medicines if any and ways to cure them?"}
          ],
          max_tokens=1024,
          n=1,
          stop=None,
          temperature=0.9,
     )
     return response.choices[0].message.content # type: ignore

def app():
    st.title("Medication Recommendation")

    lottie_login = load_lottieFile("Medication.json")
    st_lottie(lottie_login, height=300, key="login_animation")
    file_name = st.text_input("Enter Patient Name:", value="") + ".txt"

    if file_name:
        if st.button("Get Medication"): 
            print("Loading summary from S3...")
            s3 = boto3.client('s3',
                              aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                              aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
            bucket_name = os.getenv("S3_BUCKET_NAME")
            try:
                response = s3.get_object(Bucket=bucket_name, Key=file_name)
                summary = response['Body'].read().decode('utf-8')
                print("Summary loaded successfully.")
            except:
                st.error("Error loading summary from S3")
                return

            print("Connecting to Pinecone index...")
            pc = Pinecone(api_key=os.getenv('pinecone_api_key'))
            index_name = "perclias"
            index = pc.Index(name=index_name)
            print("Connected to Pinecone index.")

            # Extract symptoms from the summary
            print("Extracting symptoms from the summary...")
            symptoms = extract_relevant_symptoms(summary)
            print(f"Extracted {len(symptoms)} relevant symptoms: {symptoms}")
            processed_symptoms = [symptom.lower().strip() for symptom in symptoms]
            print(f"\nProcessed symptoms: {processed_symptoms}")

            # Vectorize the symptoms using LangChain
            print("Vectorizing symptoms using LangChain...")
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            symptom_vectors = embeddings.embed_documents(processed_symptoms)

            # Club all the symptom vectors together
            print("Clubbing symptom vectors together...")
            combined_symptom_vector = np.mean(symptom_vectors, axis=0).tolist()

            if symptoms:
                st.subheader("Recommended Medications, Remedies, and Diseases:")
                try:
                    query_result = index.query(
                        vector=combined_symptom_vector,
                        top_k=7,
                        include_metadata=True
                    )

                    if query_result["matches"]:
                        for match in query_result["matches"]:
                            id = match['id']
                            score = match['score']
                    else:
                        st.write("No matches found in Pinecone.")
                    
                    descriptive_texts = [match['id'] for match in query_result['matches']]

                    if descriptive_texts:
                        diagnosis_report = generate_diagnosis(descriptive_texts)
                        st.write(diagnosis_report)
                    else:
                        st.write("No relevant data found in Pinecone.")

                except Exception as e:
                    st.error(f"Error processing symptoms: {e}")
            else:
                st.subheader("Possible Diseases Based on OpenAI Analysis:")
                openai.api_key = os.getenv("OPENAI_API_KEY")
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful medical assistant."},
                       {"role": "user", "content": f"Based on the provided summary, what are the top 5 possible diseases, a small description, their symptoms, home remedies if any, medicines if any and ways to cure them?"}
                    ],
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.7,
                )
                disease_info = response.choices[0].message.content # type: ignore
                st.write(disease_info)

if __name__ == "__main__":
    app()