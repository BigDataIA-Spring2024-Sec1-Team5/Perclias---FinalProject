import streamlit as st
from streamlit_option_menu import option_menu
import app1, about, app2, app3, login, patient

def main():
    st.set_page_config(
        page_title="🏥Perclias AI🩺",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login.app()
    else:
        with st.sidebar:
            app = option_menu(
                menu_title='',
                options=['🏥 Patient Care', '🤖 Perclias AI', '⚕️ Diagnosis', '💊 Medication', '🔍 About', '🚪 Logout'],
                #icons=['person-circle', 'robot', 'trophy-fill', 'capsule', 'info-circle-fill', 'box-arrow-right'],
                icons=['🏥','🤖','⚕️','💊','🔍','🚪'],
                menu_icon='chat-text-fill',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        if app == "🏥 Patient Care":
            patient.app()
        elif app == "🤖 Perclias AI":
            app1.main()
        elif app == "⚕️ Diagnosis":
            app2.app()
        elif app == "💊 Medication":
            app3.app()
        elif app == "🔍 About":
            about.app()
        elif app == "🚪 Logout":
            st.session_state.logged_in = False
            st.experimental_rerun()

if __name__ == "__main__":
     main()