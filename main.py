import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import users, advertisements, ratings, categories, messages, chat
from app.auth import auth
from app.db.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from logger_config import setup_logger

app = FastAPI(title="MarketNest API")

app.include_router(auth.router, prefix="/auth", tags=['auth'])
app.include_router(users.router, prefix="/users", tags=['users'])
app.include_router(advertisements.router, prefix='/advertisements', tags=['advertisements'])
app.include_router(categories.router, prefix='/categories', tags=['categories'])
app.include_router(ratings.router, prefix="/ratings", tags=["ratings"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
app.include_router(chat.router, prefix="/chat", tags=['websockets'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://marketnest-client.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

logger = setup_logger()



@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"➡ {request.method} {request.url}")

    try:
        response = await call_next(request)
    except Exception as e:
        process_time = (time.time() - start_time) * 1000
        logger.error(f"🔥 Error: {type(e).__name__}: {str(e)} "
                     f"- {request.method} {request.url} (500) "
                     f"({process_time:.2f} ms)")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"}
        )

    process_time = (time.time() - start_time) * 1000
    logger.info(f"⬅ {request.method} {request.url} Status: {response.status_code} "
                f"({process_time:.2f} ms)")
    return response