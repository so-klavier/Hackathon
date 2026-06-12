from fastapi import FastAPI

app = FastAPI(title="Hackathon")

@app.get("/")
async def root():
    return{"message": "surver running"}