# M Lok Narayan — Portfolio

A full-stack portfolio website built with **Python (Flask)** backend and a custom HTML/CSS/JS frontend.

---

## 🗂 Project Structure

```
portfolio/
├── app.py               # Flask backend
├── requirements.txt     # Python dependencies
├── Procfile             # For Render/Railway deploy
├── render.yaml          # Render config
├── messages.json        # Auto-created, stores contact form submissions
├── templates/
│   └── index.html       # Main HTML template
└── static/
    ├── resume.pdf        # ← ADD YOUR RESUME HERE
    └── (css/js/images)  # Optional static assets
```

---

## 🚀 Run Locally

### 1. Install Python 3.10+
Make sure Python is installed: `python --version`

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
python app.py
```

Visit: **http://localhost:5000**

---

## 📧 Email Setup (Gmail)

To receive contact form messages by email:

1. Go to your Google Account → Security → **2-Step Verification** → **App Passwords**
2. Create an App Password (select "Mail")
3. Set environment variables:

```bash
export EMAIL_USER="your.gmail@gmail.com"
export EMAIL_PASSWORD="your-app-password"
export EMAIL_TO="mloknarayan@gmail.com"
```

Or create a `.env` file (install `python-dotenv` and load it in `app.py`).

---

## ☁️ Deploy to Render (Free Hosting)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial portfolio"
git remote add origin https://github.com/YOUR_USERNAME/portfolio.git
git push -u origin main
```

### Step 2 — Deploy on Render
1. Go to [render.com](https://render.com) and sign up free
2. Click **New → Web Service**
3. Connect your GitHub repo
4. Settings:
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Add Environment Variables:
   - `EMAIL_USER` → your Gmail
   - `EMAIL_PASSWORD` → your App Password
   - `EMAIL_TO` → mloknarayan@gmail.com
   - `ADMIN_KEY` → any secret key you choose
6. Click **Deploy** — your site will be live at `https://your-app.onrender.com`

---

## 🛤 Alternative: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Add the same environment variables
4. Done — Railway auto-detects the Procfile

---

## 🔑 Admin: View Messages

Visit: `https://your-site.com/api/messages?key=YOUR_ADMIN_KEY`

This returns all contact form submissions as JSON.

---

## ✏️ Customise

| What to change | Where |
|---|---|
| Name, bio, roles | `templates/index.html` → About section |
| Projects | `templates/index.html` → Projects section |
| Social links | `templates/index.html` → Contact section |
| Skills & bars | `templates/index.html` → Skills section |
| Stats (15+ projects etc.) | `templates/index.html` → Hero section |
| Email recipient | `app.py` → `EMAIL_TO` variable |
| Your resume | Replace `static/resume.pdf` |
| Admin key | `app.py` → `ADMIN_KEY` default or env var |

---

## 🔒 .gitignore

Create a `.gitignore` file:
```
venv/
__pycache__/
*.pyc
messages.json
.env
.DS_Store
```

---

## 📬 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Serves the portfolio |
| `/api/contact` | POST | Saves + emails contact form |
| `/api/messages?key=KEY` | GET | Admin: view all messages |
| `/api/stats` | GET | Returns portfolio stats JSON |

---

Built with ❤️ by M Lok Narayan
