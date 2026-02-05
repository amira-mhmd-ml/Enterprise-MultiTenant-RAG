import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="Enterprise RAG v2", layout="wide")
st.title("🏢 Advanced Multi-Tenant RAG Platform")

# 2. Sidebar: Admin & Control (For indexing new files)
with st.sidebar:
    st.header("⚙️ Admin Settings")
    company_id = st.text_input("Active Company ID", value="company_1")
    uploaded_file = st.file_uploader("Upload (PDF, Word, HTML)", type=["pdf", "docx", "html"])
    
    if st.button("Index Knowledge Base") and uploaded_file:
        with st.spinner("Processing and Indexing..."):
            # Prepare the file for the request
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {"company_id": company_id}
            
            try:
                # This calls the /ingest endpoint in your main.py
                res = requests.post("http://localhost:8000/ingest", files=files, data=data)
                if res.status_code == 200:
                    st.success(res.json().get("message", "Success!"))
                else:
                    st.error(f"Error indexing: {res.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

# 3. Chat Interface
st.subheader("💬 Smart AI Assistant")

# We use a form or a container to keep the chat organized
question = st.text_input("Ask anything about your data:")

if question:
    with st.spinner("Searching knowledge base..."):
        # We send a JSON payload to the /ask endpoint
        payload = {
            "company_id": company_id,
            "question": question
        }
        
        try:
            # Calling the FastAPI backend
            res = requests.post("http://localhost:8000/ask", json=payload)
            
            if res.status_code == 200:
                answer = res.json().get("answer")
                st.markdown("### Assistant Response:")
                st.info(answer)
                
                # Feedback Section (The "Senior" touch for HR)
                st.write("---")
                c1, c2 = st.columns([1, 15])
                with c1: st.button("👍", key="up")
                with c2: st.button("👎", key="down")
            else:
                st.error(f"Backend Error {res.status_code}: {res.text}")
                
        except Exception as e:
            st.error(f"Could not connect to Backend. Is main.py running? \nError: {e}")