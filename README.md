# Flask Fundamentals

Hands-on practice repo for learning Flask — building toward backend system design and REST API fundamentals.

Part of a structured internship-prep program (Phase 2). Each "Day" represents one focused session, tested against real HTTP traffic via `curl` and browser `fetch()`.

## Progress

### Day 1 — Routing Basics
- WSGI request-response cycle
- Static routes (`@app.route('/path')`)
- Dynamic routes with URL parameters (`<param>`)
- Handling POST bodies via `request.json`
- Tested manually using `curl.exe` (Windows PowerShell + curl JSON body via `-d "@body.json"` workaround for quoting issues)

### Day 2 — In-Memory CRUD API
- Full CRUD on `/items`: `POST`, `GET` (all), `GET` by id, `DELETE`
- Input validation with correct status codes (`400` invalid input, `201` created, `404` not found)
- Four real bugs found and fixed independently:
  - Validation running in the wrong order relative to input parsing
  - `NameError` from incorrect id-generation variable scope
  - Used `.pop()` where `.remove()` was needed (index vs. value semantics)
  - URL parameter type mismatch — fixed using the `<int:id>` route converter
- Tested via `curl` and browser DevTools `fetch()`

## Running Locally

```bash
pip install flask
python app.py
```

Server runs on `http://127.0.0.1:5000` by default.

### Example requests

```bash
# GET all items
curl http://127.0.0.1:5000/items

# GET a single item by id
curl http://127.0.0.1:5000/items/1

# POST a new item (Windows-safe method)
curl.exe -X POST http://127.0.0.1:5000/items -H "Content-Type: application/json" -d "@body.json"

# DELETE an item by id
curl.exe -X DELETE http://127.0.0.1:5000/items/1
```

## Notes

- On Windows, PowerShell 5.1 mangles inline JSON in `curl -d`, even when quoted correctly — write the JSON to a file (e.g. `body.json`) and pass it with `-d "@body.json"` instead.

## Roadmap

- [x] Day 1 — Routing basics
- [x] Day 2 — In-memory CRUD API
- [ ] Wire into real HTTP calls against `api-data-fetcher` (live endpoints, not in-memory)
- [ ] Error handling patterns + Flask-specific pytest tests
- [ ] Flask-SQLAlchemy basics
- [ ] Deployment basics

---
Part of a multi-phase self-directed backend engineering prep program.