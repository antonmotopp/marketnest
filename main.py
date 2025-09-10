from fastapi import FastAPI
from app.api import auth, users, advertisements, ratings
from app.db.database import Base, engine

app = FastAPI(title="MarketNest API")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=['auth'])
app.include_router(users.router, prefix="/users", tags=['users'])
app.include_router(advertisements.router, prefix='/advertisements', tags=['advertisements'])

app.include_router(ratings.router, prefix="/ratings", tags=["ratings"])