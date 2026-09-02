import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


messages=[]
while True:
    user_input=input("You:-")
    
    if user_input.lower() == "exit":
        print("bye bye...")
        break

    messages.append({
        "role":"user",
        "content":user_input
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )
    messages.append({
        "role":"assistant",
        "content":"response.choices[0].message.content"
    })
    print(response.choices[0].message.content)
    
#response API code using built-in tools
"""
    
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


messages=[]
while True:
    user_input=input("You:-")
    
    if user_input.lower() == "exit":
        print("bye bye...")
        break

    messages.append({
        "role":"user",
        "content":user_input
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        tools=[{"type":"browser_search"}],
        messages=messages
    )
    messages.append({
        "role":"assistant",
        "content":"response.choices[0].message.content"
    })
    print(response.choices[0].message.content)
    """
    