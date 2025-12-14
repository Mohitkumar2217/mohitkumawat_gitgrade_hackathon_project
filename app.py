from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import subprocess
import sys

app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>GitHub Repo Analyzer</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            padding: 40px;
        }}
        .box {{
            background: white;
            padding: 20px;
            max-width: 800px;
            margin: auto;
            border-radius: 8px;
        }}
        input {{
            width: 80%;
            padding: 10px;
        }}
        button {{
            padding: 10px 20px;
        }}
        pre {{
            background: #eee;
            padding: 15px;
            white-space: pre-wrap;
        }}
    </style>
</head>
<body>
    <div class="box">
        <h2>GitHub Repository Analyzer</h2>
        <form method="post">
            <input name="repo_url" placeholder="https://github.com/user/repo" required />
            <button type="submit">Analyze</button>
        </form>
        <pre>{result}</pre>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE.format(result="")

@app.post("/", response_class=HTMLResponse)
def analyze(repo_url: str = Form(...)):
    try:
        output = subprocess.check_output(
            [sys.executable, "repo_analyzer.py", repo_url],
            stderr=subprocess.STDOUT,
            text=True
        )
    except subprocess.CalledProcessError as e:
        output = e.output

    return HTML_PAGE.format(result=output)
