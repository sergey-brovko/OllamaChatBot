import os
from kafka import KafkaConsumer
import json
import requests
import redis
import logging

MODEL = 'hf.co/Vikhrmodels/Vikhr-Llama-3.2-1B-instruct-GGUF:F16'
# MODEL = "deepseek-r1:1.5b"
OLLAMA_API = os.getenv('OLLAMA_API')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)



r = redis.Redis(host='redis', port=6379, db=0)

consumer = KafkaConsumer(
    'requests',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)


for message in consumer:
    try:
        data = message.value
        request_id = data['id']
        prompt = data['prompt']

        response = requests.post(
            "http://ollama:11434/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        result = response.json()['response']
        r.set(request_id, json.dumps({"status": "completed", "result": result}))
    except Exception as e:
        r.set(request_id, json.dumps({"status": "error", "result": str(e)}))