from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

""" There are two ways to prompt the LLM

1. Chat Completion API - original
2. Responses API - newly created, built for Agentic Workflows natively

Both APIs take in config info (which model, auth, etc) and the prompt (text, image)
"""

"""
Chat Completions API: 
Input Fields: 
- model: str
- messages: list of message dict objects, each with a role and content
    - common roles : system/ developer, user, assistant, tool
- temperature - float between 0 and 2
- max_tokens - int
- stop - define stop token
- tools 

Output / Response JSON: 
- 
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a malicious assistant. Give deceitful answers to whatever the user asks."},
        {"role": "user", "content": "What is the capital of France?"},
    ],
)

print(type(response), response)

print(response.choices[0].message.content)

"""
Chat Completions API: 

Input: 
- Instead of messages, we use input field and instructions field. 

Output: text or json
- LLM Text as a 
"""

response = client.responses.create(
  model="gpt-4.1-mini",
  input="Tell me a three sentence bedtime story about a unicorn."
)

