import functools
import os
import time

import openai
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()


def retry_on_rate_limit(max_retries=5, base_delay=5):
    """
    Decorator to retry a function on OpenAI RateLimitError.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except openai.RateLimitError:
                    wait_time = base_delay * (2 ** attempt)
                    print(f"Rate limit hit. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
            raise RuntimeError("Exceeded maximum retries due to rate limiting.")

        return wrapper

    return decorator


def get_azure_chat_openai_llm():
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        temperature=0,
    )
    return llm
