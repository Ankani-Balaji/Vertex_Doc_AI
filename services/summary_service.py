import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


class SummaryService:

    @staticmethod
    def generate_summary(text):

        if not text:
            return "No content available."

        prompt = f"""
You are an intelligent document assistant.

Generate a professional summary of the following document.

Rules:
- Maximum 150 words
- Use simple English
- Mention the main purpose
- Mention important topics
- Do not invent information

Document:

{text[:12000]}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text