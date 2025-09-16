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

Output / Response JSON:  https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion.py
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
- Instead of messages, we use input field 
- Instructions field is basically the system role, setting the context for the LLM system.  

Output: ChatCompletion object with following guaranteed fields: 
text or json
- LLM Text as a 
"""

response = client.responses.create(
  model="gpt-4.1-mini",
  input="Tell me a three sentence bedtime story about a unicorn."
)


"""

<class 'openai.types.chat.chat_completion.ChatCompletion'> 
ChatCompletion(id='chatcmpl-Bqf5DJXxweSjWsYtyyFNgg9Idirnd', 
               choices=[
                   Choice(finish_reason='stop', index=0, logprobs=None, 
                            message=ChatCompletionMessage(content='The capital of France is Berlin.', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None)
                        )
                ], created=1751890679, model='gpt-4.1-mini-2025-04-14', object='chat.completion', 
                service_tier='default', system_fingerprint='fp_658b958c37', 
                usage=CompletionUsage(completion_tokens=7, prompt_tokens=34, total_tokens=41, 
                                      completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, 
                                                                                        rejected_prediction_tokens=0), 
                                                                                        prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)
                                    )
                )

"""