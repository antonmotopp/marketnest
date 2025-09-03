from fastapi import FastAPI

app = FastAPI(title='MarketNest API')

@app.get("/")
def root():
    return {"message": "Server is working"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)