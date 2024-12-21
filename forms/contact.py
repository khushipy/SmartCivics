import streamlit as st 
import re
import requests

def is_valid_email(email):
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_pattern, email) is not None
def contact_form():
    with st.form("Registration Form"):
        name = st.text_input("First Name")
        last = st.text_input("Last Name")
        email = st.text_input("Email Address")
        message = st.text_area("Your Message")
        submit_button = st.form_submit_button("submit")
        if submit_button:
            if not name:
                st.error(
                    "Provide Name Please.",icon="📧"
                )
                st.stop()
            if not email:
                st.error(
                    "Provide Email Please.",icon="📧"
                )
                st.stop()
            if not is_valid_email(email):
                st.error(
                    "Provide Valid Email Please.",icon="📧"
                )
                st.stop()
            if not message:
                st.error(
                    "Provide message Please.",icon="📧"
                )
                st.stop()
            st.success("Your Registration is done Successfully 🎉", icon="🚀")

