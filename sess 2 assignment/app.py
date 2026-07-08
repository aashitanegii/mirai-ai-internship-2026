import streamlit as st
st.title("The Identity Echo Interface")
st.write("Enter your name and message below.")

user_name = st.text_input("Enter your Name")
user_message = st.text_input("Enter your Message")

if st.button("Transmit"):

    if user_name == "":
        st.error("Please provide your name.")

    elif user_message == "":
        st.warning("Please type a message to transmit.")

    else:
        st.success(
            f"Transmission successful! Greetings, {user_name}. We received your message: {user_message}"
        )

        token_count = len(user_message) / 4

        st.info(
            f"System Check: Your message will consume approximately {token_count:.2f} tokens from our context window."
        )
