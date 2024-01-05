from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/some_chat")
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})