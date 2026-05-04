# 🧠 Review Analytics System

A Python-based project that scrapes Amazon product reviews, analyzes sentiment using AI, and generates insights such as revenue impact and user behavior.

---

## 🚀 Features

- 🔍 Scrape Amazon product reviews using Playwright
- 🔐 Persistent login session handling
- 🤖 AI-powered sentiment analysis (Gemini/OpenAI compatible)
- 📊 Revenue and review analytics
- 📁 Structured JSON output for further processing

---

## 📂 Project Structure

```
Review Analytics/
│
├── app.py
├── main.py
├── scraper.py
├── ai_engine.py
├── revenue_engine.py
├── all_reviews.py
├── step5_login_session.py
│
├── reviews_data/        # Scraped review data
├── reviews.json         # Processed output
├── amazon_session.json  # Saved login session
├── .env                 # Environment variables
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd Review-Analytics
```

---

### 2️⃣ Create and activate virtual environment

```bash
python -m venv venv
```

#### ▶️ Activate:

- **Windows**

```bash
venv\Scripts\activate
```

- **Mac/Linux**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install required libraries

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Install Playwright browsers

```bash
playwright install
```

---

## 🔐 Amazon Login Session Setup (IMPORTANT)

Before scraping reviews, you must log in to Amazon and save your session.

### 👉 Run:

```bash
python step5_login_session.py
```

### 🧭 What to do:

1. A browser window will open
2. Log in to your Amazon account manually
3. Complete CAPTCHA / OTP if prompted
4. Wait until login is successful
5. The session will be saved automatically as:

```
amazon_session.json
```

✅ This allows scraping without logging in every time.

---

## 🤖 AI Setup (Gemini API Key)

Your project uses AI for sentiment analysis.

### 👉 Step:

Open:

```
ai_engine.py
```

### 🔑 Add your Gemini API key:

Example:

```python
GEMINI_API_KEY = "your_api_key_here"
```

⚠️ Important:

- Do NOT commit your API key to GitHub
- You can also store it in `.env` for better security

---

## ▶️ Running the Project

After setup is complete:

```bash
python main.py
```

---

## 📊 Output

- `reviews.json` → processed reviews with sentiment
- `reviews_data/` → raw scraped data

---

## ⚠️ Notes & Best Practices

- Do not share:
  - `.env`
  - `amazon_session.json`

- Amazon may block scraping if overused → use responsibly
- Always ensure your login session is valid

---

## 🛠️ Troubleshooting

### ❌ Playwright errors

```bash
playwright install
```

### ❌ Login not working

- Delete `amazon_session.json`
- Re-run:

```bash
python step5_login_session.py
```

### ❌ AI not working

- Check API key
- Verify internet connection

---

## 📌 Future Improvements

- Web dashboard for analytics
- Real-time review tracking
- Multi-product comparison
- Deployment as SaaS

---

## 👨‍💻 Author

**Venkata Sankar Chatakondu**  
AI Engineer | Full Stack Developer (MERN + FastAPI)  
Building LLM-powered systems, AI agents, and scalable healthcare solutions

## ⭐ If you found this useful

Give it a star on GitHub 🌟
