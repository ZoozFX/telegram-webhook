
from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

@app.post("/send")
async def send_to_telegram(request: Request):
    data = await request.json()
    token = os.getenv("token")
    chat_id = os.getenv("chat_id")

    message = f"""📣 حدث: {data.get('event', 'غير معروف')}
📈 الأداة: {data.get('symbol', 'غير معروف')}
💵 السعر: {data.get('price', '?')}
📝 ملاحظة: {data.get('note', '')}"""

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message.strip()}

    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

    return {"status": "تم الإرسال ✅"}
