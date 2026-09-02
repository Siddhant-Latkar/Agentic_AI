import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():
    # Connect to MCP server
    client = MultiServerMCPClient(
        {
            "calculator": {
                "transport": "stdio",
                "command": "python",
                "args": ["server.py"],
            }
        }
    )

    # Get MCP tools
    tools = await client.get_tools()

    print("MCP tools available:")
    for tool in tools:
        print("-", tool.name)

    print("\nType a calculation.")
    print("Examples:")
    print("  add 10 20")
    print("  multiply 5 6")
    print("  greet Siddhant")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        parts = user_input.split()

        try:
            command = parts[0].lower()

            if command == "add" and len(parts) == 3:
                tool = next(t for t in tools if t.name == "add")

                result = await tool.ainvoke(
                    {
                        "a": float(parts[1]),
                        "b": float(parts[2]),
                    }
                )

            elif command == "multiply" and len(parts) == 3:
                tool = next(t for t in tools if t.name == "multiply")

                result = await tool.ainvoke(
                    {
                        "a": float(parts[1]),
                        "b": float(parts[2]),
                    }
                )

            elif command == "greet" and len(parts) >= 2:
                tool = next(t for t in tools if t.name == "greet")

                result = await tool.ainvoke(
                    {
                        "name": " ".join(parts[1:])
                    }
                )

            else:
                print("Invalid input.")
                continue

            print("Result:", result)

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    asyncio.run(main())