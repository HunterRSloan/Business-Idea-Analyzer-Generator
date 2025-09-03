# 💡 Business Idea Analyzer & Generator — Gradio Demo

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-informational.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
<!-- Replace USER/SPACE with your actual Space to activate this badge -->
[![Open in 🤗 Spaces](https://img.shields.io/badge/%F0%9F%A4%97-Open%20in%20Spaces-blue)](https://huggingface.co/spaces/USER/SPACE)

Generate business ideas and assess feasibility via a simple Gradio UI.  
The app tries to import your project's `BusinessIdeaGenerator` and gracefully falls back to a lightweight stub if imports fail, so the demo always runs.

---

## ✨ Features
- **Generate Ideas**: industry + target market → ranked ideas with optional scores/rationale.
- **Assess Idea**: feasibility summary + raw JSON output.
- **Batch Assess (CSV)**: upload ideas to score at once and download a results file.
- **Environment-ready**: reads `.env` locally and **HF Spaces Variables** in production.

---

## 🖥️ Quickstart (Windows)

```cmd
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py app.py
```
Open the printed local URL.  
**Temporary public link**: edit the bottom of `app.py` to use `demo.launch(share=True)`.

---

## 🚀 Deploy to Hugging Face Spaces

1. Create a new Space → **SDK = Gradio**.
2. Upload `app.py` and `requirements.txt` (README optional).
3. Go to **Settings → Variables** and add any secrets your code uses (e.g., `OPENAI_API_KEY`, `NEWS_API_KEY`).
4. Click **Restart this Space** if needed.

**Badge:** After your Space exists, replace `USER/SPACE` in the badge at the top of this README with your handle:

```md
[![Open in 🤗 Spaces](https://img.shields.io/badge/%F0%9F%A4%97-Open%20in%20Spaces-blue)](https://huggingface.co/spaces/<your-username>/<your-space-name>)
```

---

## 📦 Batch CSV format
Upload a CSV with columns:
```
idea[, initial_investment, target_roi, industry, target_market]
```
A sample file `business_batch_sample.csv` is included.

---

## 🔌 Environment variables
- Put secrets in a local `.env` (gitignored) or in HF Spaces → Settings → Variables.
- See `.env.example` for names used by typical integrations.

---

## 🧩 Project structure
```
.
├─ app.py
├─ requirements.txt
├─ README.md
├─ .env.example
├─ business_batch_sample.csv
├─ LICENSE
├─ .gitignore
└─ (your project modules providing BusinessIdeaGenerator)
```

---

## 📝 Notes
- The UI first tries: `from business_idea_analyzer import BusinessIdeaGenerator` then `from business_generator import BusinessIdeaGenerator`.
- If signatures differ, the code retries calls without optional args so variants still work.
- For production, prefer a fixed package layout and pinned versions.

---

## ⚖️ License
[MIT](./LICENSE)
