from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.admin.routers import main_router
from app.core.config import settings

# Создание экземпляра приложения FastAPI
app = FastAPI(
    title=settings.app_title,
    description=settings.app_description
)

# Добавление промежуточного слоя CORS для разрешения запросов с других источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Создание экземпляра Jinja2Templates для работы с HTML-шаблонами
templates = Jinja2Templates(directory="app/api/admin/static")

# Определение маршрута для корневого URL ("/") с указанием HTMLResponse в качестве класса ответа
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Включение дополнительных маршрутов с префиксом "/api"
app.include_router(main_router, prefix="/api")

# Подключение директории "/static" для обслуживания статических файлов
app.mount("/static", StaticFiles(directory="app/api/admin/static"), name="static")
