import json
from fastapi import FastAPI, Form, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

SENTENCES_FILE = "sentences.json"
websocket_clients = []

def load_sentences() -> List[str]:
    try:
        with open(SENTENCES_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_sentences(sentences: List[str]):
    with open(SENTENCES_FILE, "w") as file:
        json.dump(sentences, file)

all_sentences: List[str] = []
save_sentences(all_sentences)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

async def notify_clients():
    sentences = load_sentences()
    # Group sentences in reverse order and reverse the order of boxes as well
    grouped_sentences = [sentences[i:i + 3][::-1] for i in range(0, len(sentences), 3)][::-1]
    data = {"boxes": grouped_sentences}

    for client in websocket_clients:
        try:
            await client.send_json(data)
        except Exception as e:
            print(f"Error sending data to client: {e}")
            websocket_clients.remove(client)

@app.post("/add-sentence")
async def add_sentence(sentence: str = Form(...)):
    global all_sentences
    all_sentences = load_sentences()
    all_sentences.append(sentence.strip())
    save_sentences(all_sentences)
    await notify_clients()
    return {"status": "success", "message": "Sentence added."}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)
    try:
        await notify_clients()
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if websocket in websocket_clients:
            websocket_clients.remove(websocket)
        await websocket.close()
