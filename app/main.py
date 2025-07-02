import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    st.title("📧 Cold Email Generator")

    url_input = st.text_input("Enter a Job Post URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Generate Email")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = loader.load().pop().page_content
            cleaned_data = clean_text(data)

            portfolio.load_portfolio()
            jobs = llm.extract_jobs(cleaned_data)

            for job in jobs:
                skills = job.get('skills', [])
                metadata = portfolio.query_links(skills)
                flat_links = [meta["links"] for meta in metadata if "links" in meta]
                links_str = "\n".join(flat_links)
                email = llm.write_mail(job, links_str)
                st.subheader(f"Cold Email for: {job.get('role', 'Unknown Role')}")
                st.code(email, language="markdown")

        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio)
