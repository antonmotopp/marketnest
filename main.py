from fastapi import FastAPI
from app.api import auth, advertisements

app = FastAPI(title='MarketNest API')

app.include_router(auth.router, prefix="/auth", tags=['auth'])
app.include_router(advertisements.router, prefix='/advertisements', tags=['advertisements'])

@app.get("/")
def root():
    return "Server is working"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)