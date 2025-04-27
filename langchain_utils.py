from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
import os
from chroma_utils import vectorstore


retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
output_parser = StrOutputParser()




# Set up prompts and chains
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])



qa_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an educational AI assistant designed to help parents and children become more aware of human trafficking risks and prevention strategies. "
     "Answer all questions using only the provided context related to human trafficking. "
     "If the answer is not found in the context, politely say 'I'm sorry, I don't have enough information based on what I know.' "
     "If the user sends a casual greeting or message (e.g., 'hi', 'hello', 'thank you', 'okay', 'bye'), respond politely and appropriately without needing any context. "
     "Stay positive, supportive, and educational at all times."),
    
    ("system", "Context: {context}"),

    MessagesPlaceholder(variable_name="chat_history"),

    ("human", "{input}")
])


def get_rag_chain(model="gpt-4o-mini"):
    llm = ChatOpenAI(model=model)
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)    
    return rag_chain



 
    