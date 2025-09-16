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
If response step (in outputs list) is a function tool call, fields are: 
ResponseFunctionToolCall: 
- < type : str > i.e 'function_call'
- < name : str > i.e 'spin_roulette_wheel'
- < arguments : dict of function args > i.e '{}'
- < id : str > i.e 'fc_686bc66cd70c819b998ab4520b66ea1909b6fa0a707af934'
- < call_id : str > i.e 'call_hpWPpTNHzclkAbvEHSGrMINt'
- < status : str > i.e 'completed'

If response step is message, important fields are: 
- <content, List[ResponseOutputText] > with ResponseOutputText.text being the message text. ResponseOutputText.type is 'output_text'
- role : assistant
ResponseOutputMessage(id='msg_686bc6c9b62081988af0198780cc0a0a0ceead6c12424290', 
                          content=[(annotations=[], text='I understand your requestt task now.', type='output_text', logprobs=[])], 
                            role='assistant', status='completed', type='message'),  


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
            result = spin_roulette_wheel()
            print(f"🎲 Tool result: {tool_result}")
        case _:
            return {"error": "Unknown tool"}
    return {
        "type": "function_call_output", 
        "call_id": tool_call.call_id, 
        "output": json.dumps(result)
    }

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
                conversation += [step, tool_result]
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
