from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
from langchain import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
class DocumentRetrievalChain:
    def __init__(self):
        for filename in os.listdir("resources"):
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(f"resources/{filename}")
                self.loaded_doc = loader.load()
                break

    def get_chunks(self):
        splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "\t"], chunk_size=400, chunk_overlap=50)
        self.chunks = splitter.split_documents(self.loaded_doc)

    def get_vectordb(self):
        embeddings = HuggingFaceEmbeddings()
        self.vectordb = FAISS.from_documents(self.chunks, embeddings)

    def get_llm(self):
        self.llm = OpenAI(temperature=0.4, max_tokens=100)

    def get_chain(self):
        self.get_chunks()
        self.get_vectordb()
        self.get_llm()
        chain = RetrievalQAWithSourcesChain(llm=self.llm, retriever=self.vectordb.as_retriever(), chain_type="stuff")
        return chain





