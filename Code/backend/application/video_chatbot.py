from dotenv import load_dotenv
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
import google.generativeai as genai
from PyPDF2 import PdfReader
import os
from langchain.llms.base import LLM
from typing import Any, List, Optional, Dict
from pydantic import Field
from langchain.schema import Document
# from pytube import YouTube

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")


class GeminiLLM(LLM):
    model_name: str = Field(..., description="gemini-pro")
    model: Any = Field(None, description="The GenerativeModel instance")
    
    def __init__(self, model_name: str):
        super().__init__(model_name=model_name)
        # self.model_name = model_name
        api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model_name)
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.model.generate_content(prompt)
        return response.text
    
    @property
    def _llm_type(self) -> str:
        return "gemini"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {"model_name": self.model_name}
    
# load_dotenv(Path(".env"))
# load_dotenv()
# print("LOAD_DOTENV:",load_dotenv())

def generate_rag_prompt(query, context):
    prompt=("""
    You are V.Chatty an AI assistant for Video Lectures. Your role is to provide accurate and helpful information\
    about the Lectures.Analyze student's queries and retrieve relevant information to the course content and video\
    in the the database.Provide concise and informative response to the student.Use this information to offer insights\
    and statistics when answering questions. Please strictly don't give answer to any of the question that asks you to\
    give a solution to a programming assignment,When responding to queries, prioritize official IIT Madras policies and guidelines.\
    Strictly don't go outside the scope of video\ 
    If a query falls outside your knowledge base, politely direct the Student to the appropriate representative.\
            QUESTION: '{query}'
            CONTEXT: '{context}'

            Response: 
""").format(query=query,context=context)
    return prompt

def generate_answer(prompt):
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    print("GEMINI API KEY:",os.getenv('GEMINI_API_KEY'))
    llm = genai.GenerativeModel(model_name='gemini-pro')
    answer = llm.generate_content(prompt)
    return answer.text

pdfreader = PdfReader("lec1.pdf")

def process_additional_data():
    # Extract text from PDF
    pdf_text = ""
    for page in pdfreader.pages:
        pdf_text += page.extract_text()
    
    # Create a Document object from PDF text
    pdf_doc = Document(page_content=pdf_text, metadata={"source": "lec1.pdf"})
    
    website_url=["https://www.geeksforgeeks.org/python-lists/",
                 "https://www.geeksforgeeks.org/python-sets/"]
    
    web_loader=WebBaseLoader(website_url)
    web_docs = web_loader.load()
    
    youtube_url="https://youtu.be/WQNxG2B85rc"
    youtube_loader=YoutubeLoader.from_youtube_url(youtube_url=youtube_url,add_video_info=True)
    print("Youtube Loader:", youtube_loader)
    youtube_docs = youtube_loader.load()

    all_docs = [pdf_doc] + web_docs + youtube_docs

    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    split_docs = text_splitter.split_documents(all_docs)
    texts = [doc.page_content for doc in split_docs]
    embedding_function = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    faiss_vector_store = FAISS.from_texts(texts, embedding_function)

    return faiss_vector_store


class VideoChat:
        def __init__(self):
            self.faiss_vector_store = process_additional_data()
            self.gemini_llm =GeminiLLM(model_name='gemini-1.5-flash')
            self.embedding_function = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        
        def chat(self,user_input):
            if isinstance(user_input,list):
                user_input=''.join(user_input)
            # user_embedding = self.embedding_function.embed_query(user_input)
            # query_text = user_input.strip()
            relevant_docs = self.faiss_vector_store.similarity_search(user_input,k=3)
            context="\n".join([doc.page_content for doc in relevant_docs])
            prompt = generate_rag_prompt(query=user_input, context=context)
            # answer=generate_answer(prompt=prompt)
            answer=self.gemini_llm(prompt=prompt)
            return answer