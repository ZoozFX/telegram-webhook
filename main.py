from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

# متغير لحفظ آخر رسالة
last_data = {}

# تنسيق الرسالة حسب نوع التنبيه
def build_message(data: dict) -> str:
    alert_type = data.get("alert", "unknown")
    if alert_type == "buy_now":
        return f"""🟢 فتح صفقة جديدة

🔹 النوع: {data.get('type', 'N/A')}
💼 اللوت: {data.get('lot', 'N/A')}
📈 السعر: {data.get('price', 'N/A')}
🪙 الزوج: {data.get('symbol', 'N/A')}

🎯 TP1: {data.get('tp1', 'N/A')}
🎯 TP2: {data.get('tp2', 'N/A')}
🎯 TP3: {data.get('tp3', 'N/A')}
🛑 وقف خسارة: {data.get('stop', 'N/A')}
📊 Tickmill: {"✅" if data.get('Tickmill') else "❌"} | XM: {"✅" if data.get('xm') else "❌"}"""

    elif alert_type == "close_now":
        return f"""🔴 تم إغلاق الصفقة يدويًا

🆔 ID: {data.get('id')}
🪙 الزوج: {data.get('symbol')}
📈 السعر: {data.get('price')}
🔁 النوع: {data.get('type')}"""

    else:
        return f"""📣 تنبيه: {alert_type}
📈 الزوج: {data.get('symbol', '؟')}
💵 السعر: {data.get('price', '?')}"""

# POST - من TradingView
@app.post("/send")
async def send_post_to_telegram(request: Request):
    global last_data
    data = await request.json()

    if data.get("secret") != os.getenv("secret"):
        return {"status": "❌ Secret غير صحيح"}

    last_data = data  # حفظ البيانات الأخيرة

    token = os.getenv("token")
    chat_id = os.getenv("chat_id")
    message = build_message(data)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message.strip()}

    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

    return {"status": "✅ تم الإرسال من POST"}

# GET - لقراءة آخر رسالة
@app.get("/last")
async def get_last_data():
    global last_data
    return last_data
