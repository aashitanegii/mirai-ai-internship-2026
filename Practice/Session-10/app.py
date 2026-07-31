import streamlit as st

st.set_page_config(
    page_title="Course Registration",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Course Registration Form")
st.write("Fill in your details to register for a course.")

# Create Form
with st.form("course_registration_form"):

    name = st.text_input(
        "FULL NAME",
        placeholder="Enter your name"
    )

    email = st.text_input(
        "EMAIL",
        placeholder="Enter your email"
    )

    course = st.selectbox(
        "SELECT COURSE",
        [
            "Artificial Intelligence",
            "Web Development",
            "Data Science",
            "Cyber Security",
            "UI/UX Design"
        ]
    )

    year = st.selectbox(
        "COLLEGE YEAR",
        [
            "1st Year",
            "2nd Year",
            "3rd Year",
            "4th Year"
        ]
    )

    experience = st.slider(
        "PROGRAMMING EXPERIENCE",
        min_value=0,
        max_value=5,
        value=1
    )

    learning_mode = st.radio(
        "PREFERRED LEARNING MODE",
        ["Online", "Offline", "Hybrid"]
    )

    reason = st.text_area(
        "WHY DO YOU WANT TO JOIN?",
        placeholder="Tell us briefly..."
    )

    agree = st.checkbox(
        "I confirm that the information is correct."
    )

    # Every form needs a form submit button
    submitted = st.form_submit_button(
        "🚀 REGISTER"
    )


# Process data after form submission
if submitted:

    if not name or not email:
        st.warning("⚠️ Please enter your name and email.")

    elif not agree:
        st.warning("⚠️ Please confirm your information.")

    else:
        st.success("✅ Registration Successful!")

        st.divider()

        st.subheader("📋 Registration Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Student:**")
            st.write(name)

            st.write("**Course:**")
            st.write(course)

            st.write("**Learning Mode:**")
            st.write(learning_mode)

        with col2:
            st.write("**Email:**")
            st.write(email)

            st.write("**College Year:**")
            st.write(year)

            st.write("**Experience:**")
            st.write(f"{experience} years")

        if reason:
            st.write("### 💭 Reason for Joining")
            st.write(reason)