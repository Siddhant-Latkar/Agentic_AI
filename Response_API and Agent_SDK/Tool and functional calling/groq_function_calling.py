import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")

client = Groq(api_key=api_key)


# ============================================================
# 1. PYTHON FUNCTIONS - ACTUAL TOOLS
# ============================================================

def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


# ============================================================
# 2. TOOL DEFINITIONS SENT TO THE MODEL
# ============================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiply two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "subtract",
            "description": "Subtract the second number from the first number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"],
                "additionalProperties": False
            }
        }
    }
]


# ============================================================
# 3. TOOL DISPATCHER
# ============================================================

def execute_tool(tool_name: str, arguments: str):
    args = json.loads(arguments)

    if tool_name == "add":
        return add(args["a"], args["b"])

    elif tool_name == "multiply":
        return multiply(args["a"], args["b"])

    elif tool_name == "subtract":
        return subtract(args["a"], args["b"])

    else:
        raise ValueError(f"Unknown tool: {tool_name}")


# ============================================================
# 4. CHAT LOOP
# ============================================================

messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful assistant. "
            "Use the available tools whenever calculation is required."
        )
    }
]


while True:

    user_input = input("\nYou:- ")

    if user_input.lower() == "exit":
        print("bye bye...")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    # --------------------------------------------------------
    # MODEL ↔ TOOL LOOP
    # --------------------------------------------------------

    while True:

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        # ----------------------------------------------------
        # NO TOOL CALL -> FINAL ANSWER
        # ----------------------------------------------------

        if not assistant_message.tool_calls:

            print("AI:-", assistant_message.content)

            messages.append({
                "role": "assistant",
                "content": assistant_message.content
            })

            break

        # ----------------------------------------------------
        # TOOL CALL FOUND
        # ----------------------------------------------------

        messages.append({
            "role": "assistant",
            "content": assistant_message.content,
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                }
                for tool_call in assistant_message.tool_calls
            ]
        })

        # Execute every requested tool
        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            print(f"\n[Tool requested] {tool_name}")
            print(f"[Arguments] {arguments}")

            result = execute_tool(
                tool_name,
                arguments
            )

            print(f"[Tool result] {result}")

            # Send result back to model
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": str(result)
            })