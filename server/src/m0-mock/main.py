from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn
from pydantic import BaseModel
import asyncio

app = FastAPI()

class StreamRequest(BaseModel):
    query: str

async def send_token(query: str):
    for token in query:
        yield token
        await asyncio.sleep(0.1)

@app.post("/streaming")
async def ask_stream(request: StreamRequest) -> StreamingResponse:
    return StreamingResponse(
        send_token(request.query),
        media_type="text/event-stream",
    )


# curl -N -X POST  \
#  -H "Content-Type: application/json" \
#  -H "accept: text/event-stream" \
#  -d '{"query":"你都知道些啥？\n"}' \
#  http://127.0.0.1:7777/streaming