import os
import sys
import asyncio
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# STEP 1: INITIALIZE GROQ MODEL
# ============================================================

from langchain_groq import ChatGroq

model = ChatGroq(
    model="llama-3.1-8b-instant"
)


# ============================================================
# STEP 2: MCP CLIENT
# ============================================================

from langchain_mcp_adapters.client import MultiServerMCPClient


async def run_agent(question: str):

    # --------------------------------------------------------
    # Connect to MCP Server
    # --------------------------------------------------------

    client = MultiServerMCPClient(
        {
            "math": {
                "command": sys.executable,
                "args": [
                    os.path.abspath("main_server.py")
                ],
                "transport": "stdio",
            }
        }
    )


    # --------------------------------------------------------
    # Get tools from MCP Server
    # --------------------------------------------------------

    tools = await client.get_tools()


    # --------------------------------------------------------
    # Display available MCP tools
    # --------------------------------------------------------

    print("\n==== Available MCP Tools ====")

    for tool in tools:
        print(
            f"{tool.name} = {tool.description}"
        )

    print()


    # ========================================================
    # STEP 3: CREATE LANGCHAIN AGENT
    # ========================================================

    from langchain.agents import create_agent

    agent = create_agent(
        model=model,
        tools=tools
    )


    # ========================================================
    # STEP 4: RUN AGENT
    # ========================================================

    print("-" * 60)
    print(f"User:- {question}")
    print("-" * 60)


    result = await agent.ainvoke(
        {
            "messages": [
                ("user", question)
            ]
        }
    )


    # ========================================================
    # STEP 5: SHOW EXECUTION TRACE
    # ========================================================

    print("\n===== MCP Execution Trace =====")
    print("-" * 60)


    for message in result["messages"]:

        # ----------------------------------------------------
        # Show tool calls
        # ----------------------------------------------------

        if hasattr(message, "tool_calls") and message.tool_calls:

            for tool_call in message.tool_calls:

                print(
                    "Tool used:-",
                    tool_call["name"]
                )

                print(
                    "Arguments:-",
                    tool_call["args"]
                )


        # ----------------------------------------------------
        # Show tool result
        # ----------------------------------------------------

        if message.type == "tool":

            print(
                "Tool Result:-",
                message.content
            )


    # ========================================================
    # STEP 6: FINAL ANSWER
    # ========================================================

    print("\n===== Final Answer =====")

    final_answer = result["messages"][-1].content

    print("Agent:-", final_answer)


# ============================================================
# STEP 7: USER INPUT
# ============================================================

if __name__ == "__main__":

    question = input("You:- ")

    asyncio.run(
        run_agent(question)
    )