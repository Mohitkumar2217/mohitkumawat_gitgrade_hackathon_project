from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import subprocess
import sys

app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>GitHub Repo Analyzer</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-slate-900 to-slate-800 min-h-screen flex items-center justify-center text-slate-100">

  <div class="w-full max-w-3xl bg-slate-900/80 backdrop-blur rounded-xl shadow-xl p-8">
    
    <h1 class="text-3xl font-bold text-center mb-2">
      🚀 GitHub Repository Analyzer
    </h1>
    <p class="text-center text-slate-400 mb-6">
      Paste a public GitHub repo and get a score, summary & roadmap
    </p>

    <form method="post" class="flex gap-3 mb-6">
      <input
        name="repo_url"
        required
        placeholder="https://github.com/username/repository"
        class="flex-1 px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        class="px-6 py-3 rounded-lg bg-blue-600 hover:bg-blue-700 transition font-semibold"
      >
        Analyze
      </button>
    </form>

    <div class="bg-slate-800 border border-slate-700 rounded-lg p-4">
      <h2 class="font-semibold mb-2 text-blue-400">Analysis Output</h2>
      <pre class="text-sm whitespace-pre-wrap text-slate-200">{result}</pre>
    </div>

    <footer class="text-center text-xs text-slate-500 mt-6">
      Built with FastAPI + AI Code Analysis
    </footer>

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
