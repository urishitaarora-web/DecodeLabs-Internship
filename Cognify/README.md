# 🧠 Cognify – AI-Powered Machine Learning Workspace

<p align="center">
  <strong>Transform raw datasets into intelligent insights through an automated data analysis and machine learning workspace.</strong>
</p>

<p align="center">
  <a href="https://cognify-frontend-bggv.onrender.com">
    <img src="https://img.shields.io/badge/Live%20Demo-Render-46E3B7?style=for-the-badge&logo=render" />
  </a>
  <img src="https://img.shields.io/badge/React-Vite-61DAFB?style=for-the-badge&logo=react&logoColor=black"/>
  <img src="https://img.shields.io/badge/FastAPI-Python-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Clerk-Authentication-6C47FF?style=for-the-badge&logo=clerk"/>
  <img src="https://img.shields.io/badge/Supabase-Database-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white"/>
</p>

---

## 🌐 Live Demo

**Frontend:**
https://cognify-frontend-bggv.onrender.com

**Backend API:**
https://cognify-backend-gk08.onrender.com

---

## 📖 About

Cognify is an AI-powered machine learning workspace designed to simplify the journey from raw datasets to meaningful insights.

The platform brings dataset management, automated analysis, data quality assessment and preprocessing into one workspace, with ML training and advanced intelligence planned for upcoming phases.

### Core Workflow

```text
Dataset Upload
      ↓
Data Analysis
      ↓
Data Quality Assessment
      ↓
Preprocessing
      ↓
ML Training
      ↓
Evaluation
      ↓
Prediction & Insights
```

---

## ✨ Current Features

* Secure authentication with **Clerk**
* Dataset upload and management
* Support for **CSV, XLSX and JSON**
* Dataset library with user-specific datasets
* Automated dataset analysis
* Missing-value analysis
* Duplicate detection
* Data quality information
* Automatic column type detection
* Column-level intelligence
* Numeric statistics:

  * Count
  * Sum
  * Mean
  * Median
  * Minimum
  * Maximum
  * Variance
  * Standard deviation
* Histograms and distribution visualizations
* Correlation analysis
* Categorical column insights
* Interactive analysis dashboard
* FastAPI backend with protected endpoints
* Supabase database integration
* Render deployment
* Responsive React/Vite interface

---
## 🛠️ Tech Stack

**Frontend**

* React
* Vite
* JavaScript
* CSS
* Recharts
* Lucide React

**Backend**

* Python
* FastAPI
* Pandas
* Uvicorn

**Authentication & Database**

* Clerk
* Supabase

**Deployment**

* Render

---

## 🏗️ Architecture

```text
User
 │
 ▼
React + Vite Frontend
 │
 │ Clerk Token
 ▼
FastAPI Backend
 │
 ├── Dataset Analysis
 ├── EDA
 ├── Preprocessing
 │
 ├── Clerk Authentication
 │
 └── Supabase
       │
       ▼
   Dataset Storage
```

---

## 📂 Project Structure

```text
Cognify/
├── backend/
│   ├── main.py
│   ├── analysis_router.py
│   ├── eda_router.py
│   ├── preprocessing.py
│   ├── preprocessing_router.py
│   ├── dataset_storage.py
│   ├── clerk_auth.py
│   └── requirements.txt
│
├── src/
│   ├── components/
│   ├── pages/
│   │   ├── AnalysisPage.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Landing.jsx
│   │   └── WorkspacePage.jsx
│   └── App.jsx
│
├── public/
├── stitch-reference/
├── package.json
└── vite.config.js
```

---

## 💻 Local Setup

### Frontend

```bash
npm install
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

Configure environment variables using the provided `.env.example` files.

---

## 🔐 Security

Cognify uses:

* Clerk authentication
* Backend token verification
* Protected dataset endpoints
* User-specific dataset access
* Environment-based secrets
* Supabase service-role key restricted to the backend
* Production CORS configuration

Production secrets are not committed to GitHub.

---

## 🚧 Current Progress

### Completed

* Frontend foundation
* Landing page
* Authentication
* Dashboard
* Workspace
* Dataset upload
* Dataset storage
* Dataset library
* Backend API
* Automated dataset analysis
* EDA functionality
* Column Intelligence
* Statistical analysis
* Visualization
* Render deployment

### Next

* Automated preprocessing recommendations
* Outlier detection and handling
* Feature engineering
* ML model training
* Model comparison
* Model evaluation
* Prediction
* Explainable AI
* Automated reports

---

## 🎯 Goal

> **Make machine learning workflows simpler, faster, and easier to understand.**

Cognify aims to bring the complete machine learning lifecycle into one intelligent workspace.

---

## 👩‍💻 Author

**Urishita Arora**

GitHub:
https://github.com/urishitaarora-web
