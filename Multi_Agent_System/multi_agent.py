import os
import json

from groq import Groq
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-120b"


# ============================================================
# SPECIALIST AGENTS
# ============================================================

def math_agent(user_query: str) -> str:

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the Math Specialist Agent. "
                    "Solve mathematical problems accurately. "
                    "Show the important calculation steps briefly."
                )
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

    return response.choices[0].message.content


def general_agent(user_query: str) -> str:

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the General Knowledge Specialist Agent. "
                    "Answer general questions clearly and professionally."
                )
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

    return response.choices[0].message.content


def writer_agent(user_query: str) -> str:

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the Writing Specialist Agent. "
                    "Help the user write, rewrite, summarize, "
                    "or improve content in a clear professional style."
                )
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

    return response.choices[0].message.content


# ============================================================
# HANDOFF FUNCTIONS
# ============================================================

def handoff_to_math_agent(query: str) -> str:
    print("\n[HANDOFF] Router -> Math Agent")
    return math_agent(query)


def handoff_to_general_agent(query: str) -> str:
    print("\n[HANDOFF] Router -> General Agent")
    return general_agent(query)


def handoff_to_writer_agent(query: str) -> str:
    print("\n[HANDOFF] Router -> Writer Agent")
    return writer_agent(query)


# ============================================================
# HANDOFF TOOL DEFINITIONS
# ============================================================

handoff_tools = [
    {
        "type": "function",
        "function": {
            "name": "handoff_to_math_agent",
            "description": (
                "Transfer the user's request to the Math Specialist "
                "when the request involves mathematics, arithmetic, "
                "equations, calculations, or numerical reasoning."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The complete user request to transfer."
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "handoff_to_general_agent",
            "description": (
                "Transfer the user's request to the General Knowledge "
                "Specialist for general questions, explanations, "
                "concepts, technology, science, or other knowledge."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The complete user request to transfer."
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "handoff_to_writer_agent",
            "description": (
                "Transfer the user's request to the Writing Specialist "
                "for writing, rewriting, emails, summaries, captions, "
                "or professional content."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The complete user request to transfer."
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    }
]


# ============================================================
# HANDOFF DISPATCHER
# ============================================================

def execute_handoff(tool_name: str, arguments: str) -> str:

    args = json.loads(arguments)

    query = args["query"]

    if tool_name == "handoff_to_math_agent":
        return handoff_to_math_agent(query)

    if tool_name == "handoff_to_general_agent":
        return handoff_to_general_agent(query)

    if tool_name == "handoff_to_writer_agent":
        return handoff_to_writer_agent(query)

    raise ValueError(f"Unknown handoff: {tool_name}")


# ============================================================
# ROUTER AGENT
# ============================================================

def router_agent(user_query: str) -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "You are the Router Agent in a multi-agent system.\n\n"

                "Your job is NOT to solve the user's request.\n"
                "Your job is to select the most appropriate specialist "
                "and hand off the request.\n\n"

                "Use exactly one handoff tool:\n"
                "- Math Agent for mathematics and calculations\n"
                "- General Agent for general knowledge and explanations\n"
                "- Writer Agent for writing and rewriting\n\n"

                "Transfer the user's complete request to the specialist."
            )
        },
        {
            "role": "user",
            "content": user_query
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=handoff_tools,
        tool_choice="required"
    )

    message = response.choices[0].message

    if not message.tool_calls:
        return "Router did not select a specialist."

    # We expect one handoff
    tool_call = message.tool_calls[0]

    print(f"\n[ROUTER] Selected: {tool_call.function.name}")

    result = execute_handoff(
        tool_call.function.name,
        tool_call.function.arguments
    )

    return result


# ============================================================
# MAIN CHAT LOOP
# ============================================================

def main():

    print("======================================")
    print("     GROQ MULTI-AGENT SYSTEM")
    print("======================================")
    print("Agents:")
    print("1. Math Agent")
    print("2. General Agent")
    print("3. Writer Agent")
    print("\nType 'exit' to quit.")

    while True:

        user_input = input("\nYou:- ").strip()

        if user_input.lower() == "exit":
            print("bye bye...")
            break

        try:

            answer = router_agent(user_input)

            print("\nFinal Answer:")
            print(answer)

        except Exception as e:

            print("\nError:")
            print(e)


if __name__ == "__main__":
    main()