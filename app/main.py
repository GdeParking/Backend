from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import api_router
from app.admin.routers import admin_router
from app.core.config import settings
import uvicorn

from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}", encoding="utf-8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    lifespan=lifespan
)


app.state.debug = True

origins = ['http://localhost:3000/',]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router)
app.include_router(admin_router)

# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url("redis://localhost")
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")



if __name__=='__main__':
    uvicorn.run(app='app.main:app',
                reload=True)

