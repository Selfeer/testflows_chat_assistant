#!/usr/bin/env python3

import argparse

from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

from template import template


def load_data_from_file():
    """Load data from a file into a document object."""
    loader = WebBaseLoader(
        "https://raw.githubusercontent.com/testflows/TestFlows-WebSite/master/source/handbook/index.md"
    )

    return loader.load()


def format_docs(docs):
    """Format the documents for the RAG chain."""
    return "\n\n".join(doc.page_content for doc in docs)


def set_up_chain(key, model=None):
    """Set up the RAG chain."""
    if model is None:
        model = "gpt-4-turbo"

    llm = ChatOpenAI(model=model, api_key=key)

    docs = load_data_from_file()

    prompt = PromptTemplate.from_template(template)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(
        documents=splits, embedding=OpenAIEmbeddings(openai_api_key=key)
    )

    retriever = vectorstore.as_retriever()

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain, vectorstore


def ask_a_question(chain):
    """Ask a question to the RAG chain."""
    while True:
        question = input("Ask a question: ")

        if question == "exit":
            break

        print(chain.invoke(question))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set up the RAG chain.")
    parser.add_argument("--key", type=str, required=True, help="OpenAI API key.")
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4-turbo",
        help="OpenAI LLM model to use for the RAG chain.",
    )
    args = parser.parse_args()

    rag_chain, vectorstore = set_up_chain(key=args.key, model=args.model)

    ask_a_question(chain=rag_chain)

    vectorstore.delete_collection()
