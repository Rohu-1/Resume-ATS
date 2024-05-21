import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input):
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

I want the response single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}

"""
# Set page configuration
st.set_page_config(
    page_title="Smart ATS",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS for grey background and styling
st.markdown(
    """
    <style>
    body {
        background-color: #ADB5BD;
    }
    .stApp {
        background-color: #ADB5BD;
    }
    .stButton button {
        background-color: #007BFF;
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 12px;
    }
    .stButton button:hover {
        background-color: white;
        color: black;
        border: 2px solid #007BFF;
    }
    .response-container {
        background-color: #ffffff;
        border: 2px solid #007BFF;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
    }
    .response-text {
        font-size: 18px;
        color: #212529;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown("<h1 style='color: #007BFF;'>Smart ATS</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='color: #007BFF;'>Improve your Resume ATS</h1>", unsafe_allow_html=True)
# Custom CSS for styling

jd=st.text_area("Paste the Job Description")

uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")


st.markdown(
    """
    <style>
    .stButton button {
        background-color: #007BFF; /* Green background */
        border: none; /* Remove borders */
        color: white; /* White text */
        padding: 15px 32px; /* Some padding */
        text-align: center; /* Center the text */
        text-decoration: none; /* Remove underline */
        display: inline-block; /* Get the element to fit beside other elements */
        font-size: 16px; /* Increase font size */
        margin: 4px 2px; /* Some margin */
        transition-duration: 0.4s; /* Transition effect for hover (smooth transition) */
        cursor: pointer; /* Pointer/hand icon on hover */
        border-radius: 12px; /* Rounded corners */
    }
    .stButton button:hover {
        background-color: white; /* White background on hover */
        color: black; /* Black text on hover */
        border: 2px solid #4CAF50; /* Green border on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)




# Add the submit button
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt)
        
        st.markdown(
            f"""
            <div class="response-container">
                <div class="response-text">
                    <strong>Gemini AI Response:</strong>
                    <p>{response}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("Please upload a PDF file to proceed.")