# summary_service.py
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

    Generate a structured summary using this format:

    Overview:
    (2-3 sentences)

    Key Points:
    • Point 1
    • Point 2
    • Point 3

    Important Information:
    • Item 1
    • Item 2

    Keep it under 150 words.

    Document:

    {text[:3000]}
    """

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        # except Exception:

        #     return (
        #         "⚠ AI Summary is temporarily unavailable because "
        #         "the Gemini API quota has been reached."
        #     )
        except Exception as e:

            print("=" * 50)
            print("SUMMARY ERROR")
            print(e)
            print("=" * 50)

            return (
                "⚠ AI Summary is temporarily unavailable because "
                "the Gemini API quota has been reached."
            )