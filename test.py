# test.py
import os
import requests
import numpy as np
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

print(f"HF_API_KEY loaded: {HF_API_KEY[:10]}..." if HF_API_KEY else "HF_API_KEY is MISSING")

response = requests.post(
    "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2",
    headers={"Authorization": f"Bearer {HF_API_KEY}"},
    json={"inputs": "test sentence", "options": {"wait_for_model": True}}
)

print(f"Status code: {response.status_code}")
print(f"Response: {response.json()}")