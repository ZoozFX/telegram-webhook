from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

@app.post("/send")
async def send_to_telegram(request: Request):
    data = await request.json()

    # تحقق من السر
    if data.get("secret") != "8D81Yqh4lJbUsqGWpD9zCl1jQubexk":
        return {"status": "❌ Secret غير صحيح"}

    token = os.getenv("token")
    chat_id = os.getenv("chat_id")

    alert_type = data.get("alert")

    # رسالة افتراضية
    message = "🚨 تنبيه جديد لم يتم التعرف عليه."

    # ======= 1. فتح صفقة (buy_now) =======
    if alert_type == "buy_now":
        message = f"""🟢 فتح صفقة جديدة

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

    # ======= 2. تحريك التارجت (condition_move_tsl) =======
    elif alert_type == "condition_move_tsl":
        message = f"""🔄 تعديل هدف للصفقة رقم: {data.get('id')}

🪙 الزوج: {data.get('symbol')}
📈 السعر الجديد: {data.get('price')}
🎯 الهدف المعدل: {data.get('edit')}
"""

    # ======= 3. فتح جميع الصفقات (all_open) =======
    elif alert_type == "all_open":
        message = f"""📢 تم فتح جميع الصفقات بنجاح
🪙 الزوج: {data.get('symbol')}
"""

    # ======= 4. الحصول على صفقة معينة (get_id) =======
    elif alert_type == "get_id":
        message = f"""🔍 طلب معلومات صفقة

🆔 ID: {data.get('id')}
🪙 الزوج: {data.get('symbol')}
"""

    # ======= 5. إغلاق صفقة (close_now) =======
    elif alert_type == "close_now":
        message = f"""🔴 تم إغلاق الصفقة يدويًا

🆔 ID: {data.get('id')}
🪙 الزوج: {data.get('symbol')}
📈 السعر: {data.get('price')}
🔁 النوع: {data.get('type')}
"""

    # ======= إرسال الرسالة =======
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message.strip()}

    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

    return {"status": "تم الإرسال ✅"}
