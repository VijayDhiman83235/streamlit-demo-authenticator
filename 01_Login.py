import streamlit as st
import warnings
import plotly.graph_objects as go
from PIL import Image
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import warnings
from ONDC import ONDC_dash

warnings.filterwarnings('ignore')

icon_ = Image.open("ICON/paytm_icon-icons.com_62778.ico")

st.set_page_config(page_title="Paytm Reports", 
                   page_icon=icon_,
                   layout="wide")


image = Image.open("ICON/Paytm_Logo.png")
image = image.resize((300, 100))
st.sidebar.image(image,caption=" ")


names = ["Vijay Kumar","Suresh Fatehpuria"]
usernames = ["vkumar","sfatehpuria"]

file_path = Path(__file__).parent / "hashed_pw.pkl"

with file_path.open("rb") as file:
    hashed_password = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_password,
                                    "dashboard_password", "abcdef", cookie_expiry_days=1)


if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
    st.session_state['username'] = None
def page2():
    st.write("This is page 2")

def page3():
    st.write("This is page 3")


def create_pages_dict(page_numbers):
    all_pages = {
        1: ("ONDC", ONDC_dash),
        2: ("Test Page 2", page2),
        3: ("Test Page 3", page3),      
    }

    pages_dict = {}
    for num in page_numbers:
        if num in all_pages:
            page_name, page_function = all_pages[num]
            pages_dict[page_name] = page_function

    return pages_dict

pages = create_pages_dict([1, 2])

def main():

    if st.session_state.get('authentication_status') != True:
        name, authentication_status, username = authenticator.login("Login", "main")

        st.session_state['authentication_status'] = authentication_status
        st.session_state['username'] = username
        
        if authentication_status == False:
            st.error("Username/password is incorrect")
        elif authentication_status == None:
            st.warning("Please enter your username and password")
        return  

    st.sidebar.title(f"Welcome {st.session_state['username']}")
    page = st.sidebar.selectbox("Select Report", list(pages.keys()))
    pages[page]()

authenticator.logout("Logout", "sidebar")


main()
