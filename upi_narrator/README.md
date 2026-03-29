# UPI Narrator — AI-Powered UPI Expense Analyser

Your money, finally explained. Upload your UPI transaction CSV and get a personalised AI-written money story with charts, insights, and forward-looking tips.

---

## Setup (5 minutes)

### 1. Clone / download this project
```
upi_narrator/
├── app.py
├── requirements.txt
├── pages/
│   ├── upload.py
│   ├── dashboard.py
│   ├── narrative.py
│   └── insights.py
├── utils/
│   ├── processor.py
│   └── ai_engine.py
└── data/
    └── demo_transactions.csv
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

The app opens at http://localhost:8501

---

## How to use

**Without AI (free, no API key needed)**
- Click "Try with demo data" on the Upload tab
- Explore Dashboard, My Story, and Insights tabs
- Insights and narrative use smart rule-based fallbacks

**With AI (OpenAI API key needed)**
- Get a free API key at platform.openai.com
- Paste it in the Upload tab expander
- Upload your real CSV or use demo data
- AI generates a personalised narrative and 6 specific insights

---

## How to export your UPI CSV

**Google Pay:**
Open GPay → Profile icon → Statements & Transactions → Download

**PhonePe:**
Open PhonePe → History → Download Statement → CSV

**Paytm:**
Open Paytm → Passbook → Download Statement

---

## Deploy to Streamlit Cloud (free)

1. Push this folder to a GitHub repo
2. Go to share.streamlit.io
3. Connect your GitHub → select repo → select app.py
4. Deploy — get a live public link in 2 minutes

---

## Tech stack

- **Frontend:** Streamlit
- **Data:** Pandas
- **Charts:** Plotly
- **AI:** OpenAI GPT-4o-mini
- **Deploy:** Streamlit Cloud (free)

---

Built by Sayan Sengupta · UEM Kolkata · APM Portfolio Project · 2025
