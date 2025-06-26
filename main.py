from fastapi import FastAPI, Request, Query
import httpx
import os

app = FastAPI()

# توليد رسالة بناءً على نوع التنبيه
def build_message(data: dict) -> str:
    alert_type = data.get("alert")

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
📊 Tickmill: {"✅" if data.get('Tickmill') else "❌"} | XM: {"✅" if data.get('xm') else "❌"}
"""

    elif alert_type == "condition_move_tsl":
        return f"""🔄 تعديل هدف للصفقة رقم: {data.get('id')}
🪙 الزوج: {data.get('symbol')}
📈 السعر الجديد: {data.get('price')}
🎯 الهدف المعدل: {data.get('edit')}
"""

    elif alert_type == "all_open":
        return f"""📢 تم فتح جميع الصفقات بنجاح
🪙 الزوج: {data.get('symbol')}
"""

    elif alert_type == "get_id":
        return f"""🔍 طلب معلومات صفقة

🆔 ID: {data.get('id')}
🪙 الزوج: {data.get('symbol')}
"""

    elif alert_type == "close_now":
        return f"""🔴 تم إغلاق الصفقة يدويًا

🆔 ID: {data.get('id')}
🪙 الزوج: {data.get('symbol')}
📈 السعر: {data.get('price')}
🔁 النوع: {data.get('type')}
"""

    else:
        return f"""📣 تنبيه: {alert_type}
📈 الزوج: {data.get('symbol', '؟')}
💵 السعر: {data.get('price', '?')}"""

# استقبال عبر POST من TradingView
@app.post("/send")
async def send_post_to_telegram(request: Request):
    data = await request.json()

    # تحقق من السر
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

# استقبال عبر GET من الميتاتريدر
@app.get("/send")
async def send_get_to_telegram(
    alert: str = Query(None),
    symbol: str = Query(None),
    price: str = Query(None),
    secret: str = Query(None),
    id: str = Query(None),
    type: str = Query(None)
):
    if secret != os.getenv("secret"):
        return {"status": "❌ Secret غير صحيح"}

    token = os.getenv("token")
    chat_id = os.getenv("chat_id")

    data = {
        "alert": alert,
        "symbol": symbol,
        "price": price,
        "id": id,
        "type": type
    }

    message = build_message(data)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message.strip()}

    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

    return {"status": "✅ تم الإرسال من GET"}
