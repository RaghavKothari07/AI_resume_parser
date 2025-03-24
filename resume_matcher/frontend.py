import streamlit as st
import requests

st.title("AI Resume Matcher")

resume_text = st.text_area("Paste your resume")
if st.button("Upload Resume"):
    response = requests.post("http://127.0.0.1:8000/api/upload-resume/", json={"resume_text": resume_text})
    st.json(response.json())

job_text = st.text_area("Paste a job description")
if st.button("Upload Job Posting"):
    response = requests.post("http://127.0.0.1:8000/api/upload-job/", json={"job_text": job_text})
    st.json(response.json())

if st.button("Match Candidate"):
    response = requests.post("http://127.0.0.1:8000/api/match-candidate/", json={"candidate": resume_text, "job": job_text})
    st.json(response.json())

if st.button("Generate Cover Letter"):
    response = requests.post("http://127.0.0.1:8000/api/generate-cover-letter/", json={"candidate": resume_text, "job": job_text})
    st.write(response.json().get("cover_letter"))
