from fastapi import FastAPI, HTTPException, Response, status
from fastapi.openapi.utils import status_code_ranges
from pydantic import BaseModel
import uuid
import json
from kafka import KafkaProducer
import redis

app = FastAPI()

# Redis connection
r = redis.Redis(host='redis', port=6379, db=0)

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate(prompt_request: PromptRequest):
    request_id = str(uuid.uuid4())
    r.set(request_id, json.dumps({"status": "processing", "result": None}))
    producer.send('requests', {'id': request_id, 'prompt': prompt_request.prompt})
    return {"request_id": request_id}

@app.get("/result/{request_id}", status_code=200)
async def get_result(request_id: str, response: Response):
    data = r.get(request_id)

    if not data:
        raise HTTPException(status_code=404, detail="Request not found")
    data = json.loads(data)
    if not data.get('result'):
        response.status_code = status.HTTP_204_NO_CONTENT
    return data