import streamlit as st
import os
import time
from langchain_groq import ChatGroq
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# If you don't have OpenAI key, use Huggingface embeddings
os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")
from langchain_huggingface import HuggingFaceEmbeddings

# Initialize embeddings and LLM
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma2-9b-It")

# Define prompt template
prompt = ChatPromptTemplate.from_template("""
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question.
<context>
{context}
</context>
Question:{input}
""")

# Function to create vector embeddings for documents
def create_vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = embeddings
        st.session_state.loader = PyPDFDirectoryLoader("legal_documents")  # Data ingestion step
        st.session_state.docs = st.session_state.loader.load()  # Load documents
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        # Limit the number of documents for faster processing
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:50])
        
        # Create FAISS vector database
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

# Streamlit UI for the Legal Assistant
st.title("LEGAL ASSISTANT")
user_prompt = st.text_input("Enter Your Query")

# Button for answering
if st.button("Answer"):
    create_vector_embedding()
    st.write("Vector Database is ready")

    # Use the retrieval chain
    if user_prompt:
        # Create a document chain
        document_chain = create_stuff_documents_chain(llm, prompt)
        
        # Create a retriever from the FAISS vector store
        retriever = st.session_state.vectors.as_retriever()
        
        # Create the retrieval chain
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        start = time.process_time()
        
        # Get the response
        response = retrieval_chain.invoke({'input': user_prompt})
        
        # Display response time
        st.write(f"Response time: {time.process_time() - start:.2f} seconds")

        # Display the answer
        st.write("Answer:")
        st.write(response['answer'])
        
        # Display the document similarity search with a Streamlit expander
        with st.expander("Document Similarity Search"):
            for i, doc in enumerate(response['context']):
                st.write(f"Document {i+1}:")
                st.write(doc.page_content)
                st.write('------------------------')
