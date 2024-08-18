from dotenv import load_dotenv
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
import google.generativeai as genai
from PyPDF2 import PdfReader
import os
from langchain.llms.base import LLM
from typing import Any, List, Optional, Dict
from pydantic import Field
from langchain.schema import Document
import pickle


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
    


def generate_rag_prompt(query, context):
    prompt=("""
    You are Gajaa, the official administrative support chatbot for the IIT Madras BS Degree program.\ 
    You have access to the student handbook, which contains all relevant administrative information.\ 
    Your role is to assist students and prospective students by providing accurate and timely information\ 
    on admissions, course details, schedules, fees, deadlines, and other administrative queries. Respond\ 
    politely, concisely, and in an easy-to-understand manner. If you cannot provide a specific answer,\ 
    guide the user on how to obtain the required information or escalate the query to a human representative.

    Specific Cases:

        1. Admissions Queries: If a student asks about admission procedures, eligibility, or deadlines, provide\ 
        details from the handbook, including links to the admissions portal and relevant contact information.

        2. Course Enrollment: If asked about course registration, prerequisites, or add/drop deadlines, provide the\ 
        necessary steps and deadlines according to the academic calendar.

        3. Fee Payment: For questions regarding fee structure, payment deadlines, or modes of payment, guide students\ 
        with the correct information, including links to the payment portal.

        4. Examination Details: If a student inquires about exam schedules, hall tickets, or grading policies, provide\ 
        the relevant details and direct them to the appropriate section of the student handbook.

        5. Student Support Services: For queries about academic counseling, mentorship, or mental health resources,\ 
        share the contact details and processes outlined in the handbook.

        6. Technical Issues: If a student reports issues with the online portal, course access, or any technical\ 
        difficulties, guide them to the IT support desk or provide troubleshooting steps as listed in the handbook.

        7. Leaves of Absence: For questions regarding applying for leaves of absence, including medical leave or\ 
        personal leave, provide the procedure and any required documentation as per the handbook.

        8. Certificate and Transcripts: If asked about obtaining certificates, transcripts, or other official documents,\ 
        explain the application process and expected timelines.

        Escalation: If the query is beyond your scope or requires human intervention, politely inform the user and\ 
        escalate the issue to the appropriate department or representative.

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
    if Path("support_faiss_index.pkl").exists():
        with open("support_faiss_index.pkl", "rb") as f:
            faiss_vector_store = pickle.load(f)
            return faiss_vector_store
    else:        
        # # Extract text from PDF
        # pdf_text = ""
        # for page in pdfreader.pages:
        #     pdf_text += page.extract_text()
        
        # # Create a Document object from PDF text
        # pdf_doc = Document(page_content=pdf_text, metadata={"source": "Python Transcript(PDF).pdf"})
        # print("PDF DOC", pdf_doc)
        website_url=["https://docs.google.com/document/u/1/d/e/2PACX-1vQB7SYIXQPJr0-WcfekVVSt488MdlkNzRUPacbRh2QgOALXcinPybopWIFlY83tdr_mH1QtrhCIsFUq/pub?urp=gmail_link#h.x92fd0h9amj4",]
        
        web_loader=WebBaseLoader(website_url)
        web_docs = web_loader.load()
        
        # all_docs = [pdf_doc] + web_docs 
        all_docs = web_docs 

        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        split_docs = text_splitter.split_documents(all_docs)
        texts = [doc.page_content for doc in split_docs]

        embedding_function = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        faiss_vector_store = FAISS.from_texts(texts, embedding_function)
        with open("support_faiss_index.pkl", "wb") as f:
            pickle.dump(faiss_vector_store, f)

        return faiss_vector_store


class SupportChat:
        def __init__(self):
            self.faiss_vector_store = process_additional_data()
            self.gemini_llm =GeminiLLM(model_name='gemini-1.5-flash')
            self.embedding_function = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        
        def chat(self,user_input):
            print("----SUPPORT CHATTING----")
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