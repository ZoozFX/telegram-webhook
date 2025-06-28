from fastapi import FastAPI, Request
import httpx
import os
from datetime import datetime

app = FastAPI()

# حفظ آخر رسالة
last_data = {}

# تنسيق رسالة تيليجرام
def build_message(data: dict) -> str:
    alert_type = data.get("alert", "unknown").lower()

    if alert_type in ["buy_now", "sell_now"]:
        type_ = data.get("type", "buy").lower()
        price = float(data.get("price", "0"))

        try:
            tp1 = float(data.get("tp1", 0))
            tp2 = float(data.get("tp2", 0))
            tp3 = float(data.get("tp3", 0))
            stop = float(data.get("stop", 0))
        except:
            tp1 = tp2 = tp3 = stop = 0

        if type_ == "buy":
            tp1_price = price + tp1 
            tp2_price = price + tp2 
            tp3_price = price + tp3 
            stop_price = price - stop 
        else:
            tp1_price = price - tp1 
            tp2_price = price - tp2 
            tp3_price = price - tp3 
            stop_price = price + stop 

        return f"""{"🟢" if alert_type == "buy_now" else "🔴"} فتح صفقة جديدة

🔹 النوع: {data.get('type', 'N/A')}
💼 اللوت: {data.get('lot', 'N/A')}
📈 السعر: {price:.2f}
🪙 الزوج: {data.get('symbol', 'N/A')}

🎯 TP1: {tp1_price:.2f}
🎯 TP2: {tp2_price:.2f}
🎯 TP3: {tp3_price:.2f}
🛑 وقف خسارة: {stop_price:.2f}
📊 Tickmill: {"✅" if data.get('Tickmill') else "❌"} | XM: {"✅" if data.get('xm') else "❌"}"""

    elif alert_type == "close_now":
        return f"""🔴 تم إغلاق الصفقة يدويًا

🆔 ID: {data.get('id', 'N/A')}
🪙 الزوج: {data.get('symbol', 'N/A')}
📈 السعر: {data.get('price', 'N/A')}
🔁 النوع: {data.get('type', 'N/A')}"""

    elif alert_type == "condition_move_tsl":
        return f"""🔁 تحريك وقف الخسارة (TSL)

🪙 الزوج: {data.get('symbol', 'N/A')}
🆔 ID: {data.get('id', 'N/A')}
✏️ التعديل: {data.get('edit', 'N/A')}
📈 السعر الجديد: {data.get('price', 'N/A')}"""

    elif alert_type == "all_open":
        return f"""📊 عرض كل الصفقات المفتوحة

🪙 الزوج: {data.get('symbol', 'N/A')}"""

    elif alert_type == "get_id":
        return f"""📌 جلب بيانات الصفقة

🪙 الزوج: {data.get('symbol', 'N/A')}
🆔 ID: {data.get('id', 'N/A')}"""

    else:
        return f"""📣 تنبيه: {data.get('alert', 'N/A')}
🪙 الزوج: {data.get('symbol', '؟')}
📈 السعر: {data.get('price', '?')}"""

# ✅ POST - استقبال من TradingView
@app.post("/send")
async def send_post_to_telegram(request: Request):
    global last_data
    data = await request.json()

    if data.get("secret") != os.getenv("secret"):
        return {"status": "❌ Secret غير صحيح"}

    # ✅ إضافة time كمعرّف فريد
    data["time"] = datetime.utcnow().isoformat()

    last_data = data

    token = os.getenv("token")
    chat_id = os.getenv("chat_id")
    message = build_message(data)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message.strip()}

    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

    return {"status": "✅ تم الإرسال من POST"}

# ✅ GET - جلب آخر رسالة
@app.get("/last")
async def get_last_data():
    global last_data
    return last_data
