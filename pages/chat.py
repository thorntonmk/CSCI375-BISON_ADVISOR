from dotenv import load_dotenv
import streamlit as st
from streamlit_chat import message
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)


def main():
    load_dotenv()
    st.set_page_config(page_title="Production")
    st.header("AI Bison Advising")
    # noinspection SpellCheckingInspection
    maindoc = open('CS courses.pdf', 'rb')
    option = st.selectbox(
        'What do you want?',
        ('Course', 'Questions', "Risk"))

    if option == "Course":
        return courses(maindoc)

    if option == "Questions":
        return study()

    if option == "Risk":
        return risk()


# upload file


def courses(pdf):
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        user_question = st.text_input("What questions do you have about your curriculum? ")  # User input

        if user_question:
            docs = knowledge_base.similarity_search(user_question)

            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=user_question)
                print(cb)  # Prints cost to python output
            st.write(response)  # this is the official out put for the question


def risk():
    pdf = st.file_uploader("Upload your Transcript", type="pdf")
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        # show user input

        user_question = st.text_input("How May I Help You? ")  # User input
        if user_question:
            docs = knowledge_base.similarity_search(user_question)

            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=user_question)
                print(cb)  # Prints cost to python output
            st.write(response)  # this is the official out put for the question


def init():
    # Load the OpenAI API key from the environment variable
    load_dotenv()


def study():
    init()

    chat = ChatOpenAI(temperature=0, )

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a study assistant.")
        ]

    st.header("Welcome to Bison AI")

    # sidebar with user input
    user_input = st.text_input("Enter your question", key="user_input")

    # handle user input
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Thinking..."):
            response = chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')


if __name__ == '__main__':
    main()
