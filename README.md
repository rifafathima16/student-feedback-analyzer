# Student Feedback Analyzer

A beginner‑friendly Flask web app that collects student feedback, analyses sentiment with VADER, stores the data in a local MongoDB, and displays an analytics dashboard.

---

## 📦 Project Structure

```
student-feedback-analyzer/
│
├─ app.py                 # Main Flask app – routes, DB connection, sentiment analysis, suggestions
├─ requirements.txt       # Python dependencies (Flask, pymongo, vaderSentiment)
├─ seed_data.py           # Generates 1,000 realistic fake feedback records
├─ static/
│   └─ style.css          # Dark purple‑blue theme, responsive cards, gradient navbar
└─ templates/
    ├─ index.html         # Feedback form with validation and flash messages
    ├─ thankyou.html      # Simple thank‑you page after a successful submission
    └─ dashboard.html     # Dashboard showing stats, Chart.js doughnut chart, and suggestions
```

Each file is kept short and well‑commented for easy understanding.

---

## 🚀 Quick Start

1. **Start MongoDB locally** (default URI `mongodb://localhost:27017`)
   ```bash
   mongod --port 27017
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   .\\venv\\Scripts\\activate   # PowerShell on Windows
   ```
3. **Install the required packages**
   ```bash
   pip install -r requirements.txt
   ```
4. **(Optional) Load sample data**
   ```bash
   python seed_data.py   # inserts 1 000 fake feedback documents
   ```
5. **Run the Flask app**
   ```bash
   python app.py
   ```
   Visit `http://127.0.0.1:5000/` in your browser.

---

## 🛠️ How It Works (simple terms)

- **`app.py`** – Sets up Flask, connects to MongoDB, defines the home route (`/`) for the feedback form, the `/dashboard` route for analytics, and a helper `get_suggestions` that scans negative comments for keywords and returns improvement tips.
- **`seed_data.py`** – Creates realistic fake feedback using random subjects, faculty names, and comment sentences, clears the collection first so you can re‑run safely.
- **`templates/index.html`** – Shows the feedback form. If the comment field is empty, a flash error is shown and previously entered values are preserved.
- **`templates/dashboard.html`** – Retrieves feedback from MongoDB, calculates totals, percentages, average rating, renders a Chart.js doughnut chart, lists the 10 most recent entries, and displays the top suggestions.
- **`static/style.css`** – Provides the dark purple‑blue visual theme with gradient navbar, rounded cards, soft shadows, and responsive layout.
- **`requirements.txt`** – Lists exact package versions used.

---

## 💡 Tips & Next Steps

- Replace the hard‑coded `app.secret_key` with a strong random value before deploying.
- Change the MongoDB URI if you want to use a remote database.
- Add more keyword‑to‑suggestion pairs inside `get_suggestions` for richer advice.
- Deploy to a cloud provider (e.g., Render, Fly.io) – remember to turn off `debug` mode.

Enjoy exploring student feedback!
