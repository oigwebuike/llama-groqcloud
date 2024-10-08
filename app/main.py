import streamlit as st
from chain import Chain
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader
import os
from dotenv import load_dotenv

load_dotenv()

def create_streamlit_app(llm):
    
    url = os.getenv("URL")

    st.title("📧 Job Email Generator")
    url_input = st.text_input("Enter Url: (Required)",  value=url)
    name_input = st.text_input("Enter Name: (Required)", value="name")
    current_role = st.text_input("Enter Current Role:", value="")
    current_company = st.text_input("Enter Current Company:", value="")
    linkedin_addr = st.text_input("Enter Linkedin:", value="")
    short_desc = st.text_input("Enter a short description of your current role at your company: (Required)")

    submit_button = st.button("Submit")
    if submit_button:
        # Check if the name field is filled before allowing submission
        if name_input and url_input and short_desc:
            st.success(f"Hello, {name_input}! Your input has been received.")
        else:
            st.error("Name, url and a short description of yourself are required. Please enter your name before submitting.")
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get("skills", [])
                email = llm.write_email(name_input, short_desc, current_company, linkedin_addr, current_role, job)
                st.code(email, language="markdown")
        except Exception as e:
            st.error(f"Exception: An error occured, {e}")
            

if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Job Email Generator", page_icon="📧")
    create_streamlit_app(chain)
            

