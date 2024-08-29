import streamlit as st
import os
import math
import random
import smtplib

st.set_page_config(page_title="OTP ",layout="centered",initial_sidebar_state="auto",menu_items=None)

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Function to initialize or get the session state
def get_session():
    if 'session' not in st.session_state:
        st.session_state.session = SessionState(otp="")
    return st.session_state.session

st.header("OTP Verification System")

def hideAll():
    hide = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """   
    st.markdown(hide, unsafe_allow_html=True)

hideAll() 
# Generate OTP
digits = "0123456789"
session_state = get_session()
if not session_state.otp:  # Generate a new OTP only if it doesn't exist in the session state
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    session_state.otp = OTP

# Prepare email message
otp_message = session_state.otp + " is your OTP"
sender_mail = 'wrieddude@gmail.com'
receivers_mail = st.text_input("Enter the mail address")

if st.button("Send OTP"):
    if receivers_mail:
        message = otp_message
        try:
            # Connect to Gmail's SMTP server
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()

            # Replace 'your_gmail_account@gmail.com' and 'your_app_password' with your actual Gmail account and app password
            s.login('wrieddude@gmail.com', 'password')
            s.sendmail(sender_mail, receivers_mail, message)
            s.quit()
            st.write("Successfully sent email")
        except Exception as e:
            st.write("Error: unable to send email.", e)

# User input for OTP verification
otp_input = st.text_input("Enter Your OTP >>")

if st.button("Verify OTP"):
    if otp_input == session_state.otp:  # Verify against the stored OTP in the session state
        st.write("OTP Verified")
    else:
        st.write("Please check your OTP again")
