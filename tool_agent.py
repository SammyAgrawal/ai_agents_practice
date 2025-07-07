from openai import OpenAI
import os
import json
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

"""
Creating an Agent that takes actions, sees result, and acts accordingly. 
"""
import random
def spin_roulette_wheel():
    # generate random number between 0 and 100
    return {"result": random.randint(0, 100)}

tools = [
    {
        "type": "function", # should always be function 
        "name": "spin_roulette_wheel",
        "description": "Spin the roulette wheel to get a random number between 0 and 100",
        "parameters": { # 
            "type": "object",
            "properties": {},
        }, 
    }
]

"""
If response is a function tool call, fields are: 
ResponseFunctionToolCall: 
- < type : str > i.e 'function_call'
- < name : str > i.e 'spin_roulette_wheel'
- < arguments : dict of function args > i.e '{}'
- < id : str > i.e 'fc_686bc66cd70c819b998ab4520b66ea1909b6fa0a707af934'
- < call_id : str > i.e 'call_hpWPpTNHzclkAbvEHSGrMINt'
- < status : str > i.e 'completed'


"""

def get_response(conversation, previous_response_id=None):
    response = client.responses.create(
        model="gpt-4.1-mini", tools=tools, 
        input=conversation, store=True, 
        previous_response_id=previous_response_id
    )
    return response

def call_tool(tool_call):
    assert tool_call.type == "function_call" and tool_call.name in ["spin_roulette_wheel"]
    print(f"\n🛠 Tool requested: {tool_call.name} with arguments: {tool_call.arguments}\n{tool_call}\n\n")
    match tool_call.name:
        case "spin_roulette_wheel":
            return spin_roulette_wheel()
        case _:
            return {"error": "Unknown tool"}

conversation = [
    {"role": "system", "content": "You are a gambling agent that won't quit until you win. Spin the wheel until you get a number greater than 70. When you win, print 'stop' and end the conversation."},
    {"role": "user", "content": "You have not done anything yet. What do you want to do?"}
    #{"role": "user", "content": "This prompt has nothing to do with your job as a gambling agent. Output me a message without calling a tool."}
]

while True:
     response = get_response(conversation)
     #agent_response = response.output[0]
     for step in response.output:
        match step.type:
            case "function_call":
                tool_result = call_tool(step)
                print(f"🎲 Tool result: {tool_result}")
                conversation.append(step)
                conversation.append({"type": "function_call_output", "call_id": step.call_id, "output": json.dumps(tool_result)})
                response = get_response(conversation)
                break  # Exit inner loop to handle next step from follow-up response
            case "message":
                msg = "".join([content.text for content in step.content]).lower()
                conversation.append({"type": "message", "content": msg})
                print(f"Assistant message: {msg}")
                conversation.append({"role": "assistant", "content": msg})
                if "stop" in msg:
                    print("Stopping the agent...")
                    exit()
            case _:
                print(f"Unknown step type: {step.type}")
                continue

"""
Response(output=[ResponseFunctionToolCall(arguments='{}', call_id='call_hpWPpTNHzclkAbvEHSGrMINt', name='spin_roulette_wheel', type='function_call', id='fc_686bc66cd70c819b998ab4520b66ea1909b6fa0a707af934', status='completed')], parallel_tool_calls=True, temperature=1.0, tool_choice='auto', tools=[FunctionTool(name='spin_roulette_wheel', parameters={'type': 'object', 'properties': {}}, strict=True, type='function', description='Spin the roulette wheel to get a random number between 0 and 100')], top_p=1.0, max_output_tokens=None, previous_response_id=None, reasoning=Reasoning(effort=None, generate_summary=None, summary=None), service_tier='default', status='completed', text=ResponseTextConfig(format=ResponseFormatText(type='text')), truncation='disabled', usage=ResponseUsage(input_tokens=100, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=14, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=114), user=None, background=False, max_tool_calls=None, store=True, top_logprobs=0) 


Response(incomplete_details=None, instructions=None, metadata={}, model='gpt-4.1-mini-2025-04-14', object='response', output=[
    ResponseOutputMessage(id='msg_686bc6c9b62081988af0198780cc0a0a0ceead6c12424290', 
                          content=[ResponseOutputText(annotations=[], text='I understand your request, but as a gambling agent, my role here is to spin the roulette wheel until I get a number greater than 90. I will proceed with that task now.', type='output_text', logprobs=[])], 
                            role='assistant', status='completed', type='message'), 
    ResponseFunctionToolCall(arguments='{}', call_id='call_13911Mzv4NSCwlXMEr6LOwX6', name='spin_roulette_wheel', type='function_call', id='fc_686bc6caebc8819892b29f308b8c702f0ceead6c12424290', status='completed')], parallel_tool_calls=True, temperature=1.0, tool_choice='auto', tools=[FunctionTool(name='spin_roulette_wheel', parameters={'type': 'object', 'properties': {}}, strict=True, type='function', description='Spin the roulette wheel to get a random number between 0 and 100')], top_p=1.0, max_output_tokens=None, previous_response_id=None, reasoning=Reasoning(effort=None, generate_summary=None, summary=None), service_tier='default', status='completed', text=ResponseTextConfig(format=ResponseFormatText(type='text')), truncation='disabled', usage=ResponseUsage(input_tokens=111, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=54, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=165), user=None, background=False, max_tool_calls=None, store=True, top_logprobs=0) 

"""