# 🧠 Cognify – AI-Powered Machine Learning Workspace

<p align="center">
  <strong>Transform raw datasets into intelligent machine learning workflows with automated data analysis, preprocessing, model training, evaluation, prediction, and explainable insights.</strong>
</p>

<p align="center">
  <a href="https://cognify-frontend-bggv.onrender.com">
    <img src="https://img.shields.io/badge/Live%20Demo-Render-46E3B7?style=for-the-badge&logo=render" />
  </a>
  <img src="https://img.shields.io/badge/React-Vite-61DAFB?style=for-the-badge&logo=react&logoColor=black"/>
  <img src="https://img.shields.io/badge/FastAPI-Python-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Clerk-Authentication-6C47FF?style=for-the-badge&logo=clerk"/>
  <img src="https://img.shields.io/badge/Supabase-Database-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white"/>
  <img src="https://img.shields.io/badge/Render-Deployment-46E3B7?style=for-the-badge&logo=render"/>
</p>

---

# 🌐 Live Demo

### 🚀 Frontend

https://cognify-frontend-bggv.onrender.com

### ⚙️ Backend API

https://cognify-backend-gk08.onrender.com

---

# 📖 About

Cognify is an AI-powered machine learning workspace designed to simplify the journey from raw data to machine learning insights.

Instead of switching between multiple tools for dataset analysis, preprocessing, model training, evaluation, prediction, and reporting, Cognify is designed to bring the complete ML workflow into a single intelligent workspace.

### Core Workflow

```text
Raw Dataset
     ↓
Data Analysis
     ↓
Data Quality Assessment
     ↓
Preprocessing
     ↓
Model Training
     ↓
Model Evaluation
     ↓
Model Comparison
     ↓
Prediction
     ↓
Explainable Insights
     ↓
Reports

Cognify currently provides a functional dataset management and analysis system with secure authentication, persistent dataset storage, automatic dataset-library updates, and a scalable architecture for future ML capabilities.

✨ Features
📂 Dataset Management
Upload datasets directly from the workspace
Drag & drop file upload
CSV support
XLSX / Excel support
JSON support
File type validation
File size detection
Dataset library
Persistent dataset records
Automatic library updates after upload
🔍 Automated Dataset Analysis

Cognify analyzes uploaded datasets and extracts:

Total rows
Total columns
Missing values
Missing-value percentage
Duplicate rows
Data quality score
Numerical columns
Categorical columns
Datetime columns
Column data types
Unique values per column
Missing values per column
Example
Dataset Analysis
│
├── Rows
├── Columns
├── Missing Values
├── Missing Percentage
├── Duplicate Rows
├── Data Quality Score
│
└── Column Information
    ├── Column Name
    ├── Data Type
    ├── Missing Values
    └── Unique Values
📊 Data Quality Assessment

Cognify generates an automated data-quality score based on dataset characteristics.

The current scoring system considers:

Missing values
Duplicate records
Dataset completeness

This gives users an immediate overview of whether a dataset is ready for further ML processing.

🔐 Authentication

Cognify uses Clerk for authentication.

Features include:

Secure user sign-in
Clerk session management
Protected backend APIs
Backend token verification
User-specific dataset access
Authenticated dataset saving
Authenticated dataset retrieval
🗄️ Persistent Dataset Storage

Cognify uses Supabase to store dataset metadata.

Stored information includes:

Dataset
│
├── ID
├── User ID
├── Filename
├── File Size
├── Rows
├── Columns
├── Missing Values
├── Missing Percentage
├── Duplicates
├── Data Quality
├── Column Types
├── Column Information
├── Status
└── Created At
⚡ Automatic Dataset Library Updates

After a dataset is successfully analyzed and saved, Cognify automatically refreshes the dataset library.

The user does not need to manually refresh the browser.

Upload Dataset
      ↓
Analyze Dataset
      ↓
Save Dataset
      ↓
Fetch Updated Dataset Library
      ↓
Library Automatically Updates
🧠 ML Workflow

Cognify is structured around a complete machine learning workflow.

1️⃣ Dataset

Upload and manage datasets.

2️⃣ Analysis

Understand dataset structure, types, missing values, duplicates, and quality.

3️⃣ Preprocessing

Prepare data for machine learning.

Planned capabilities include:

Missing-value handling
Duplicate removal
Outlier detection
Feature scaling
Categorical encoding
Feature engineering
4️⃣ Model Training

Train multiple machine learning models.

Planned model support includes:

Random Forest
XGBoost
Support Vector Machine
Logistic Regression
Neural Networks
5️⃣ Evaluation

Evaluate models using:

Accuracy
Precision
Recall
F1 Score
ROC-AUC
Confusion Matrix
6️⃣ Model Comparison

Compare multiple models based on their performance.

7️⃣ Prediction

Generate predictions using trained models.

8️⃣ Explainable AI

Provide understandable insights into model predictions and important features.

9️⃣ Reports

Generate structured dataset, model, evaluation, and prediction reports.

🏗️ Architecture
                         ┌───────────────────────┐
                         │       Cognify UI      │
                         │     React + Vite      │
                         └───────────┬───────────┘
                                     │
                                     │ HTTPS REST API
                                     ▼
                         ┌───────────────────────┐
                         │    FastAPI Backend    │
                         │        Python         │
                         └───────────┬───────────┘
                                     │
                 ┌───────────────────┼───────────────────┐
                 │                   │                   │
                 ▼                   ▼                   ▼
          ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
          │    Clerk    │     │  Supabase   │     │   Pandas    │
          │     Auth    │     │  Database   │     │ Data Engine │
          └─────────────┘     └─────────────┘     └─────────────┘
                                     │
                                     ▼
                          ┌────────────────────┐
                          │ Dataset Metadata   │
                          │ Persistent Storage │
                          └────────────────────┘
🛠️ Tech Stack
Category	Technologies
Frontend	React, Vite, JavaScript
UI	CSS, Lucide Icons
Backend	Python, FastAPI
Data Processing	Pandas
Excel Processing	OpenPyXL
Authentication	Clerk
Database	Supabase
API	REST API
Deployment	Render
Version Control	Git & GitHub
Development	VS Code
📂 Project Structure
Cognify/
│
├── index.html
├── package.json
├── package-lock.json
├── vite.config.js
│
├── README.md
├── architecture.md
├── .env.example
├── .gitignore
│
├── public/
│   └── assets/
│       └── cognify_workflow.mp4
│
├── src/
│   │
│   ├── App.jsx
│   ├── main.jsx
│   ├── styles.css
│   ├── supabase.js
│   │
│   ├── components/
│   │   ├── DatasetUploader.jsx
│   │   ├── Logo.jsx
│   │   ├── Navbar.jsx
│   │   ├── Shell.jsx
│   │   ├── ThemeToggle.jsx
│   │   └── WorkflowAnimation.jsx
│   │
│   ├── data/
│   │   └── pages.js
│   │
│   └── pages/
│       ├── Auth.jsx
│       ├── Dashboard.jsx
│       ├── Landing.jsx
│       └── WorkspacePage.jsx
│
├── backend/
│   │
│   ├── main.py
│   ├── clerk_auth.py
│   ├── requirements.txt
│   └── .env.example
│
└── stitch-reference/
    ├── DESIGN.md
    ├── code.html
    └── screen.png
🔑 Environment Variables
Frontend

Create a .env file inside the Cognify root directory.

VITE_API_URL=https://cognify-backend-gk08.onrender.com
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
Backend

Create:

backend/.env

Add:

SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
CLERK_SECRET_KEY=your_clerk_secret_key

⚠️ Never commit real API keys, Clerk secrets, or Supabase service-role keys to GitHub.

⚙️ Local Installation
1. Clone the Repository
git clone https://github.com/urishitaarora-web/DecodeLabs-Internship.git
2. Move Into Cognify
cd DecodeLabs-Internship/Cognify
💻 Frontend Setup

Install dependencies:

npm install

Start the Vite development server:

npm run dev

Frontend:

http://localhost:5173
🐍 Backend Setup

Move into the backend:

cd backend

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Start FastAPI:

uvicorn main:app --reload

Backend:

http://127.0.0.1:8000
🔗 API Endpoints
Health Check
GET /

Returns:

{
  "message": "Cognify ML Backend is running",
  "status": "online"
}
Analyze Dataset
POST /analyze-dataset

Accepts:

CSV
XLSX
JSON

Returns:

Dataset statistics
Missing-value information
Duplicate count
Data quality score
Column types
Column-level information
Save Dataset
POST /save-dataset

Stores authenticated dataset metadata in Supabase.

Get Datasets
GET /datasets

Returns datasets belonging to the authenticated Clerk user.

🔐 Authentication Flow
User
 ↓
Clerk Sign In
 ↓
Authenticated Session
 ↓
Frontend obtains Clerk Session Token
 ↓
Authorization: Bearer <token>
 ↓
FastAPI Backend
 ↓
Clerk Token Verification
 ↓
Authenticated User ID
 ↓
Supabase Dataset Query

This ensures that dataset operations are associated with the authenticated user.

🗃️ Database

The primary Supabase table is:

datasets

Important fields include:

id
user_id
filename
file_size
rows
columns
missing_values
missing_percentage
duplicates
data_quality
column_types
columns_info
status
created_at
🔒 Security

Cognify uses a backend-controlled authentication architecture.

Security practices include:

Clerk authentication
Backend token verification
Protected dataset endpoints
User-specific dataset queries
Environment-based secrets
Supabase service-role key kept on the backend
No production secrets committed to GitHub
CORS configuration for production frontend
📸 Screenshots

Recommended screenshots for the project:

screenshots/
│
├── landing-page.png
├── authentication.png
├── dashboard.png
├── dataset-upload.png
├── dataset-analysis.png
├── dataset-library.png
├── workflow.png
└── responsive-view.png

Add screenshots using:

![Cognify Landing Page](screenshots/landing-page.png)
🎬 Workflow Animation

Cognify includes a visual ML workflow animation representing the journey from raw data to insights.

Raw Dataset
     ↓
Data Cleaning
     ↓
Feature Engineering
     ↓
AI Training
     ↓
Model Comparison
     ↓
Prediction
     ↓
Insights Dashboard

Animation file:

public/assets/cognify_workflow.mp4
🚀 Deployment

Cognify is deployed using Render.

Frontend

https://cognify-frontend-bggv.onrender.com

Backend

https://cognify-backend-gk08.onrender.com

Production Architecture
                    User Browser
                         │
                         ▼
              ┌────────────────────┐
              │  Render Frontend   │
              │   React + Vite     │
              └─────────┬──────────┘
                        │
                        │ HTTPS
                        ▼
              ┌────────────────────┐
              │ Render Backend     │
              │ FastAPI + Python   │
              └─────────┬──────────┘
                        │
              ┌─────────┼─────────┐
              │         │         │
              ▼         ▼         ▼
           Clerk    Supabase    Pandas
            Auth     Database   Analysis
🧪 Current Project Status
Phase 1 – Foundation
 React/Vite frontend
 Premium landing page
 Dashboard
 Workspace
 Clerk authentication
 FastAPI backend
 Dataset upload
 CSV support
 XLSX support
 JSON support
 Dataset analysis
 Data quality scoring
 Dataset persistence
 Dataset library
 Automatic library refresh
 Protected API endpoints
 Supabase integration
 Render deployment
🔮 Future Roadmap
Phase 2 – Intelligent Preprocessing
Automated missing-value handling
Duplicate removal
Outlier detection
Feature scaling
Categorical encoding
Feature engineering
Automated preprocessing recommendations
Phase 3 – ML Training
Automated model selection
Multiple ML algorithms
Hyperparameter tuning
Cross-validation
Training history
Model versioning
Phase 4 – Model Evaluation
Accuracy
Precision
Recall
F1 Score
ROC-AUC
Confusion Matrix
Performance visualization
Phase 5 – Model Comparison
Side-by-side model comparison
Automated best-model selection
Performance ranking
Training-time comparison
Prediction-time comparison
Phase 6 – Explainable AI
Feature importance
Prediction explanations
SHAP-style insights
Human-readable recommendations
Explainable AI reports
Phase 7 – Reports & Deployment
Automated PDF reports
Dataset reports
Model reports
Prediction reports
Export functionality
Model deployment
Prediction APIs
🎯 Why Cognify?

Traditional machine learning workflows often require users to work across multiple tools for:

Data Collection
      +
Data Cleaning
      +
Data Analysis
      +
Preprocessing
      +
Model Training
      +
Evaluation
      +
Visualization
      +
Prediction

Cognify aims to bring these stages together into one intelligent workspace.

Our goal

Make machine learning workflows simpler, faster, and easier to understand.

🧠 Learning Outcomes

Building Cognify strengthened practical understanding of:

React
Vite
Component-based architecture
JavaScript
CSS
FastAPI
Python
Pandas
Dataset processing
REST APIs
Clerk authentication
Supabase
Database design
API security
CORS
Git & GitHub
Render deployment
Full-stack application architecture
🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
git checkout -b feature-name
3. Make your changes
4. Commit your changes
git add .
git commit -m "Added new feature"
5. Push your branch
git push origin feature-name
6. Open a Pull Request
👩‍💻 Author
Urishita Arora

GitHub:

https://github.com/urishitaarora-web

⭐ Show Your Support

If you found Cognify interesting or useful, consider giving the repository a ⭐ on GitHub.

Your support helps motivate continued development and improvement.

📜 License

This project is licensed under the MIT License.
