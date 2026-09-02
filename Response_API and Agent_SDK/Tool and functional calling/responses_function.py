import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

messages = []

while True:
    user_input = input("You:- ")

    if user_input.lower() == "exit":
        print("bye bye...")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages
    )

    assistant_message = response.choices[0].message.content

    messages.append({
        "role": "assistant",
        "content": assistant_message
    })

    print("AI:-", assistant_message)