import validators, streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
import os

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Streamlit app title and subheader
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader('Summarize URL')

# Get the Groq API Key and URL (YT or website) to be summarized
groq_api_key = os.getenv("GROQ_API_KEY")
generic_url = st.text_input("URL", label_visibility="collapsed")

# Gemma Model using Groq API
llm = ChatGroq(model="gemma2-9b-It", groq_api_key=groq_api_key)

prompt_template = """
Provide a summary of the following content in 300 words in a point-by-point format:
Content: {text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# If button is pressed to summarize the content
if st.button("Summarize the Content from YT or Website"):
    # Validate all the inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL. It can be a YT video URL or website URL")

    else:
        try:
            with st.spinner("Waiting..."):
                # Loading the website or YT video data
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
                    )
                docs = loader.load()

                # Chain for summarization
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.invoke(docs)

                # Check if the output summary is empty
                if not output_summary.strip():
                    st.error("The summary is empty or wasn't generated properly.")
                else:
                    # Output only the summary, no other details
                    st.success(output_summary)

        except Exception as e:
            st.exception(f"Exception: {e}")

                    
