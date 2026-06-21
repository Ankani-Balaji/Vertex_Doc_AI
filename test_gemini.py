from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say Hello"
    )

    print(response.text)

except Exception as e:
    print(type(e))
    print(e)