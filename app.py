import streamlit as st
import os
import sys
import importlib.util
from dotenv import load_dotenv

# Load environment variables (API Keys)
load_dotenv()

# Add project directory to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the core PDF builder that works safely
from src.rag_pipeline import build_rag_pipeline

# STATIC EXTRACTION STRATEGY: Parse main.py to grab the runtime 'graph' object without running it
@st.cache_resource
def load_langgraph_instance():
    try:
        main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
        if not os.path.exists(main_path):
            return None
            
        # Read main.py lines to find what it imports or builds
        with open(main_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # If main.py imports graph from somewhere, let's grab it directly from that source
        if "from src.langgraph_flow import" in content or "import graph" in content:
            import src.langgraph_flow as lflow
            if hasattr(lflow, "graph"): return getattr(lflow, "graph")
            if hasattr(lflow, "workflow"): return getattr(lflow, "workflow").compile()
            
        # Fallback to direct script evaluation if it's uniquely declared
        spec = importlib.util.spec_from_file_location("main_module", main_path)
        main_module = importlib.util.module_from_spec(spec)
        
        # Patch input out of the module lifecycle entirely before executing
        main_module.input = lambda *args, **kwargs: "exit"
        sys.modules["main_module"] = main_module
        spec.loader.exec_module(main_module)
        
        if hasattr(main_module, "graph"):
            return getattr(main_module, "graph")
    except Exception:
        pass
        
    # Standard source lookup fallback
    try:
        import src.langgraph_flow as lflow
        for key in dir(lflow):
            attr = getattr(lflow, key)
            if attr.__class__.__name__ == "Pregel":
                return attr
            if attr.__class__.__name__ == "StateGraph":
                return attr.compile()
    except Exception:
        pass
    return None

graph_instance = load_langgraph_instance()

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
                if graph_instance is not None:
                    try:
                        # Invoke your LangGraph workflow
                        response = graph_instance.invoke({
                            "query": user_query,
                            "iteration": 0
                        })
                        
                        # Pull final answer from the graph state dictionary safely
                        final_answer = "No answer generated."
                        if isinstance(response, dict):
                            final_answer = response.get("generation", response.get("answer", response.get("response", str(response))))
                        else:
                            final_answer = str(response)
                        
                        st.markdown(final_answer)
                        st.session_state.messages.append({"role": "assistant", "content": final_answer})
                    
                    except Exception as e:
                        st.error(f"Error executing LangGraph flow: {str(e)}")
                else:
                    st.error("Could not isolate the LangGraph pipeline execution variable. Try running via CLI 'python main.py' to verify runtime status.")
else:
    st.info("Please upload a PDF document above to start chatting.")