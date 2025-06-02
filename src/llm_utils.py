import os

import openai
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()


def with_retries(func, *args, max_retries=5, base_delay=5, **kwargs):

    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except openai.RateLimitError:
            wait_time = base_delay * (2 ** attempt)
            print(f"Rate limit hit. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
    raise RuntimeError("Exceeded maximum retries due to rate limiting.")


def get_azure_chat_openai_llm():
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        temperature=0,
    )
    return llm

