#chat_service.py

import os

from dotenv import load_dotenv
from google import genai

from services.rag_service import RAGService

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


class ChatService:

    @staticmethod
    def ask_question(question, session_id):

        docs = RAGService.search(
            question,
            session_id
        )

        if not docs:
            return "No document has been uploaded."

        # Lowest score is best
        best_score = docs[0][1]

        print("=" * 50)
        print(f"Question : {question}")
        print(f"Similarity Score : {best_score}")
        print("=" * 50)

        if best_score > 2.0:

            return (
                "Sorry, I couldn't find relevant information "
                "in the uploaded document. "
                "Please ask a question based on the uploaded PDF."
            )

        context = "\n\n".join(
            [doc.page_content for doc, score in docs]
        )

        prompt = f"""
        You are VertexDoc AI Assistant.

        Use ONLY the document context below.

        Rules:

        1. Answer ONLY from the provided context.
        2. Never use external knowledge.
        3. Never guess.
        4. Never make assumptions.
        5. If the answer is missing or incomplete,
        reply exactly:

        Sorry, I couldn't find relevant information in the uploaded document. Please ask a question based on the uploaded PDF.

        Document Context:

        {context}

        User Question:

        {question}

        Answer:
        """

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            print("=" * 50)
            print("CHAT ERROR")
            print(e)
            print("=" * 50)

            return (
                "⚠️ AI service is temporarily unavailable."
            )