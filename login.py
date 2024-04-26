import streamlit as st
import firebase_admin
import json
import requests
from streamlit_lottie import st_lottie
from firebase_admin import credentials
from firebase_admin import auth

# cred = credentials.Certificate('perclias-ai-0723efbf20f5.json')
# firebase_admin.initialize_app(cred)
# Check if Firebase app is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate('perclias-ai-0723efbf20f5.json')
    firebase_admin.initialize_app(cred)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_lottieFile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def app():
    #st.title("Access :violet[Perclias AI] Platform🩺")
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
    st.markdown(
        f'<h1 style="text-align:center;">Access <span style="color:violet;">Perclias AI</span> Platform🩺</h1>',
        unsafe_allow_html=True
    )
    # Load Lottie animation
    lottie_login = load_lottieFile("login.json")
    st_lottie(lottie_login, height=200, key="login_animation")
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail =''
    if 'signout' not in st.session_state:
        st.session_state.signout = False
    if 'signedout' not in st.session_state:
        st.session_state.signedout = False

    def f():
        try:
            user = auth.get_user_by_email(email)
            st.write('Login Successful')
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.signedout = True
            st.session_state.signout = True
            st.session_state.logged_in = True  # Set logged_in to True
        except:
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''
        st.session_state.logged_in = False  # Set logged_in to False
    
    if not st.session_state['signedout']:
        choice = st.selectbox('Login/Signup',['Login','Sign Up'])

        if choice =='Login':
            # Load Lottie animation
            # lottie_login = load_lottieFile("login.json")
            # st_lottie(lottie_login, height=300, key="login_animation")

            email = st.text_input('Email Address:')
            password = st.text_input('Password:', type='password')
            st.button('Login', on_click=f, key='login_button')
        else:
            email = st.text_input('Email Address:')
            password = st.text_input('Password:', type='password')
            username = st.text_input('UserName:')
            if st.button('Create my account', key='signup_button'):
                user = auth.create_user(email = email, password = password, uid = username)
                st.success('Account created successfully!!')
                st.markdown('Please Login using your Email Address and Password')
                st.balloons()

    if st.session_state.signout:
        st.markdown('Name: '+st.session_state.username)
        st.markdown('Email id: '+st.session_state.useremail)
        st.button('Sign out', on_click = t, key='signout_button')