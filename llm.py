# utils/llm.py

import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# GET API KEY
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if not GROQ_API_KEY:

    raise RuntimeError(
        "GROQ_API_KEY is not configured. "
        "Please add GROQ_API_KEY to your .env file."
    )


# ============================================================
# SHARED LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=GROQ_API_KEY,
)
