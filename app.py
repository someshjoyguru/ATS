import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

## streamlit app

st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
jd=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit = st.button("Tell Me About the Resume")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        # Parse the generated JSON string
        try:
            response_json = json.loads(response)
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON: {e}")
            response_json = {}

        # Display the output using Streamlit
        st.subheader("ATS Resume Evaluation Result")
        
        if "JD Match" in response_json:
            st.write(f"JD Match: {response_json['JD Match']}%")

        if "MissingKeywords" in response_json:
            st.write(f"Missing Keywords: {', '.join(response_json['MissingKeywords'])}")

        if "Profile Summary" in response_json:
            st.write(f"Profile Summary: {response_json['Profile Summary']}")
    else:
        st.write("Please upload the resume")

