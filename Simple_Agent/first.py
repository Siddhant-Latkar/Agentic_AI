from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.tools import tool


# Initialize Groq model
model = ChatGroq(
    model="llama-3.3-70b-versatile"
)


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """Divide the first number by the second."""

    if b == 0:
        return "Error: Cannot divide by zero"

    return a / b


# Create agent
agent = create_agent(
    model=model,
    tools=[multiply, divide]
)


# Run agent
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is 15 multiplied by 8, then divided by 4?"
            }
        ]
    }
)


# Print final answer
print(result["messages"][-1].content)