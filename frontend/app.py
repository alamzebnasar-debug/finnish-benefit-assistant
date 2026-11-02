import streamlit as st
import requests

# Configure Streamlit page layout
st.set_page_config(
    page_title="Finnish Public Benefit Assistant",
    page_icon="🇫🇮",
    layout="centered"
)

# API endpoint for our FastAPI backend
FASTAPI_URL = "http://127.0.0.1:8000/ask"

st.title("🇫🇮 Finnish Benefit & Tax Assistant")
st.markdown("Ask any questions about **Kela** general housing allowances or **Vero** remote work tax deductions!")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hei! I am your Finnish public benefits assistant. Ask me anything about Kela benefits or Vero tax deductions."
        }
    ]

# Display prior chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If sources were stored with the assistant message, show them in an expander
        if "sources" in message and message["sources"]:
            with st.expander("📚 View Source Documents"):
                for idx, source in enumerate(message["sources"], 1):
                    st.markdown(f"**Source {idx}:** {source}")

# Accept user input from the chat box at the bottom
if prompt := st.chat_input("Type your question here... (e.g., What are the student housing allowance rules?)"):
    
    # 1. Append user message to state and display it immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Query our FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Searching guidelines and consulting Gemini..."):
            try:
                response = requests.post(
                    FASTAPI_URL,
                    json={"question": prompt},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer returned.")
                    sources = data.get("sources", [])
                    
                    # Display the answer
                    st.markdown(answer)
                    
                    # Display sources inside an expandable dropdown
                    if sources:
                        with st.expander("📚 View Source Documents"):
                            for idx, source in enumerate(sources, 1):
                                st.markdown(f"**Source {idx}:** {source}")
                    
                    # Append assistant response and sources to session history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                else:
                    error_detail = response.json().get("detail", "Unknown server error")
                    err_msg = f"⚠️ Server Error ({response.status_code}): {error_detail}"
                    st.error(err_msg)
            
            except requests.exceptions.ConnectionError:
                st.error("🚨 Failed to connect to the FastAPI backend. Make sure your Uvicorn server is running (`uvicorn backend.main:app --reload`)!")
            except Exception as e:
                st.error(f"⚠️ An unexpected error occurred: {e}")