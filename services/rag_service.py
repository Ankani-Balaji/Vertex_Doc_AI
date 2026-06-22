# rag_service.py
import os
import requests
import numpy as np

from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS


VECTOR_ROOT = "vector_store"

class HuggingFaceAPIEmbeddings(Embeddings):

    def embed_documents(self, texts):
        return [self._embed(t) for t in texts]

    def embed_query(self, text):
        return self._embed(text)

    def _embed(self, text):
        response = requests.post(
            "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2",
            headers={"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"},
            json={"inputs": text, "options": {"wait_for_model": True}}
        )
        result = response.json()
        arr = np.array(result)
        if arr.ndim == 2:
            arr = arr.mean(axis=0)
        return arr.tolist()


embedding_model = HuggingFaceAPIEmbeddings()


class RAGService:

    @staticmethod
    def create_vector_store(text, session_id):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )


        chunks = splitter.split_text(text)

        if not chunks:
            return 0


        vector_store = FAISS.from_texts(
            texts=chunks,
            embedding=embedding_model
        )

        session_path = os.path.join(
            VECTOR_ROOT,
            session_id
        )

        os.makedirs(session_path, exist_ok=True)

        vector_store.save_local(session_path)

        return len(chunks)

    @staticmethod
    def load_vector_store(session_id):

        session_path = os.path.join(
            VECTOR_ROOT,
            session_id
        )

        if not os.path.exists(session_path):
            return None

        return FAISS.load_local(
            session_path,
            embedding_model,
            allow_dangerous_deserialization=True
        )

    @staticmethod
    def search(question, session_id):

        db = RAGService.load_vector_store(session_id)

        if db is None:
            return []

        docs = db.similarity_search_with_score(
            question,
            k=3
        )

        return docs