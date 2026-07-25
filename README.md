# Flask Fundamentals

Hands-on practice repo for learning Flask — building toward backend system design and REST API fundamentals.

Part of a structured internship-prep program (Phase 2). Each "Day" folder/commit represents one focused session, tested against real HTTP traffic via `curl`.

## Progress

### Day 1 — Routing Basics
- WSGI request-response cycle
- Static routes (`@app.route('/path')`)
- Dynamic routes with URL parameters (`<param>`)
- Handling POST bodies via `request.json`
- Tested manually using `curl.exe` (Windows PowerShell + curl JSON body via `-d "@body.json"` workaround for quoting issues)

## Running Locally

```bash
pip install flask
python app.py
```

Server runs on `http://127.0.0.1:5000` by default.

### Example requests

```bash
# GET example
curl http://127.0.0.1:5000/

# GET with dynamic param
curl http://127.0.0.1:5000/user/123

# POST with JSON body (Windows-safe method)
curl.exe -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d "@body.json"
```

## Notes

- On Windows, PowerShell 5.1 mangles inline JSON in `curl -d`, even when quoted correctly — write the JSON to a file (e.g. `body.json`) and pass it with `-d "@body.json"` instead.

## Roadmap

- [ ] Day 2 — (add once decided: query params / error handling / templates / etc.)
- [ ] Flask-SQLAlchemy basics
- [ ] REST API design patterns
- [ ] Deployment basics

---
Part of a multi-phase self-directed backend engineering prep program.
