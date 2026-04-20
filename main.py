from fastapi import FastAPI, Request, Query
import os

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "mi_token_secreto")

@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)
    return {"error": "Token inválido"}, 403

@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print("Mensaje recibido:", data)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "Bot activo"}