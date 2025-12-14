# **404** Writeup

| Challenge | 404 |
| :------- | :----- |
| Difficulty | Easy |
| Category | Web |

# Challenge Overview
404 Description Not Found

# Code Analysis
We are given the Python file that the server logic runs on.
```python
from flask import Flask, make_response, render_template_string
import base64
import textwrap
import os

app = Flask(__name__)
flag = os.getenv("FLAG")

CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE'))
chunks = [flag[i:i+CHUNK_SIZE] for i in range(0, len(flag), CHUNK_SIZE)]
NUM_CHUNKS = len(chunks)

TEMPLATE = textwrap.dedent('''
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>404 Not Found</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        body { font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; display:flex; height:100vh; align-items:center; justify-content:center; background:#0f172a; color:#e6eef8; }
        .card { background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02)); padding:32px; border-radius:12px; box-shadow: 0 6px 30px rgba(2,6,23,0.6); max-width:720px; }
        pre { white-space:pre-wrap; word-wrap:break-word }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>404 — Nothing to see here</h1>
            <p>We couldn't find the page you requested: <strong>{{ path }}</strong></p>
            <p>If you think this is a mistake, try the homepage.</p>
            <hr>
            <small>Contact support at <em>noreply@example.com</em> if you believe this to be an error.</small>
        </div>
    </body>
</html>

''')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'HEAD'])
def catch_all(path):
    last_segment = path.split('/')[-1] if path else ''
    idx = None
    try:
        idx = int(last_segment)
    except Exception:
        idx = None

    if idx is not None and 0 <= idx < NUM_CHUNKS:
        raw = chunks[idx].encode('utf-8')
        b64 = base64.b64encode(raw).decode('utf-8')
        etag_val = f'W/"chunk{idx}-{b64}"'
    else:
        etag_val = 'W/"not-found"'

    resp = make_response(render_template_string(TEMPLATE, path='/' + path), 404)
    resp.headers['ETag'] = etag_val
    resp.headers['X-404-Reason'] = 'Missing, probably moved'
    return resp
```

## What it does:
This is code for a web page that always returns a 404 page, regardless of the URL. Therefore it can be accessed using a web browser *(duh)*.
# Vulnerability
Seen in the headers of the page, you can see an unusual header, `X-404-Reason` saying `Missing, probably moved`, along with a weak `ETag` saying `W/"not-found"`. 

On certain endpoints, parts of the flag are leaked. This is what you need to abuse.
## Solution
The endpoints aforementioned are `/0`, `/1` and so on (the amount of endpoints depends on the flag size). As seen in the code, each endpoint contains a **base64 encoded** text of 6 flag characters (default of `CHUNK_SIZE`, can be controlled within the ENV).

Send `HEAD` requests to each endpoint, get the `ETag` value and decode it piece by piece.
`curl -I <ip>:<port>/0`
`curl -I <ip>:<port>/1` 
*(and so on...)*

# Flag
```
flag{th1s_he4d3r_w4s_n0t_f0und!}
```