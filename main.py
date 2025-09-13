from fastapi import FastAPI
from app.api import users, advertisements, ratings, categories, messages
from app.auth import auth
from app.db.database import Base, engine

app = FastAPI(title="MarketNest API")

app.include_router(auth.router, prefix="/auth", tags=['auth'])
app.include_router(users.router, prefix="/users", tags=['users'])
app.include_router(advertisements.router, prefix='/advertisements', tags=['advertisements'])
app.include_router(categories.router, prefix='/categories', tags=['categories'])
app.include_router(ratings.router, prefix="/ratings", tags=["ratings"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])


Base.metadata.create_all(bind=engine)