import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama3-70b-8192"
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template("""
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        Extract job postings from this text. Return them in JSON format with these fields:
        `role`, `experience`, `skills`, `description`.
        Output only valid JSON (no extra text).
        """)

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke({"page_data": cleaned_text})

        try:
            parser = JsonOutputParser()
            result = parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Unable to parse the job listings.")

        return result if isinstance(result, list) else [result]

    def write_mail(self, job, link_list):
        prompt_email = PromptTemplate.from_template("""
        ### JOB DESCRIPTION:
        {job_description}

        ### INSTRUCTION:
        You are Mohan, a business development executive at AtliQ, an AI & Software Consulting company.
        Write a cold email to the client describing how AtliQ can fulfill their needs based on the job role.
        Also, include the most relevant ones from these portfolio links:
        {link_list}
        Don't include a preamble or sign-off. The tone should be formal and concise.

        ### EMAIL:
        """)

        chain_email = prompt_email | self.llm
        response = chain_email.invoke({
            "job_description": str(job),
            "link_list": link_list
        })
        return response.content
