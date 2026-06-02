# 📧 Email Tracker

Gmail বা যেকোনো email এ invisible tracking pixel যোগ করে জানো কে, কখন, কোথা থেকে email open করেছে।

---

## 🚀 Render এ Deploy করার steps

### Step 1 — GitHub এ upload করো
1. [github.com](https://github.com) এ account বানাও (না থাকলে)
2. New repository তৈরি করো — নাম দাও `email-tracker`
3. এই folder এর সব file upload করো

### Step 2 — Render এ Deploy
1. [render.com](https://render.com) এ account বানাও (GitHub দিয়ে login করো)
2. "New +" → "Web Service" click করো
3. তোমার `email-tracker` repo select করো
4. নিচের settings দাও:
   - **Name:** email-tracker
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. "Create Web Service" click করো
6. ২-৩ মিনিট অপেক্ষা করো — Deploy হয়ে যাবে!

### Step 3 — URL পাবে
Deploy হলে Render তোমাকে একটা URL দেবে, যেমন:
`https://email-tracker-xxxx.onrender.com`

---

## 📌 কীভাবে ব্যবহার করবে

1. Dashboard এ যাও: `https://your-url.onrender.com`
2. একটা **Email ID** দাও (যেমন: `raj_followup`)
3. **Pixel তৈরি করো** button চাপো
4. HTML code copy করো
5. Email লেখার সময় HTML mode এ গিয়ে সেই code paste করো
6. Email পাঠাও!
7. Dashboard এ দেখো কে কখন open করেছে 🎉

---

## 📁 File Structure

```
email-tracker/
├── app.py              ← Main server
├── requirements.txt    ← Python packages
├── render.yaml         ← Render config
├── Procfile            ← Start command
└── templates/
    └── dashboard.html  ← Dashboard UI
```
