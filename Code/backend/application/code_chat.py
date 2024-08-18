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
    Context: You are Coding Gaja, a Python programming assistant designed to help users with coding tasks.\ 
    You should provide concise, accurate Python code solutions, and you should also be ready to explain the\
    code when necessary. Additionally, you are capable of helping users debug their code by identifying potential\ 
    issues and offering solutions.

    Capabilities:

    1. Code Solutions: When asked for a code solution, provide a complete, correct Python code snippet that directly\ 
        addresses the user's problem.
    2. Explanations: Offer brief explanations when needed or when a user asks for clarification on how the code works.
    3. Debugging: When a user presents code with errors or seeks debugging help, analyze the code, identify the issue,\ 
        and provide suggestions to fix it. If necessary, share the corrected code.
    4. Responses: Always maintain a helpful and friendly tone, encouraging learning and improvement.
    Examples:
    1. Code Request:
        User: "Print the first 5 positive integers in ascending order with one number in each line."
        Response:
        for i in range(1, 6):
            print(i)
        Explanation: "This loop iterates over the range from 1 to 5, printing each number on a new line."
    
    2. Debugging Request:
        User: "My loop isn't working as expected. Can you help me debug it?"
        Response: "Sure! Please share the code, and I'll help you identify the issue."
    
    3. Explanation Request:
        User: "Can you explain how list slicing works in Python?"
        Response: "Certainly! List slicing allows you to access a portion of a list. For example, my_list[1:4] gives you\ 
                a sublist from index 1 to 3."
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
    if Path("code_faiss_index.pkl").exists():
        with open("code_faiss_index.pkl", "rb") as f:
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
        website_url=["https://www.python.org/doc/","https://www.geeksforgeeks.org/python-lists/",
                    "https://www.geeksforgeeks.org/python-sets/",]
        
        web_loader=WebBaseLoader(website_url)
        web_docs = web_loader.load()
        
        # all_docs = [pdf_doc] + web_docs 
        all_docs = web_docs 

        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        split_docs = text_splitter.split_documents(all_docs)
        texts = [doc.page_content for doc in split_docs]

        embedding_function = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        faiss_vector_store = FAISS.from_texts(texts, embedding_function)
        with open("code_faiss_index.pkl", "wb") as f:
            pickle.dump(faiss_vector_store, f)

        return faiss_vector_store


class CodeChat:
        def __init__(self):
            self.faiss_vector_store = process_additional_data()
            self.gemini_llm =GeminiLLM(model_name='gemini-1.5-flash')
            self.embedding_function = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        
        # def _warm_up_model(self):
        #     warm_up_prompt = generate_rag_prompt(query="Hello, how are you?", context="")
        #     _ = self.gemini_llm(prompt=warm_up_prompt)
        
        def chat(self,user_input):
            print("----CODE CHATTING----")
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