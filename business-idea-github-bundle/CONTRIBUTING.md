
# Contributing

Thanks for your interest!

## Run locally (Windows)

```cmd
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py app.py
```

## Guidelines
- Python 3.10+
- Keep functions small and documented.
- If you change method signatures, keep the Gradio UI defensive calls or update them.
- If you add dependencies, update `requirements.txt`.
