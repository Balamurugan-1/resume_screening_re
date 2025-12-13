import os
import numpy as np
import google.generativeai as genai
import dotenv

dotenv.load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

EMBEDDING_MODEL = "models/text-embedding-004"
MAX_CHARS = 6000

def get_embedding(text: str) -> np.ndarray:
    if not text or not text.strip():
        raise ValueError("Empty text")

    text = text[:6000]

    try:
        response = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text
        )
        return np.array(response["embedding"], dtype=np.float32)
    except Exception as e:
        raise RuntimeError(f"Embedding failed: {str(e)}")

print("GOOGLE_API_KEY loaded:", bool(os.getenv("GOOGLE_API_KEY")))

