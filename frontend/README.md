# Pagebound frontend

Plain HTML/CSS/JS (no build step) that talks to the FastAPI backend.

```
frontend/
  index.html     products, search, sort, categories, cart drawer
  login.html     POST /login
  register.html  POST /register
  css/style.css
  js/config.js   <- API base URL lives here
  js/common.js   api helper, session, cart, header
  js/index.js    products page logic
  js/auth.js     login + register forms
```

## Run
1. Start the backend: `uvicorn main:app --reload` (http://127.0.0.1:8000)
2. Serve this folder: `python -m http.server 5500` inside `frontend/`, then open http://127.0.0.1:5500
   (or use the VS Code "Live Server" extension)

## Backend must-haves
- CORS, otherwise the browser blocks every request:
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_methods=["*"], allow_headers=["*"])
```
- Optional product fields the UI already understands: `price`, `description`, `category`, `image_url`.
  Without them the cards just show the name on a generated cover.
