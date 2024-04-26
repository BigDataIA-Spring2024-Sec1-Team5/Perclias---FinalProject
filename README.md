# FinalProject

## Project Resources
Youtube Video URL: 
App link (hosted on Google Cloud):

## Live application Links
[![codelabs](https://img.shields.io/badge/codelabs-4285F4?style=for-the-badge&logo=codelabs&logoColor=white)]( https://codelabs-preview.appspot.com/?file_id=1pi7QseL9IrVMDiInLdGWVaC9McmrILCVLP_ml_icGlI#0)
[![workflow_architecture](https://img.shields.io/badge/workflow_architecture-FC6600?style=for-the-badge&logo=jupyter&logoColor=white)](https://colab.research.google.com/drive/15hzHqTEWEA3mODdOzBBs7hKNeoz7Bj7d#scrollTo=yO3GCFVqjeoF)
[![knowledge_summaries](https://img.shields.io/badge/knowledge_summaries-FC6600?style=for-the-badge&logo=jupyter&logoColor=white)](https://colab.research.google.com/drive/1z_bdJxOZ216nw997gTckQT6ZLWcJr4jP?usp=sharing)
[![Generate_Q&A](https://img.shields.io/badge/Generate_Q&A-FC6600?style=for-the-badge&logo=jupyter&logoColor=white)](https://colab.research.google.com/drive/1fSoI3f0jRflBNtc3EdGbU76-oyPbj3-A?usp=sharing)
[![Similarity_Search](https://img.shields.io/badge/Similarity_Search-FC6600?style=for-the-badge&logo=jupyter&logoColor=white)](https://colab.research.google.com/drive/1fSoI3f0jRflBNtc3EdGbU76-oyPbj3-A?usp=sharing)

## Technologies Used
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-3776AB?style=flat)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat&logo=selenium&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-007FFF?style=flat&logo=pinecone&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white)
![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=flat&logo=snowflake&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=flat&logo=firebase&logoColor=black)
![Langchain](https://img.shields.io/badge/Langchain-3776AB?style=flat&logo=langchain&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=flat&logo=apacheairflow&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-00A0E9?style=flat&logo=gemini&logoColor=white)
![AWS_S3](https://img.shields.io/badge/AWS_S3-569A31?style=flat&logo=amazons3&logoColor=white)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com/)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-109989?style=flat&logo=pydantic&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat&logo=pytest&logoColor=white)








## Overview

Perclias is basically AI for doctors! Leveraging conversational AI to assist patients and healthcare professionals can greatly enhance the efficiency and effectiveness of healthcare delivery. By analyzing patient-doctor conversations and utilizing data-driven approaches, Perclias can provide personalized healthcare solutions, diagnosis, and treatment recommendations tailored to individual needs. This could significantly improve patient outcomes and streamline the healthcare process.

## Problem statement
● Inefficient Information Management: Manual capture and organization of patient-doctor conversations can be time-consuming and prone to errors, leading to inefficiencies in healthcare delivery.

● Limited Personalization: Providing personalized healthcare recommendations based on individual patient symptoms and medical history is challenging, particularly in high-volume healthcare settings where time constraints are prevalent.

● Communication Barriers: Effective communication between patients and healthcare professionals is essential for accurate diagnosis and treatment. However, language barriers, medical jargon, and limited consultation time often impede this process, hindering the quality of care provided.

## Technology Stack

1. Streamlit
2. WhisperAI
3. GCP 
4. OpenAI
5. S3
6. Gemini Vision Pro
7. Beautiful Soup + Selenium 
8. Snowflake
9. Apache Airflow
10. Pinecone
11. AWS
12. Langchain
13. Firebase
    
## Architecture Workflow
![Workflow](https://github.com/BigDataIA-Spring2024-Sec1-Team5/FinalProject/blob/main/Images/Final_Architecture.jpg)

## Project Structure

```
📦 FinalProject
├─ ReadMe
├─ Documentation
├─ ETL
│  ├─ main.py
│  ├─ requirements.txt
|  ├─ scraping.py
|  ├─ snowflake_load.py
│  └─ validation.py
├─ Images
│  ├─ About_Us_UI.png
│  ├─ Final_Architecture.jpg
│  ├─ Login_Page_UI.png
|  ├─ Logout_UI.png
|  ├─ Medical_Image_Analysis_UI.png
|  ├─ Medication_Recommendation_UI.png
|  ├─ Part-1.png
|  ├─ Part-2.png
|  ├─ Patient_Management_1_UI.png
|  ├─ Patient_Management_UI.png
│  └─ Perclias_AI_UI.png
|  
|
├─ Snowflake
|   ├─ Patient_data.sql
|
├─ Streamlit
|   |
|   ├─ About_Us.json
|   ├─ Dockerfile
|   ├─Medication.json
|   ├─about.py
|   ├─app1.py
|   ├─app2.py
|   ├─app3.py
|   ├─ doc.json
|   ├─docker-compose.yml
|   ├─head_logo.json
|   ├─login.json
|   ├─login.py
|   ├─logo.jpg
|   ├─logo.json
|   ├─main.py
|   ├─patient.py
|   ├─requirements.txt
|   └─ Medical_Image.json
| 
├─ Validations
    ├─pytest.py
    ├─validation.py
```
## Flow Chart
```mermaid
graph TD
    A[Voice Recording and Transcription] -->|Transcribed Conversation| B[Conversation Summarization]
    B --> |Summary| C[Symptom Identification and Analysis]
    C --> |Further Diagnosis Needed| D[Image Analysis ]
    C --> |Diagnosis and History| E[Knowledge Base Integration]
    E --> |Knowledge Base| F[Recommendation Generation]
    F --> |Recommendations| G[User Interface]
    G --> |Store Data| H[Data Storage and Management]
    H -->  I[Continuous Improvement]
    I --> E
```

## Team Information and Contribution 

Name | Contribution %| Contributions |
--- |--- | --- |
Aditya Kanala | 33.33% |OpenAI, Pinecone & Deployment|
Shikhar Patel | 33.33% | Streamlit, LLMs Integration & Snowflake|
Shubh Patel | 33.33% | Scraping, Data Validation, Airflow & Snowflake|
