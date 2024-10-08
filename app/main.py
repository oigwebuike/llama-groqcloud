import streamlit as st
from chain import Chain
from utils import clean_text
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os
from dotenv import load_dotenv
import chromadb

import os
from dotenv import load_dotenv

load_dotenv()

def create_streamlit_app(llm):
    
    url = os.getenv("URL")

    st.title("📧 Job Email Generator")
    url_input = st.text_input("Enter Url:",  value=url)

    submit_button = st.button("Submit")
    if submit_button:
        try:
            loader = WebBaseLoader(url_input)
            data = clean_text(loader.load().pop().page_content)
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get("skills", [])
                email = llm.write_email(job)
                st.code(email, language="markdown")
        except Exception as e:
            st.error(f"Exception: An error occured, {e}")
            

if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Job Email Generator", page_icon="📧")
    create_streamlit_app(chain)
            

