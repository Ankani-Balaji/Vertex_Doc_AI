import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


class QuestionService:

    @staticmethod
    def generate_questions(text):

        if not text:
            return []

        prompt = f"""
Generate exactly 4 short questions that a user might ask after reading this document.

Rules:
- Return only the questions.
- One question per line.
- Maximum 12 words each.

Document:

{text[:8000]}
"""

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return [
                line.replace("-", "").strip()
                for line in response.text.split("\n")
                if line.strip()
            ]

        except Exception:

            return [

                "What is this document about?",

                "Give a brief summary.",

                "What are the important points?",

                "What are the key takeaways?"

            ]

            

        questions = []

        for line in response.text.split("\n"):

            line = line.strip()

            if line:

                line = line.replace("-", "")
                line = line.replace("*", "")
                line = line.strip()

                questions.append(line)

        return questions[:4]