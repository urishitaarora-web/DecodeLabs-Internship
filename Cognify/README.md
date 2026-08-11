# Cognify Phase 1 — Stitch frontend converted into a React foundation

This package is based on the uploaded Stitch export `stitch_cognify_ai_platform.zip`.

## What was done

- Rebuilt the Stitch visual direction as a React/Vite application rather than keeping separate static HTML pages.
- Added React Router for the landing page and ML workspace.
- Added light theme as the default and a persistent dark-theme toggle.
- Added Framer Motion workflow animation on the landing page.
- Added a responsive dashboard inspired by the Stitch dashboard screen.
- Added routed UI scaffolds for:
  - Dataset Management
  - Exploratory Data Analysis
  - Preprocessing
  - Model Training
  - Evaluation
  - Model Comparison
  - Prediction
  - Explainable AI
  - Reports
  - History
- Added reusable Logo, Navbar, ThemeToggle and Workspace Shell components.
- Added reduced-motion support and visible focus behavior.

## Source material

The uploaded Stitch package contains the original `code.html` pages and `screen.png` references. This Phase 1 implementation keeps their terminology and workflow while moving the UI into a maintainable React structure.

## Run

```bash
npm install
npm run dev
```

Then open the Vite URL shown in the terminal.

## Important

Phase 1 is frontend-only. Dataset ingestion, Python/AI execution, persistence, authentication, real charts from data, and model training are not connected yet.

Planned pipeline:

Upload → Analysis → Preprocessing → Training → Evaluation → Comparison → Prediction → Explainable AI → Reports/History.
