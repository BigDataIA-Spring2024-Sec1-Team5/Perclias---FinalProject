import streamlit as st
import snowflake.connector
import os
import json
import requests
from dotenv import load_dotenv
from streamlit_lottie import st_lottie
from datetime import datetime, date
#from datetime import datetime, timedelta


# Load environment variables
load_dotenv()

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_lottieFile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def get_snowflake_connection():
    ctx = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )
    cursor = ctx.cursor()
    return cursor

def create_patient_table(cursor):
    cursor.execute(f"USE DATABASE {os.getenv('SNOWFLAKE_DATABASE')}")
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {os.getenv("SNOWFLAKE_TABLE")} (
            patient_id NUMBER AUTOINCREMENT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            date_of_birth DATE,
            age INTEGER,
            gender VARCHAR(10),
            insurance_provider VARCHAR(100),
            medical_history TEXT,
            medications TEXT
        )
    """)

def check_patient_exists(cursor, first_name, last_name, date_of_birth):
    cursor.execute(f"""
        SELECT COUNT(*) 
        FROM {os.getenv("SNOWFLAKE_TABLE")}
        WHERE first_name = %s
        AND last_name = %s
        AND date_of_birth = %s
    """, (first_name, last_name, date_of_birth))
    return cursor.fetchone()[0] > 0

def search_patient(cursor, search_text):
    cursor.execute(f"""
        SELECT * FROM {os.getenv("SNOWFLAKE_TABLE")}
        WHERE first_name LIKE '%{search_text}%'
           OR last_name LIKE '%{search_text}%'
    """)
    return cursor.fetchall()

def display_patient_details(patient_data):
    if patient_data:
        st.subheader("Patient Details")
        for row in patient_data:
            st.write(f"Patient ID: {row[0]}")
            st.write(f"First Name: {row[1]}")
            st.write(f"Last Name: {row[2]}")
            st.write(f"Date of Birth: {row[3]}")
            st.write(f"Age: {row[4]}")
            st.write(f"Gender: {row[5]}")
            st.write(f"Insurance Provider: {row[6]}")
            st.write(f"Medical History: {row[7]}")
            st.write(f"Medications: {row[8]}")
            st.write("---")
    else:
        st.write("No patient found.")

def edit_patient_details(cursor, patient_id, first_name, last_name, date_of_birth, age, gender, insurance_provider, medical_history, medications):
    cursor.execute(f"""
        UPDATE {os.getenv("SNOWFLAKE_TABLE")}
        SET first_name = %s,
            last_name = %s,
            date_of_birth = %s,
            age = %s,
            gender = %s,
            insurance_provider = %s,
            medical_history = %s,
            medications = %s
        WHERE patient_id = %s
    """, (first_name, last_name, date_of_birth, age, gender, insurance_provider, medical_history, medications, patient_id))
    st.success("Patient details updated successfully!")

def app():
    st.title("Patient Management👨‍⚕️")
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
    lottie_head_logo = load_lottieFile("doc.json")
    st_lottie(lottie_head_logo, height=200, key="head_logo")

    # Search functionality
    with st.expander("Search Patient"):
        search_text = st.text_input("Enter patient name")
        if st.button("Search"):
            cursor = get_snowflake_connection()
            patient_data = search_patient(cursor, search_text)
            display_patient_details(patient_data)

    # Patient details form
    with st.expander("Enter Patient Details"):
        # Create a form to collect patient details
        with st.form(key="patient_form"):
            col1, col2 = st.columns(2)

            with col1:
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                min_date = date(1900, 1, 1)
                max_date = date.today()
                date_of_birth = st.date_input("Date of Birth", min_value=min_date, max_value=max_date)
                age = st.slider("Age", min_value=0, max_value=120, value=30, step=1)

            with col2:
                gender_col, insurance_col = st.columns(2)
                with gender_col:
                    gender = st.radio("Gender", options=["Male", "Female", "Other"])
                with insurance_col:
                    insurance_provider = st.text_input("Insurance Provider")

            medical_history = st.text_area("Medical History")
            medications = st.text_area("Medications Currently Taking")

            submit_button = st.form_submit_button(label="Save Patient Details")

        if submit_button:
            # Save the patient details to the Snowflake database
            cursor = get_snowflake_connection()
            create_patient_table(cursor)

            if check_patient_exists(cursor, first_name, last_name, date_of_birth):
                st.error("Patient already exists.")
            else:
                cursor.execute(f"""
                    INSERT INTO {os.getenv("SNOWFLAKE_TABLE")} (
                        first_name, last_name, date_of_birth, age, gender, insurance_provider, medical_history, medications
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    first_name, last_name, date_of_birth, age, gender, insurance_provider, medical_history, medications
                ))
                st.success("Patient details saved successfully!")

    # Edit patient details
    with st.expander("Edit Patient Details"):
        cursor = get_snowflake_connection()
        patient_data = search_patient(cursor, "")
        patient_id = st.selectbox("Select Patient", [row[0] for row in patient_data])

        if patient_id:
            for row in patient_data:
                if row[0] == patient_id:
                    with st.form(key="edit_patient_form"):
                        col1, col2 = st.columns(2)

                        with col1:
                            first_name = st.text_input("First Name", value=row[1])
                            last_name = st.text_input("Last Name", value=row[2])
                            date_of_birth = st.date_input("Date of Birth", value=row[3])
                            age = st.slider("Age", min_value=0, max_value=120, value=row[4], step=1)

                        with col2:
                            gender_col, insurance_col = st.columns(2)
                            with gender_col:
                                gender = st.radio("Gender", options=["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(row[5]))
                            with insurance_col:
                                insurance_provider = st.text_input("Insurance Provider", value=row[6])

                        medical_history = st.text_area("Medical History", value=row[7])
                        medications = st.text_area("Medications Currently Taking", value=row[8])

                        submit_button = st.form_submit_button(label="Update Patient Details")

                        if submit_button:
                            edit_patient_details(cursor, patient_id, first_name, last_name, date_of_birth, age, gender, insurance_provider, medical_history, medications)
    
if __name__ == "__main__":
    app()