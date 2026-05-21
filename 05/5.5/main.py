from fastapi import FastAPI, Response
from datetime import datetime
from models import CommonHeaders

app = FastAPI()


@app.get("/headers")
async def get_headers(headers: CommonHeaders):
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language
    }

@app.get("/info")
async def get_info(headers: CommonHeaders, response: Response):
    current_time = datetime.now().isoformat()
    response.headers["X-Server-Time"] = current_time
    
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    }
