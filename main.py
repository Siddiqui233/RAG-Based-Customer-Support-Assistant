import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables (API Keys)
load_dotenv()

# Import what we know works
from src.rag_pipeline import build_rag_pipeline
from main import graph  # Importing the working graph directly from main.py

st.set_page_config(page_title="RAG LangGraph Assistant", layout="centered")
st.title("🤖 RAG Project with LangGraph")
st.write("Upload a PDF document and chat with your intelligent LangGraph agent.")

# --- PDF Upload Section ---
uploaded_file = st.file_uploader("Upload your PDF data source", type=["pdf"])

if uploaded_file is not None:
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    temp_path = os.path.join("data", "uploaded_notes.pdf")
    
    # Save the uploaded file locally
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Initialize Vectorstore via caching so it doesn't rebuild on every click
    @st.cache_resource
    def init_pipeline(path):
        return build_rag_pipeline(path)
    
    with st.spinner("Processing PDF and building vector database..."):
        vectorstore = init_pipeline(temp_path)
    st.success("Database ready! Your LangGraph agent is listening.")

    # --- Chat Interface Section ---
    st.divider()
    st.subheader("Chat with your Document")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    if user_query := st.chat_input("Ask something about your document..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

        # Generate Agent Answer via LangGraph
        with st.chat_message("assistant"):
            with st.spinner("Agent is analyzing and refining answer..."):
                try:
                    # Invoke your LangGraph workflow exactly like main.py did
                    response = graph.invoke({
                        "query": user_query,
                        "iteration": 0
                    })
                    
                    # Pull final answer from the graph state
                    final_answer = response.get("generation", response.get("answer", "No answer generated."))
                    
                    st.markdown(final_answer)
                    st.session_state.messages.append({"role": "assistant", "content": final_answer})
                
                except Exception as e:
                    # Catch rate limits or missing API key errors cleanly in UI
                    st.error(f"Error executing LangGraph flow: {str(e)}")
else:
    st.info("Please upload a PDF document above to start chatting.")