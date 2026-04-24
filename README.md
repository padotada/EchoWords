# EchoWords

**EchoWords** is an AI-powered language analysis platform built during **Irvine Hacks (Jan 2025)**.  
It combines a **React frontend** with a **Flask backend** to translate and analyze multilingual text in English, with a focus on high-quality outputs and low-latency responses.

---

## 🚀 Features

- 🌍 **Multilingual text input**
- 🔁 **Translation to English**
- 🧠 **AI-powered language analysis**
- ⚡ **Optimized Gemini API query design** for faster, better responses
- 💻 **Clean web interface** for quick interaction and iteration

---

## 🧩 Tech Stack

### Frontend
- React
- JavaScript
- HTML/CSS

### Backend
- Python
- Flask

### AI Integration
- Gemini Developer API

---

## 🏗️ Project Architecture

```text
Client (React UI)
   ↓
Flask API (Python backend)
   ↓
Gemini Developer API
   ↓
Translated + analyzed English output returned to UI
```

---

## 🎯 Motivation

Language tools often stop at literal translation.  
EchoWords was built to provide both **translation** and **analysis** so users can better understand meaning, tone, and context—not just converted words.

---

## 👥 Team & Collaboration

This project was built collaboratively during Irvine Hacks.  
Our team worked across frontend, backend, and AI integration to ship a usable end-to-end product under hackathon time constraints.

---

## 🛠️ My Contributions

- Built and integrated parts of the **React + Flask full-stack flow**
- Worked on **Gemini Developer API query/prompt refinement**
- Improved **translation quality** through better query construction
- Reduced **response latency** by optimizing request patterns

---

## 📦 Getting Started

> Update these commands if your exact folder names differ.

### 1) Clone the repository

```bash
git clone https://github.com/arjun-mann/EchoWords.git
cd EchoWords
```

### 2) Backend setup (Flask)

```bash
# from backend folder (example)
cd backend
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the backend directory:

```env
GEMINI_API_KEY=your_api_key_here
FLASK_ENV=development
```

Run the backend server:

```bash
flask run
```

### 3) Frontend setup (React)

Open a new terminal:

```bash
# from frontend folder (example)
cd frontend
npm install
npm start
```

The app should now be running locally (commonly on `http://localhost:3000`) and communicating with the Flask API.

---

## 🔐 Environment Variables

Typical variables you may need:

- `GEMINI_API_KEY` — API key for Gemini Developer API
- `FLASK_ENV` — Flask environment (`development` / `production`)
- `API_BASE_URL` (frontend, optional) — backend URL if not localhost

---

## 🧪 Future Improvements

- Add user authentication and saved history
- Support side-by-side comparison for multiple model outputs
- Add language detection confidence and richer linguistic metrics
- Improve error handling and request retry logic
- Containerize deployment with Docker

---

## 📸 Screenshots

> Add your screenshots here.

- `docs/home.png` — homepage
- `docs/results.png` — translation + analysis output

---

## 📄 License

Add your preferred license (MIT is common for student projects).

---

## 🙌 Acknowledgments

- Irvine Hacks organizers and mentors
- Gemini Developer API documentation and tooling
- Teammates who collaborated on product design and implementation
