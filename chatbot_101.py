from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

"""
The assistant role is reserved for the LLM's response. Meant for multi turn conversations / chatting
"""

