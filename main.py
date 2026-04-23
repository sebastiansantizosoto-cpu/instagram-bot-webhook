from fastapi import FastAPI, Request, Query
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "mi_token_secreto")

@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    logger.info(f"Webhook verification: mode={hub_mode}")
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)
    return {"error": "Token inválido"}

@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    logger.info(f"Mensaje recibido: {data}")
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "Bot activo"}
