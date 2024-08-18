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
import pickle
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
    You are Gajaa, an AI assistant for the IIT Madras Python course. You have access to course lectures, transcripts,\ 
    and all related course materials. Your role is to provide accurate and helpful information about the course content.\ 
    Analyze students' queries and retrieve relevant information from the database. Provide concise and informative responses,\ 
    offering insights and statistics when relevant. When responding to queries, prioritize official IIT Madras policies and guidelines.\ 
    Strictly avoid providing solutions to programming assignments, do not give out any coding assignment questions, and ensure responses\ 
    stay within the scope of the course materials.

    Specific Cases:

        1. Lecture Content: If a student asks about specific lecture topics, concepts, or examples discussed in the course, provide a\ 
        summary or direct them to the relevant lecture or transcript.

        2. Course Structure: For questions about the course syllabus, topics covered, or the sequence of lectures, provide an overview\ 
        and guide the student to the appropriate section of the course materials.

        3. Assignment Guidelines: If asked about assignment requirements or deadlines, clarify the guidelines and refer to the specific\ 
        lecture or document that contains the necessary information. Do not provide direct solutions or coding assignment questions.

        4. Exam Preparation: If a student inquires about preparing for exams, suggest relevant lectures, practice problems, and study\ 
        strategies based on the course content.

        5. Technical Help: For issues related to accessing course materials, videos, or transcripts, offer troubleshooting tips or direct\ 
        the student to technical support.

        6. Resource Recommendations: If a student asks for additional resources like books or articles related to the course topics,\ 
        recommend materials listed in the course syllabus or lectures.

        7. Policy Clarifications: If a student has questions about course policies, grading, or deadlines, refer to the official course\ 
        guidelines and provide accurate information based on the course materials.

        Escalation: If a query falls outside your knowledge base or involves issues beyond course content, politely direct the student to\ 
        the appropriate representative or department for further assistance.
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

pdfreader = PdfReader("Python Transcript(PDF).pdf")
# print("PDF READER", pdfreader)

def process_additional_data():
    # Load or create FAISS index
    if Path("faiss_index.pkl").exists():
        with open("faiss_index.pkl", "rb") as f:
            faiss_vector_store = pickle.load(f)
            return faiss_vector_store
    else:        
        # Extract text from PDF
        pdf_text = ""
        for page in pdfreader.pages:
            pdf_text += page.extract_text()
        
        # Create a Document object from PDF text
        pdf_doc = Document(page_content=pdf_text, metadata={"source": "Python Transcript(PDF).pdf"})
        # print("PDF DOC", pdf_doc)
        website_url=["https://www.geeksforgeeks.org/python-lists/",
                    "https://www.geeksforgeeks.org/python-sets/"]
        
        web_loader=WebBaseLoader(website_url)
        web_docs = web_loader.load()
        
        # youtube_url="https://youtu.be/WQNxG2B85rc"
        # youtube_url=["https://youtu.be/8ndsDXohLMQ?si=GFjlycPWs0Knel3w" , "https://youtu.be/NgZZ0HIUqbs" ,
        #             "https://youtu.be/As7_aq6XGfI" , "https://youtu.be/Yg6xzi2ie5s" , "https://youtu.be/ruQb8jzkGyQ" ,
        #             "https://youtu.be/tDaXdoKfX0k" , "https://youtu.be/8n4MBjuDBu4" , "https://youtu.be/xQXxufhEJHw" , 
        #             "https://youtu.be/8pu73HKzNOE" , "https://youtu.be/Y53K9FFu97Q" , "https://youtu.be/sS89tiDuqoM" , 
        #             "https://youtu.be/e45MVXwya7A" , "https://youtu.be/_Ccezy5hlc8" , "https://youtu.be/XZSnqseRbZY" ,
        #             "https://youtu.be/2OFZY77eOjw" , "https://youtu.be/-f833WH_cVo" , "https://youtu.be/4vWM2oTGEio" , 
        #             "https://youtu.be/bRAo6TJJjCU" , "https://youtu.be/oxFYdHVNpg8" , "https://youtu.be/FTX5wF_3J9Q"]
        # youtube_docs=[]
        # for url in youtube_url:
        #     youtube_loader=YoutubeLoader.from_youtube_url(youtube_url=url,add_video_info=True)
        #     print("Youtube Loader:", youtube_loader)
        #     youtube_docs.extend(youtube_loader.load())
        # print("Youtube DOCS:", youtube_docs)

        # all_docs = [pdf_doc] + web_docs + youtube_docs
        all_docs = [pdf_doc] + web_docs 

        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        split_docs = text_splitter.split_documents(all_docs)
        texts = [doc.page_content for doc in split_docs]

        embedding_function = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        faiss_vector_store = FAISS.from_texts(texts, embedding_function)
        with open("faiss_index.pkl", "wb") as f:
            pickle.dump(faiss_vector_store, f)

        return faiss_vector_store


class VideoChat:
        def __init__(self):
            self.faiss_vector_store = process_additional_data()
            self.gemini_llm =GeminiLLM(model_name='gemini-1.5-flash')
            self.embedding_function = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        
        def _warm_up_model(self):
            warm_up_prompt = generate_rag_prompt(query="Hello, how are you?", context="")
            _ = self.gemini_llm(prompt=warm_up_prompt)
        
        def chat(self,user_input):
            print("CHAT WITH CONTENT")
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