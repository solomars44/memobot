from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize conversation memory
memory = ConversationBufferMemory()
llm = None
conversation = None

class ChatRequest(BaseModel):
    message: str
    model: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: ChatRequest):
    global llm, conversation
    
    try:
        # Initialize or update LLM if model changes
        if llm is None or llm.model != request.model:
            llm = Ollama(model=request.model)
            conversation = ConversationChain(
                llm=llm,
                memory=memory,
                verbose=True
            )
        
        # Get response from conversation chain
        response = conversation.predict(input=request.message)
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def get_models():
    try:
        response = requests.get('http://localhost:11434/api/tags')
        if response.ok:
            data = response.json()
            return {"models": [model["name"] for model in data.get("models", [])]}
        return {"models": []}
    except:
        return {"models": []}