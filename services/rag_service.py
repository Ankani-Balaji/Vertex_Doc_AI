import os
import pickle

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

VECTOR_PATH = "vector_store"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


class RAGService:

    @staticmethod
    def create_vector_store(text):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_text(text)

        vector_store = FAISS.from_texts(
            texts=chunks,
            embedding=embedding_model
        )

        os.makedirs(VECTOR_PATH, exist_ok=True)

        vector_store.save_local(VECTOR_PATH)

        return len(chunks)

    @staticmethod
    def load_vector_store():

        if not os.path.exists(VECTOR_PATH):
            return None

        return FAISS.load_local(
            VECTOR_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )

    @staticmethod
    def search(question):

        db = RAGService.load_vector_store()

        if db is None:
            return []

        docs = db.similarity_search(question, k=4)

        return docs