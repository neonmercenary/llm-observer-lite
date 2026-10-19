import uuid
import time
import random
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from .db import get_db_connection, init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database on startup
    init_db()
    yield
    # Perform any cleanup if necessary on shutdown
    pass

app = FastAPI(title="Multimodal PDF RAG API", version="1.0", lifespan=lifespan)

# Mount static frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

class LLMRequest(BaseModel):
    prompt: str = "Hello model"
    simulate_error: bool = False # Toggle to trigger deliberate failures

class LLMRequestModel(BaseModel):
    prompt: str
    model_name: str 
    simulate_error: bool = False


@app.post("/api/v1/infer")
def run_llm_inference(data: LLMRequestModel):
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Simulate deliberate failure if requested
        if data.simulate_error:
            time.sleep(0.2)
            raise Exception("Deliberate model timeout / context overflow failure.")
        
        # Simulate model inference latency (e.g., 0.5 to 1.5 seconds)
        simulated_latency = round(random.uniform(0.4, 1.4), 2)
        time.sleep(simulated_latency)
        
        duration = round(time.time() - start_time, 2)
        token_count = len(data.prompt.split()) * 3 # Mock token calculation
        
        # Log success
        cursor.execute("""
            INSERT INTO llm_logs (request_id, model_name, prompt, duration, status, token_count)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (request_id, data.model_name, data.prompt, duration, "SUCCESS", token_count))
        conn.commit()
        
        return {
            "request_id": request_id,
            "status": "SUCCESS",
            "duration": duration,
            "response": f"Processed prompt successfully using {data.model_name}."
        }

    except Exception as e:
        duration = round(time.time() - start_time, 2)
        error_msg = str(e)
        
        # Log failure
        cursor.execute("""
            INSERT INTO llm_logs (request_id, model_name, prompt, duration, status, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (request_id, data.model_name, data.prompt, duration, "ERROR", error_msg))
        conn.commit()
        
        raise HTTPException(status_code=500, detail=f"[{request_id}] Request Failed: {error_msg}")
    finally:
        conn.close()

@app.get("/api/v1/logs")
def get_logs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT request_id, timestamp, model_name, prompt, duration, status, token_count, error_message 
        FROM llm_logs 
        ORDER BY id DESC 
        LIMIT 25
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]