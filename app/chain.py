from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
import os
from dotenv import load_dotenv
import chromadb



load_dotenv()
# chroma_client = chromadb.Client()
# collection = chroma_client.create_collection(name="new_collection")

groq_api_key = os.getenv("GROQ_API_KEY")


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
                        model="llama-3.1-70b-versatile",
                        temperature=0,
                        groq_api_key=groq_api_key,
                        max_tokens=None,
                        timeout=None,
                        max_retries=2,
                        # other params...
                        )   
        
    def extract_jobs(self, page_data):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from a career page of a web page
            Your job is to extract the job posting and return it in json format
            containing the following keys: `role`, `experience`, `description`, and `skills`.
            Only return the valid json data.
            ### VALID JSON (NO PREAMBLE):
            """
            )
        chain = prompt_extract | self.llm
        response_chain = chain.invoke(input={"page_data": page_data})

        
        
        try:
            json_parser = JsonOutputParser()
            json_res = json_parser.parse(response_chain.content)
        except OutputParserException:
            raise OutputParserException("Could not parse response, Context too large")
        return json_res if isinstance(json_res, list) else [json_res]
    
    
    # def write_email(self, job, links):
    def write_email(self, job):
        
        email_prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Onyeka, a Machine Learning Engineer at Invia Travels GmbH. Invia is a travel company and I worked in the Review Funnel as a Data Scientist. I worked earlier with the Retention Funnel as a Golang Backend    Developer, and then as a Data Scientist with the Funnel Review. Your job is to write a cold email to the company regarding the job in the description mentioned above in fulfiling the roles described.
            Do not provide a preamble.
            ###EMAIL (NO PREAMBLE):
            
            """
        )
        
        #  try:
        #     json_parser = JsonOutputParser()
        #     json_res = json_parser.parse(response_chain.content)
        # except OutputParserException:
        #     raise OutputParserException("Could not parse response, Context too large")
        # return json_res if isinstance(json_res, list) else [json_res]
       
        chain_email = email_prompt | self.llm     
        email_response = chain_email.invoke({"job_description": str(job)})
        return email_response.content
                
                
        
        