# 🛡️ DeepGuard — DeepFake Detection & Content Authentication System

DeepGuard is an AI-powered web application designed to detect manipulated or deepfake media and provide content verification capabilities.

The project uses a modern React-based frontend with a Python Flask backend. The backend provides dedicated API routes for authentication, deepfake detection, and content verification.

---

## 🚀 Features

- 🔐 User Authentication
- 🕵️ DeepFake Detection
- ✅ Media/Content Verification
- 📤 Upload media for analysis
- 🤖 AI/ML-based content analysis
- ⚡ REST API powered by Flask
- 🎨 Modern React + Tailwind CSS frontend
- 📱 Responsive web interface
- 🔄 Frontend and backend API integration

---

## 🏗️ Project Architecture

```text
deepfake-main/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── authenticate.py
│   │   │   ├── detect.py
│   │   │   └── verify.py
│   │   │
│   │   └── ...
│   │
│   ├── requirements.txt
│   └── ...
│
└── README.md

The Vite dev server proxies `/api` to `http://localhost:5000`, so both need to be running.
