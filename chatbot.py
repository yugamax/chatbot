import os
from groq import Groq
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import asyncio

load_dotenv()
client = Groq(api_key=os.getenv("gr_api_key"))

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/ping", methods=["GET", "HEAD"])
async def ping():
    await asyncio.sleep(0.1)
    return {"message": "server is running"}

@app.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    chat_hist = [
        {
            "role": "system",
            "content": "you are web3 helper bot"
        }
    ]

    try:
        while True:
            data = await websocket.receive_text()
            chat_hist.append({"role": "user", "content": data})

            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=chat_hist,
                    temperature=0.2,
                    max_tokens=512,
                )

                res = completion.choices[0].message.content
                chat_hist.append({"role": "assistant", "content": res})

                await websocket.send_text(res)

            except Exception as e:
                await websocket.send_text(f"Error: {str(e)}")

    except WebSocketDisconnect:
        print("Client disconnected")
        chat_hist=[]

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="127.0.0.1", port=port)
