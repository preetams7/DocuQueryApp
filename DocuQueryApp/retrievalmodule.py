from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
from langchain import OpenAI
from langchain.chains.combine_documents import StuffDocumentsChain

import os


class DocumentRetrievalChain:
    def __init__(self, pdfdoc):
        loader = PyPDFLoader(pdfdoc)
        self.loaded_doc = loader.load()

    def get_chunks(self):
        splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "\t"], chunk_size=400, chunk_overlap=50)
        self.chunks = splitter.split_documents(self.loaded_doc)

    def get_vectordb(self):
        embeddings = HuggingFaceEmbeddings()
        self.vectordb = FAISS.from_documents(self.chunks, embeddings)

    def get_llm(self):
        
        llm = OpenAI(temperature=0.4, max_tokens=100)
        self.combine_chain = StuffDocumentsChain(llm=llm)

    def get_chain(self):
        self.get_chunks()
        self.get_vectordb()
        self.get_llm()
        chain = RetrievalQAWithSourcesChain(llm=self.combine_chain, retriever=self.vectordb.as_retriever(), chain_type="stuff")
        return chain





