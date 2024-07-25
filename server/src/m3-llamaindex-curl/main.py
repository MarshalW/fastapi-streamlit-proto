from fastapi import FastAPI
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings
from fastapi.responses import StreamingResponse

from pydantic import BaseModel

app = FastAPI()

Settings.llm = OpenAILike(
    model="qwen2-7b-6k",
    api_base="http://ape:3000/v1",
    api_key="sk-bJP6QSnUfjAYeYeE505d3eBf63A643BeB0B8E350Df9b7750",
    is_chat_model=True,
    temperature=0.1,
    request_timeout=60.0
)
Settings.embed_model = OllamaEmbedding(
    model_name="quentinz/bge-large-zh-v1.5",
    base_url="http://ape:11435",
    ollama_additional_kwargs={"mirostat": 0},
)

documents = SimpleDirectoryReader(input_files=["./data/孔乙己.txt"]).load_data()
index = VectorStoreIndex.from_documents(documents=documents)
query_engine = index.as_query_engine(
    streaming=True,
    similarity_top_k=3
)

class QueryRequest(BaseModel):
    query: str = "孔乙己是谁"


@app.post("/query")
async def query_index(request: QueryRequest):
    print(request.query)
    results = query_engine.query(request.query)
    return StreamingResponse(results.response_gen, media_type="text/event-stream")


# curl -N -X POST  \
#  -H "Content-Type: application/json" \
#  -H "accept: text/event-stream" \
#  -d '{"query":"回字有几种写法？\n"}' \
#  http://127.0.0.1:7777/query
