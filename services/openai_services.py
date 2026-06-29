# from openai import OpenAI
# from openai import OpenAI
# from config import OPENAI_API_KEY 
# from config import MODEL

# client = OpenAI(api_key=OPENAI_API_KEY)

# def get_completion(prompt):
#     response = client.chat.completions.create(
#     model=MODEL,
#     messages=[{"role": "user", "content": prompt}]
#     )

#     return response.choices[0].message.content


 



import logging

from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError, APIStatusError
from config import OPENAI_API_KEY, MODEL

logger = logging.getLogger(__name__)

if not OPENAI_API_KEY:
     raise EnvironmentError("OPENAI_API_KEY is not set. Please add it to your .env file.")

Client = OpenAI(api_key=OPENAI_API_KEY)


def get_completion(prompt: str) -> str:
    """Send a prompt to OpenAI and return the response text."""

    logger.debug(f"Sending prompt to model '{MODEL}' (length: {len(prompt)} chars)")

    try:
         response = Client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        
         result = response.choices[0].message.content
         logger.debug(f"Received response (length: {len(result)} chars)")

         return result

    except AuthenticationError:
        logger.error("OpenAI Authentication failed — check your OPENAI_API_KEY.")
        
        raise ValueError("Invalid OpenAI API key. Please check your .env file.")

    except RateLimitError:
        logger.error("OpenAI rate limit exceeded.")
        
        raise ValueError("OpenAI rate limit reached. Please wait a moment and try again.")

    except APIConnectionError as e:
        logger.error(f"Network error connecting to OpenAI: {e}")
        
        raise ValueError("Could not connect to OpenAI. Please check your internet connection.")

    except APIStatusError as e:
        logger.error(f"OpenAI API error {e.status_code}: {e.message}")

        raise ValueError(f"OpenAI API error ({e.status_code}): {e.message}")

    except Exception as e:
        logger.exception(f"Unexpected error in get_completion: {e}")
        raise


