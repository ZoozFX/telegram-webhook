from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

# متغير لحفظ آخر بيانات تنبيه
last_data = {}

# تنسيق رسالة التليجرام
def build_message(data: dict) -> str:
    return f"""📣 تنبيه: {data.get('alert', 'غير معروف')}
📈 الزوج: {data.get('symbol', '؟')}
💵 السعر: {data.get('price', '?')}"""

# POST - من TradingView
@app.post("/send")
async def send_post_to_telegram(request: Request):
    global last_data
    data = await request.json()

    if data.get("secret") != os.getenv("secret"):
        return {"status": "❌ Secret غير صحيح"}

    last_data = data  # حفظ آخر بيانات

    token = os.getenv("token")
    chat_id = os.getenv("chat_id")
    message = build_message(data)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message.strip()}

    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

    return {"status": "✅ تم الإرسال من POST"}

# GET - يحصل على آخر بيانات
@app.get("/last")
async def get_last_data():
    global last_data
    return last_data
