#!/usr/bin/env python3

import os
import argparse

from langchain_community.document_loaders import TextLoader, ToMarkdownLoader
from langchain import hub
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible.
Always say "thanks for asking!" at the end of the answer.

{context}

Question: {question}

Helpful Answer:"""

key = os.environ["OPENAI_API_KEY"]

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=key)

loader = TextLoader("./index.md")
docs = loader.load()

prompt = PromptTemplate.from_template(template)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

retriever = vectorstore.as_retriever()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


def ask_question(question):
    return rag_chain.invoke(question)


# Add argparse code here
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ask a question.")
    parser.add_argument("question", type=str, help="The question to ask.")
    args = parser.parse_args()
    print(ask_question(args.question))
    vectorstore.delete_collection()
