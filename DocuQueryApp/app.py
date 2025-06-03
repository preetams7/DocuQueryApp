import streamlit as st
import pandas as pd
import retrievalmodule 
from retrievalmodule import DocumentRetrievalChain
import os

st.set_page_config(layout='wide')

st.header("DocuQuery (concept)")

# File uploader widget
uploaded_file = st.file_uploader("Upload a source PDF file to query", type=["pdf"])



# Save file to desired location
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        st.success("The uploaded file is a valid PDF.")
        folder_path = "resources"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        save_path = os.path.join(folder_path, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        question = st.text_input("Enter your question here", key="question")
        retrieval_chain_ob = DocumentRetrievalChain()
        retrieval_chain = retrieval_chain_ob.get_chain()

        if question:
            with st.spinner("Thinking ...")
            answer = retrieval_chain({"question":question}, return_only_outputs=True)
            answer = answer['answer']
            st.write(answer)
    else:
        st.error("Please upload a valid PDF file.")

    