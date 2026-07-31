import streamlit as st
import pandas as pd
import numpy as np
import re

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="AI Resume Optimizer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Optimizer")
st.write(
    "Analyze your resume, calculate an ATS-style score, "
    "and get suggestions to improve your job compatibility."
)

# ---------------------------------
# SIDEBAR
# ---------------------------------

st.sidebar.header("⚙️ ANALYSIS SETTINGS")

job_role = st.sidebar.selectbox(
    "SELECT JOB ROLE",
    [
        "Software Engineer",
        "Frontend Developer",
        "Data Analyst",
        "AI / ML Engineer",
        "Product Manager"
    ]
)

analysis_level = st.sidebar.slider(
    "ANALYSIS LEVEL",
    min_value=1,
    max_value=10,
    value=7
)

# ---------------------------------
# SKILLS DATABASE
# ---------------------------------

role_skills = {
    "Software Engineer": [
        "python", "java", "git", "sql",
        "data structures", "algorithms", "api"
    ],

    "Frontend Developer": [
        "html", "css", "javascript", "react",
        "typescript", "git", "api"
    ],

    "Data Analyst": [
        "python", "sql", "excel", "pandas",
        "numpy", "power bi", "tableau"
    ],

    "AI / ML Engineer": [
        "python", "machine learning", "numpy",
        "pandas", "tensorflow", "pytorch", "ai"
    ],

    "Product Manager": [
        "product management", "analytics",
        "strategy", "communication",
        "agile", "research", "leadership"
    ]
}

# ---------------------------------
# USER INPUT
# ---------------------------------

st.subheader("📥 Resume & Job Information")

resume_text = st.text_area(
    "PASTE YOUR RESUME",
    height=250,
    placeholder="Paste your resume text here..."
)

job_description = st.text_area(
    "PASTE JOB DESCRIPTION",
    height=180,
    placeholder="Paste the job description here..."
)

# ---------------------------------
# ANALYSIS BUTTON
# ---------------------------------

if st.button("🚀 ANALYZE RESUME", use_container_width=True):

    if not resume_text.strip():
        st.warning("Please paste your resume before starting the analysis.")

    elif not job_description.strip():
        st.warning("Please paste the job description before starting the analysis.")

    else:

        resume_lower = resume_text.lower()
        job_lower = job_description.lower()

        # ---------------------------------
        # SKILLS ANALYSIS
        # ---------------------------------

        required_skills = role_skills[job_role]

        matched_skills = [
            skill for skill in required_skills
            if skill in resume_lower
        ]

        missing_skills = [
            skill for skill in required_skills
            if skill not in resume_lower
        ]

        skills_score = int(
            (len(matched_skills) / len(required_skills)) * 100
        )

        # ---------------------------------
        # KEYWORD ANALYSIS
        # ---------------------------------

        job_words = set(
            re.findall(r"\b[a-zA-Z]{4,}\b", job_lower)
        )

        resume_words = set(
            re.findall(r"\b[a-zA-Z]{4,}\b", resume_lower)
        )

        common_keywords = job_words.intersection(resume_words)

        if len(job_words) > 0:
            keyword_score = int(
                (len(common_keywords) / len(job_words)) * 100
            )
        else:
            keyword_score = 0

        # ---------------------------------
        # RESUME SECTION ANALYSIS
        # ---------------------------------

        important_sections = [
            "education",
            "experience",
            "skills",
            "projects"
        ]

        found_sections = [
            section for section in important_sections
            if section in resume_lower
        ]

        section_score = int(
            (len(found_sections) / len(important_sections)) * 100
        )

        # ---------------------------------
        # FORMATTING / CONTENT SCORE
        # ---------------------------------

        word_count = len(resume_text.split())

        if 300 <= word_count <= 800:
            formatting_score = 100
        elif 200 <= word_count < 300 or 800 < word_count <= 1000:
            formatting_score = 75
        else:
            formatting_score = 50

        # ---------------------------------
        # ATS SCORE
        # ---------------------------------

        ats_score = int(
            skills_score * 0.35
            + keyword_score * 0.30
            + section_score * 0.20
            + formatting_score * 0.15
        )

        # ---------------------------------
        # DASHBOARD
        # ---------------------------------

        st.divider()

        st.subheader("📊 ATS ANALYSIS")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="ATS SCORE",
                value=f"{ats_score}/100",
                delta="Strong" if ats_score >= 70 else "Needs Improvement"
            )

        with col2:
            st.metric(
                label="SKILLS MATCH",
                value=f"{skills_score}%",
                delta=f"{len(matched_skills)} skills found"
            )

        with col3:
            st.metric(
                label="KEYWORD MATCH",
                value=f"{keyword_score}%",
                delta=f"{len(common_keywords)} matches"
            )

        with col4:
            st.metric(
                label="RESUME STRUCTURE",
                value=f"{section_score}%",
                delta=f"{len(found_sections)}/4 sections"
            )

        # ---------------------------------
        # SCORE CHART
        # ---------------------------------

        st.divider()

        st.subheader("📈 Resume Score Breakdown")

        score_data = pd.DataFrame(
            {
                "Score": [
                    skills_score,
                    keyword_score,
                    section_score,
                    formatting_score
                ]
            },
            index=[
                "Skills Match",
                "Keyword Match",
                "Resume Structure",
                "Formatting"
            ]
        )

        st.bar_chart(score_data)

        # ---------------------------------
        # MATCHED / MISSING SKILLS
        # ---------------------------------

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Matched Skills")

            if matched_skills:
                for skill in matched_skills:
                    st.success(skill.title())
            else:
                st.info("No major required skills were detected.")

        with col2:

            st.subheader("⚠️ Missing Skills")

            if missing_skills:
                for skill in missing_skills:
                    st.warning(skill.title())
            else:
                st.success("Great! All major role skills were detected.")

        # ---------------------------------
        # FEEDBACK
        # ---------------------------------

        st.divider()

        st.subheader("💡 Resume Feedback")

        if ats_score >= 80:

            st.success(
                "Excellent! Your resume shows strong compatibility "
                "with this job profile."
            )

        elif ats_score >= 60:

            st.info(
                "Your resume has a good foundation, but improving "
                "keywords and missing skills could increase its ATS score."
            )

        else:

            st.warning(
                "Your resume needs optimization before applying. "
                "Focus on relevant skills, keywords, projects, and structure."
            )

        # Specific recommendations

        st.write("### 🎯 Recommended Improvements")

        if missing_skills:
            st.write(
                "**Skills to consider adding (only if you genuinely have them):**"
            )

            st.write(", ".join(skill.title() for skill in missing_skills))

        if keyword_score < 60:
            st.write(
                "• Use more relevant terminology from the job description "
                "where it accurately reflects your experience."
            )

        if section_score < 100:
            st.write(
                "• Make sure your resume clearly includes Education, "
                "Experience, Skills, and Projects sections where applicable."
            )

        if formatting_score < 100:
            st.write(
                "• Keep the resume concise and make important information "
                "easy for recruiters and ATS systems to identify."
            )

        # ---------------------------------
        # DATA TABLE
        # ---------------------------------

        st.divider()

        st.subheader("📋 Analysis Summary")

        summary = pd.DataFrame(
            {
                "Category": [
                    "ATS Score",
                    "Skills Match",
                    "Keyword Match",
                    "Resume Structure",
                    "Formatting",
                    "Resume Word Count"
                ],

                "Result": [
                    f"{ats_score}/100",
                    f"{skills_score}%",
                    f"{keyword_score}%",
                    f"{section_score}%",
                    f"{formatting_score}%",
                    word_count
                ]
            }
        )

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "⚠️ This dashboard provides an educational ATS-style estimate. "
            "Real Applicant Tracking Systems use different scoring and "
            "screening methods."
        )