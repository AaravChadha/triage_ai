from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

client = Groq()
MODEL = "llama-3.3-70b-versatile"


def test_connection():
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "Say 'Groq connection successful' and nothing else."}],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print(test_connection())
