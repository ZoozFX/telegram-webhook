from fastapi import FastAPI, Request
import os
from datetime import datetime

app = FastAPI()

# حفظ آخر رسالة
last_data = {}

# ✅ POST - استقبال من TradingView
@app.post("/send")
async def send_post(request: Request):
    global last_data
    data = await request.json()

    if data.get("secret") != os.getenv("secret"):
        return {"status": "❌ Secret غير صحيح"}

    # ✅ إضافة الوقت كمُعرّف فريد
    data["time"] = datetime.utcnow().isoformat()
    last_data = data

    # 🚫 تم حذف إرسال الرسائل إلى Telegram
    return {"status": "✅ تم الاستلام بدون إرسال إلى Telegram"}

# ✅ GET - جلب آخر رسالة
@app.get("/last")
async def get_last_data():
    global last_data
    return last_data
