from openai import OpenAI
import os
import json
import inspect
from utils import get_response, execute_code
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    
def buggy_function(nums1, nums2):
    odds = [nums1[i] for i in range(0, len(nums1), 2)]
    evens = [nums2[i] for i in range(0, len(nums1), 2)]
    res = 0
    for i in range(min(len(odds), len(evens))):
        res += odds[i] + evens[i]
    return res

tools = [
    { # type, name, description, and parameters are main fields
        "type": "function",
        "name": "execute_code",
        "description": "Executes Python code. Returns json output with status (either success, error, or aborted by user) and output fields. Always assign whatever info you want to persist in the variable 'output'. You can edit the buggy_function code by submitting a modified version using the execute_code tool.",
        "parameters": { # type, properties, required, additionalProperties are main fields
            "type": "object",
            "properties": {
                "code_str": dict(type='string', description='The Python code to execute, with local output variable assigned to persistent info.')},
            "required": ["code_str"], "additionalProperties": False
            }
    }, 
]

def call_tool(tool_call, conversation):
    assert tool_call.type == "function_call" and tool_call.name in ["execute_code", "unit_test"]
    print(f"\n🛠 Tool requested: {tool_call.name} with arguments: {tool_call.arguments}\n\n")
    conversation.append(tool_call)
    arguments = json.loads(tool_call.arguments)
    match tool_call.name:
        case "execute_code":
            code_str = arguments.get('code_str')
            result = execute_code(code_str) if code_str else {"status" : "error", "description": "Missing code_str"}
            if result.get("status") == "aborted":
                rejection_reason = result.get("rejection_reason", "User declined to run the code without explanation. Try to fix it.")
                conversation.append(dict(role="user", content=f"I did not run the last code because: {rejection_reason}. Please revise the code and try again."))
                return conversation
        case _:
            return {"error": "Unknown tool"}
    conversation.append(dict(type="function_call_output", call_id=tool_call.call_id, output=json.dumps(result)))
    return conversation



high_level_msg = """
You are a coding agent that is trying to debug faulty code. You have a execute_code function that allows you to run code and see its output. 
Never simulate or pretend to run code. Always use the `execute_code` tool to run Python code. 
Never reply with code outputs directly in a message. Use the tool.
Output stop when code is deemed correct or fixed.
"""

instruction = f"""
Here is my function: {inspect.getsourcelines(buggy_function)}.
It is meant to take two list of numbers (nums1 and num2) and add the odd-index items of nums1 with the even-index of nums2.
Ignore excess values of the longer list. 
My implementation is buggy, can you run the code with inputs [1,2,3,4,5] and [1,2,3,4,5] and see what it outputs?
Use the execute_code tool to run the code. Make sure to output stop or done when the code is correct! I only want a version with correct output. 
"""


conversation = [
    {"role": "system", "content": high_level_msg},
    {"role": "user", "content": instruction}
]

while True:
     user_message = input("end? (y/n) ")
     if user_message == "y":
          break
     conversation.append({"role": "user", "content": user_message})
     response = get_response(client, conversation, tools=tools)
     #agent_response = response.output[0]
     for step in response.output:
        match step.type:
            case "function_call":
                conversation = call_tool(step, conversation)
                response = get_response(client, conversation, tools=tools)
                break  # Exit inner loop to handle next step from follow-up response
            case "message":
                msg = "".join([content.text for content in step.content]).lower()
                print(f"Assistant message: {msg}\n\n")
                conversation.append({"role": "assistant", "content": msg})
                if "stop" in msg or "done" in msg:
                    print("Stopping the agent...")
                    exit()
            case _:
                print(f"Unknown step type: {step.type}")
                continue