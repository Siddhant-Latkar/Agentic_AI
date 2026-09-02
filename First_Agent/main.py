import os
from dotenv import load_dotenv

#----------------------
#Step 1:load enviroment variables
#----------------------

load_dotenv()

#----------------------
#Step 2:Initialize the model(the "brain")
#----------------------
from langchain_groq import ChatGroq

# Initialize Groq model
model = ChatGroq(
    model="llama-3.1-8b-instant",
  
)

#----------------------
#Step 3:Define Tools(the "hands")
#----------------------

from langchain_core.tools import tool


@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@tool
def sub(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@tool
def division(a: float, b: float) -> float:
    """Divide a by b."""

    if b == 0:
        return "Error: Cannot divide by zero"

    return a / b

#Combine all tools into a list
tools=[add,sub,multiply,division]

#Print available tools 
print("====Available Tools====")
for t in tools:
    print(f" {t.name} = {t.description}")

print()

#----------------------
#Step 4:Create Agent(the "loops")
#----------------------

from langchain.agents import create_agent

agent=create_agent(
    model=model,
    tools=tools
)



#----------------------
#Step 5:Run the Agent
#----------------------

def run_agent(question:str):
    """Run the agent and print a clean,beginner-friendly trace."""
    
    print("-"*60)
    print(f"\n User:-{question}")
    print("-"*60)
    
    result=agent.invoke({
        "messages":[("user",question)]
    })
    
    print("Clean user execution trace")
    print("-"*60)
    
    for message in result["messages"]:
        #show tool calls
        if  hasattr(message,"tool_calls") and message.tool_calls:
            
            for tool_call in message.tool_calls:
                print("Tool used:-",tool_call["name"])
                print("Arguments:-",tool_call["args"])
                
        
        #show tool result
        if message.type=="tool":
            print("Tool Result",message.content)
            
        #show final answer
    print("\n =====Final Answer=====")
        
    final_answer=result["messages"][-1].content
        
    print("Agent:-",final_answer)


#----------------------
#Step 6:user input
#----------------------

question=input("You:-")
run_agent(question)