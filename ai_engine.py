from google import genai
from google.genai.errors import ServerError, APIError
import time

client = genai.Client()

def generate_response(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    # Model overloaded (503)
    except ServerError:
        return "__SERVER_BUSY__"

    # Bad request / quota / auth etc
    except APIError:
        return "__API_ERROR__"

    # Network / unknown crash
    except Exception:
        return "__UNKNOWN_ERROR__"
