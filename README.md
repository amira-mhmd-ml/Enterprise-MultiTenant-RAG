# 🏢 Enterprise Multi-Tenant RAG Platform

An advanced, production-ready Retrieval-Augmented Generation (RAG) system. This platform is designed to handle document intelligence for multiple organizations (Multi-Tenancy) with high-precision retrieval using **Flashrank Reranking** and **Qdrant Vector Database**.

---

## 🏗️ Project Architecture & Structure

The project is designed with a clear separation of concerns, featuring a robust **FastAPI** backend and an intuitive **Streamlit** frontend.

**📁 Folder Hierarchy:**
![Project Structure](./image_897c42.png) 
*Clean modular structure for easy scalability.*

---

## 🚀 Key Technical Features

### 1. High-Precision Retrieval (Reranking)
Beyond standard vector search, this system implements a **Reranking** layer using **Flashrank**. This ensures the LLM receives only the most contextually relevant snippets, significantly reducing hallucinations.

**🔍 Smart Extraction Example:**
![Achievement Extraction](./screenshots/Lllmfinaal.jpg)
*The AI accurately extracts specific technical metrics (e.g., "Reduced manual efforts by 20%").*

### 2. Multi-Tenant Data Isolation
Security is a priority. Using **Metadata Filtering**, the system ensures strict data isolation between different `company_id`s.

**🔒 Privacy in Action:**
![Privacy Isolation](./screenshots/llm%20privucy.jpg)
*The system refuses to answer questions if the data belongs to a different tenant ID.*

### 3. Comprehensive Ingestion Pipeline
The platform supports automated indexing for PDF, DOCX, and HTML files, utilizing `RecursiveCharacterTextSplitter` for optimal context preservation.

---

## 📸 Platform Demo

### 🗨️ Intelligent Querying
The assistant is capable of answering complex professional questions by scanning through the uploaded knowledge base.
![Technical Query](./screenshots/llm3.jpg)

### 🛠️ Technical Tool Identification
The system identifies specific frameworks and tools mentioned within the documents with high accuracy.
![Tools Identification](./screenshots/llm%20best%20.jpg)

---

## 🛠️ Tech Stack

* **LLM**: Llama 3.3 (via Groq Cloud)
* **Orchestration**: LangChain
* **Vector DB**: Qdrant
* **Backend**: FastAPI
* **Frontend**: Streamlit
* **Reranker**: Flashrank
* **Embeddings**: HuggingFace `all-MiniLM-L6-v2`

---

## 🚦 Getting Started

1. **Clone the Repo:**
   ```bash
   git clone [https://github.com/amira-mhmd-ml/enterprise-rag.git](https://github.com/amira-mhmd-ml/enterprise-rag.git)