from openai import AsyncOpenAI
from fastapi import FastAPI
from fastapi.responses import StreamingResponse


app = FastAPI()
client = AsyncOpenAI(
    base_url='http://ape:3000/v1',
    api_key='sk-bJP6QSnUfjAYeYeE505d3eBf63A643BeB0B8E350Df9b7750',
)


async def generator(msg: str):
    stream = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": msg,
            }
        ],
        model="qwen2-7b-6k",
        stream=True,
    )

    async for chunk in stream:
        yield chunk.choices[0].delta.content or ''


@app.get("/ask")
async def main(msg):
    return StreamingResponse(generator(msg))




# curl "localhost:7777/ask?msg=who%20are%20you"