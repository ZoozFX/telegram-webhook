from fastapi import FastAPI, Request, Query
import httpx
import os

app = FastAPI()

def build_message(data: dict) -> str:
    return f"""📣 تنبيه: {data.get('alert', 'غير معروف')}
📈 الزوج: {data.get('symbol', '؟')}
💵 السعر: {data.get('price', '?')}"""

@app.post("/send")
async def send_post_to_telegram(request: Request):
    data = await request.json()

    if data.get("secret") != os.getenv("secret"):
        return {"status": "❌ Secret غير صحيح"}

    token = os.getenv("token")
    chat_id = os.getenv("chat_id")
    message = build_message(data)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message.strip()}

    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

    return {"status": "✅ تم الإرسال من POST"}

@app.get("/send")
async def send_get_to_telegram(
    alert: str = Query(None),
    symbol: str = Query(None),
    price: str = Query(None),
    secret: str = Query(None)
):
    if secret != os.getenv("secret"):
        return {"status": "❌ Secret غير صحيح"}

    token = os.getenv("token")
    chat_id = os.getenv("chat_id")
    message = build_message({
        "alert": alert,
        "symbol": symbol,
        "price": price
    })

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message.strip()}

    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

    return {"status": "✅ تم الإرسال من GET"}
