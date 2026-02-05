from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from query import ask_enterprise_rag
from ingest import start_ingestion 

from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

class QueryRequest(BaseModel):
    company_id: str
    question: str

@app.post("/ingest")
async def ingest_endpoint(file: UploadFile = File(...), company_id: str = Form(...)):
    try:
        file_path = os.path.join(TEMP_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
      
        start_ingestion(file_path, company_id)
        
        os.remove(file_path)
        
        return {"message": f"Successfully indexed {file.filename} for {company_id}!"}
    
    except Exception as e:
        print(f"❌ Ingest Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_endpoint(request: QueryRequest):
    try:
     
        answer = ask_enterprise_rag(request.question)
        return {"answer": answer}
    except Exception as e:
        print(f"❌ Ask Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)