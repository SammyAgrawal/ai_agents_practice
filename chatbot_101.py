from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

"""
The assistant role is reserved for the LLM's response. Meant for multi turn conversations / chatting
"""


print("Simulated conversation with LLM! Say 'done', 'stop', or 'end' to end the conversation.")

conversation = []

while True:
    user_input = input("You: ")
    if user_input.lower() in ["done", "stop", "end"]:
        break
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=conversation
    )
    answer = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": answer}) # LLM's own content as assistant role. 
    print(f"Assistant: {answer}")