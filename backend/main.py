from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from query import ask_enterprise_rag
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import shutil
import os

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

os.makedirs("temp_uploads", exist_ok=True)

@app.post("/ingest")
async def ingest_endpoint(file: UploadFile = File(...), company_id: str = Form(...)):
    try:
        file_path = f"temp_uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # success = process_document(file_path, company_id) 
        
        return {"message": f"Successfully indexed {file.filename} for {company_id}!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class QueryRequest(BaseModel):
    company_id: str
    question: str

@app.post("/ask")
async def ask_endpoint(request: QueryRequest):
    try:
        answer = ask_enterprise_rag(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)