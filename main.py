from fastapi import FastAPI
from app.api import auth
from app.db.database import Base, engine

app = FastAPI(title='MarketNest API')

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=['auth'])

@app.get("/")
def root():
    return "Server is working"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)