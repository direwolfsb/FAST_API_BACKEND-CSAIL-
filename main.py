from fastapi import FastAPI
from pydantic_models import QueryInput, QueryResponse, MessageEntry, SessionHistoryResponse
from langchain_utils import get_rag_chain
from db_utils import insert_application_logs, get_chat_history, get_db_connection
from chroma_utils import index_document_to_chroma
from langchain_openai import ChatOpenAI
import uuid
import logging
import json

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Initialize FastAPI app
app = FastAPI()

# ✨ Define casual phrases
casual_phrases = {"hi", "hello", "thanks", "thank you", "ok", "okay", "got it", "bye", "goodbye"}

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    session_id = query_input.session_id
    logging.info(f"Session ID: {session_id}, User Query: {query_input.question}, Model: {query_input.model.value}")

    if not session_id:
        session_id = str(uuid.uuid4())

    chat_history = get_chat_history(session_id)

    # Check if input is casual before doing anything
    normalized_question = query_input.question.strip().lower()

    if normalized_question in casual_phrases:
        # Respond politely without RAG
        polite_responses = {
            "hi": "Hello! How can I assist you today?",
            "hello": "Hello! How can I assist you today?",
            "thanks": "You're very welcome!",
            "thank you": "You're very welcome!",
            "ok": "Okay!",
            "okay": "Okay!",
            "got it": "Glad to hear that!",
            "bye": "Goodbye! Stay safe!",
            "goodbye": "Goodbye! Stay safe!"
        }
        answer = polite_responses.get(normalized_question, "Hello!")
        sources_list = []
    else:
        # Proceed with normal RAG
        rag_chain = get_rag_chain(query_input.model.value)

        result = rag_chain.invoke({
            "input": query_input.question,
            "chat_history": chat_history
        })

        answer = result['answer']
        context_docs = result['context']

        # Fallback if "I don't know"
        fallback_needed = "i'm sorry, i don't have enough information based on what i know" in answer.lower()

        if fallback_needed:
            logging.info("Fallback triggered: using direct ChatGPT knowledge.")
            llm = ChatOpenAI(model=query_input.model.value)
            fallback_response = llm.invoke(query_input.question)
            answer = fallback_response.content
            sources_list = []
        else:
            unique_sources = set()
            for doc in context_docs:
                source = doc.metadata.get('source')
                if source:
                    unique_sources.add(source)

            sources_list = list(unique_sources)

    sources_string = json.dumps(sources_list)

    # Save chat log
    insert_application_logs(
        session_id,
        query_input.question,
        answer,
        query_input.model.value,
        sources_string
    )

    logging.info(f"Session ID: {session_id}, AI Response: {answer}")

    return QueryResponse(
        answer=answer,
        session_id=session_id,
        model=query_input.model,
        sources=sources_list
    )

@app.get("/get_history/{session_id}", response_model=SessionHistoryResponse)
def get_full_chat_history(session_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''SELECT user_query, gpt_response, sources 
           FROM application_logs 
           WHERE session_id = ? 
           ORDER BY created_at ASC''',
        (session_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    history = []
    for row in rows:
        sources = []
        if row['sources']:
            try:
                import json
                sources = json.loads(row['sources'])
            except:
                sources = []
        
        history.append(
            MessageEntry(
                user_query=row['user_query'],
                gpt_response=row['gpt_response'],
                sources=sources
            )
        )

    return SessionHistoryResponse(
        session_id=session_id,
        history=history
    )