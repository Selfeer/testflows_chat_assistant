#!/usr/bin/env python3

import argparse
import getpass
import os

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

from template import template


def set_openai_api_key():
    """Set the OpenAI API key as an environment variable if not already set."""
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = getpass.getpass(prompt="Enter OpenAI API key: ")


def load_data_from_file(file_path):
    """Load data from a file into a document object."""
    loader = TextLoader(file_path)

    return loader.load()


def format_docs(docs):
    """Format the documents for the RAG chain."""
    return "\n\n".join(doc.page_content for doc in docs)


def ask_question(question):
    """Ask a question about TestFlows and get an answer."""
    key = os.environ["OPENAI_API_KEY"]

    llm = ChatOpenAI(model="gpt-4-turbo", api_key=key)

    docs = load_data_from_file("./index.md")

    prompt = PromptTemplate.from_template(template)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    retriever = vectorstore.as_retriever()

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print(rag_chain.invoke(question))

    vectorstore.delete_collection()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ask a question.")
    parser.add_argument("question", type=str, help="The question to ask.")
    args = parser.parse_args()

    set_openai_api_key()

    ask_question(args.question)
