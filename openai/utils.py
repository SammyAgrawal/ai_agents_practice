from openai import OpenAI
import os
import json

def get_response(client, conversation, model="gpt-4.1-mini", tools=None, previous_response_id=None, store=True):
    response = client.responses.create(
        model=model, tools=tools, 
        input=conversation, store=store, 
        previous_response_id=previous_response_id
    )
    return response

def execute_code(code_str):
    """
    Executes the provided code string after user approval.
    Returns:
    - dict: Contains 'status' and optionally 'output' or 'rejection_reason'.
    """
    global exec_namespace
    print("The following code is requested to be executed:\n")
    print(code_str)
    approval = input("\nDo you approve executing this code? (yes/no): ").strip().lower()
    if approval != 'yes':
        reason = input("Why do you not want to execute this code? (Explain the issue to the assistant): ").strip()
        return {"status": "aborted", "rejection_reason": reason}
    try:
        exec_namespace = {}
        exec(code_str, {}, exec_namespace)
        output = exec_namespace.get('output', None)
        print(f"\nCode executed successfully. Output: {output}")
        return {"status": "success", "output": output}
    except Exception as e:
        print(f"\nAn error occurred during code execution: {e}")
        return {"status": "error", "error": str(e)}


"""
def unit_test(func_name, test_case, expected_output, namespace=None):
    namespace = namespace or globals()
    func = namespace[func_name]
    output = func(**test_case)
    if output == expected_output:
        return {"output": "Pass"}
    else:
        return {"output": "Fail"}
"""


"""
    {
        "type": "function",
        "name": "unit_test",
        "description": "Check whether a given function passes a specified test case. ",
        "parameters": {
            "type": "object",
            "properties": {
                "func_name" : dict(type='string', description='Name of function being tested' ),
                "test_case" : dict(type='object', description="A test case to assess function behavior"),
                "expected_output" : dict(type=["string", "number", "boolean", "object", "array", "null"], description='The correct output expected from the function'),
            },
            "required" : ["func_name", "test_case", "expected_output"],
            "additionalProperties": False
        }
    }
"""


"""
        case "unit_test":
            func, tc, eo = arguments.get('func_name'), arguments.get('test_case'), arguments.get('expected_output')
            if func and tc and eo:
                result = unit_test(func, tc, eo, namespace=exec_namespace)
            else:
                result = {"status" : "error", "description": "Missing arguments"}
"""