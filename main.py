from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

# serve static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

messages = [
    {"id": 1, "sender": "paypal-support@fake.com", "subject": "Your account is locked!", "label": "phish"},
    {"id": 2, "sender": "friend@pumpkincafe.com", "subject": "Free Pumpkin Latte for Halloween!", "label": "treat"},
    {"id": 3, "sender": "admin@spookybank.com", "subject": "Verify your login or lose access", "label": "phish"},
    {"id": 4, "sender": "witch@halloweenstore.com", "subject": "20% off costumes this weekend!", "label": "treat"},
]

score = 0
current_message = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    global current_message
    current_message = random.choice(messages)
    return templates.TemplateResponse("index.html", {"request": request, "message": current_message, "score": score})

@app.post("/guess", response_class=HTMLResponse)
async def guess(request: Request, choice: str = Form(...)):
    global score
    global current_message

    if not current_message:
        return RedirectResponse(url="/", status_code=303)

    correct = (choice.lower() == current_message["label"])
    if correct:
        score += 1
        result = f"🎃 Correct! You spotted the {'phish' if choice == 'phish' else 'treat'}!"
    else:
        result = f"👻 Oops! That was actually a {current_message['label']}."

    current_message = random.choice(messages)
    return templates.TemplateResponse("index.html", {"request": request, "message": current_message, "score": score, "result": result})
