from fastapi import FastAPI, Request, Query
import os
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "mi_token_secreto")
N8N_WEBHOOK_URL = "https://cursonn8n-n8n.zptqct.easypanel.host/webhook/instagram"

@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)
    return {"error": "Token inválido"}

@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    logger.info(f"Mensaje recibido: {data}")
    async with httpx.AsyncClient() as client:
        await client.post(N8N_WEBHOOK_URL, json=data)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "Bot activo"}
