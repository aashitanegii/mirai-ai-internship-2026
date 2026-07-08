import streamlit as st
st.title("Mirai Internship")
st.write("Welcome to the Mirai Internship application! Please fill out the form below to apply for the internship program.")

user_message=st.text_input("What is your name?")
if st.button("Submit"):
    st.write(f"Thank you for your application, {user_message}! We will review your submission and get back to you soon.")
