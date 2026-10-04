from openai import AsyncOpenAI

from app.core.config import OPENAI_API_KEY


client = AsyncOpenAI(
    api_key=OPENAI_API_KEY
)


async def ask_ai(message: str):
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract only the product name from the user's question. "
                    "Return only the product name and nothing else."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    )

    return response.choices[0].message.content.strip()