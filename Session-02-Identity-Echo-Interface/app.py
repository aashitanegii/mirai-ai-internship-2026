import streamlit as st

# Title
st.title("The Identity Echo Interface")

# Description
st.write("Enter your name and message below.")

# Inputs
user_name = st.text_input("Enter your Name")
user_message = st.text_input("Enter your Message")

# Button
if st.button("Transmit"):

    if user_name == "":
        st.error("Please provide your name.")

    elif user_message == "":
        st.warning("Please type a message to transmit.")

    else:
        st.success(
            f"Transmission successful! Greetings, {user_name}. We received your message: {user_message}"
        )

        # Bonus Task
        token_count = len(user_message) / 4

        st.info(
            f"System Check: Your message will consume approximately {token_count:.2f} tokens from our context window."
        )
