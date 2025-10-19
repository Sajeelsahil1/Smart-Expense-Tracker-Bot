# 💰 Smart Expense Tracker Bot

A smart, Firebase-powered **Expense Tracker Bot** built with Python.  
It helps users **track, categorize, and analyze expenses** — with future AI features like spending advice and trend predictions.

---

## 🚀 Features

✅ Add, edit, and delete expenses  
✅ Track daily, weekly, and monthly spending  
✅ Visual reports with charts  
✅ Firebase backend for user data and authentication  
✅ AI (Gemini) integration — coming soon for smart spending insights  
✅ Export to CSV for reports  
✅ Secure secret management using `.env` (no Firebase keys in repo)

---

## 🧠 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend** | Python |
| **Database** | Firebase Firestore |
| **Frontend / UI** | Tkinter ) |
| **Authentication** | Firebase Auth |
| **Data Export** | CSV generation |
| **AI Suggestion** | Gemini API |

---

## 📦 Setup Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Sajeelsahil1/Smart-Expense-Tracker-Bot.git
cd "Smart Expense Tracker Bot"
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Mac/Linux
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Add Your Firebase Credentials

Create a file named `.env` in your root folder:

```bash
FIREBASE_KEY_PATH=firebase_key.json
```

> ⚠️ **Important:**
> Never upload `firebase_key.json` to GitHub.
> This file contains sensitive credentials.
> It’s already added to `.gitignore`.

### 5️⃣ Run the App

```bash
python smarttrackerbot.py
```

---

## 📊 Export to CSV

You can export your transactions to a CSV file:

```bash
python export_csv.py
```

---

## 🔐 Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/).
2. Create a new project.
3. Add a **Service Account Key** (JSON file).
4. Save it as `firebase_key.json` in your project root.
5. Add its path to `.env` (see above).

---

## 🧑‍💻 Authentication (Coming Soon)

Each user will be able to log in with Firebase Auth, so they only see their data.

---

## 💡 Future Enhancements

* 💬 **Gemini AI integration** to analyze your spending habits
* 📱 Mobile UI in Flutter
* 📈 Real-time dashboards
* 🔔 Smart alerts for overspending

---

## 📽 Demo Video

🎥 A short demo video is already included in this repo’s folder (`demo.mp4`).

---

## 🧾 License

This project is licensed under the **MIT License** — free for personal and educational use.

---

## ⭐ Support

If you like this project, give it a **star ⭐ on GitHub** and follow for more!

**Made with ❤️ by [Sajeel Sahil](https://github.com/Sajeelsahil1)**

```

---

Would you like me to make a **version that includes badges** (e.g., “Python”, “Firebase”, “Open Source”, “MIT License”) for a more professional GitHub look?
```
