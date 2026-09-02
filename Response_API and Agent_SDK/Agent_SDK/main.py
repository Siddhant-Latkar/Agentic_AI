import os
import asyncio

from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI


# ============================================================
# 1. Load environment variables
# ============================================================

load_dotenv()


# ============================================================
# 2. Create Groq client
# ============================================================

groq_client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# ============================================================
# 3. Create Groq model
# ============================================================

model = OpenAIChatCompletionsModel(
    model="llama-3.1-8b-instant",
    openai_client=groq_client
)


# ============================================================
# 4. Define an Agent
# ============================================================

agent = Agent(
    name="Quick Helper",
    instructions="Give very brief, one-sentence answers.",
    model=model
)


# ============================================================
# 5. Run the Agent
# ============================================================

async def main():

    result = await Runner.run(
        agent,
        "When did humans land on the moon?"
    )

    print(result.final_output)


# ============================================================
# 6. Start the program
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())