from openai import AsyncOpenAI
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse


# https://danielcorin.com/posts/2024/lm-streaming-with-sse/


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
        yield f"data: {chunk.choices[0].delta.content or ''}\n\n"
    yield f"data: [DONE]\n\n"


@app.get("/ask")
async def main(msg):
    return StreamingResponse(generator(msg), media_type="text/event-stream")


@app.get("/")
async def get_index():
    return FileResponse("index.html")