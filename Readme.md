# 🚀 GitHub Repository Analyzer

An **AI-powered developer profiling tool** that evaluates a public GitHub repository and converts it into a **Score, Summary, and Personalized Improvement Roadmap** — just like feedback from a senior engineering mentor.

This project is designed for **students, hackathons, mentors, and recruiters** to objectively assess real-world coding practices.

---

## 🎯 Problem It Solves

Most students push code to GitHub but don’t know:

* How clean or maintainable their code is
* Whether the project looks professional to recruiters
* What exactly to improve next

This tool acts as a **Repository Mirror** — reflecting strengths, weaknesses, and next steps using real GitHub data.

---

## ✨ Features

* 🔗 Accepts any **public GitHub repository URL**
* 📂 Analyzes project structure (files & folders)
* 🧪 Detects presence of tests
* 📝 Evaluates README/documentation availability
* 📊 Reviews commit history & contribution consistency
* 🧠 Analyzes tech stack / language usage
* 🧮 Generates a **score (0–100)**
* 🏷️ Classifies level: **Beginner / Intermediate / Advanced**
* 🧭 Produces a **personalized improvement roadmap**

---

## 🛠️ Tech Stack

* **Python 3**
* **GitHub REST API**
* `requests` – API calls
* `radon` – code complexity metrics (extensible)
* `pygments` – syntax analysis (future use)

---

## 📦 Installation

```bash
pip install requests radon pygments
```

---

## ▶️ How to Run

```bash
python repo_analyzer.py https://github.com/username/repository
```

### Example

```bash
python repo_analyzer.py https://github.com/vercel/next.js
```

---

## 🔐 (Optional) GitHub Token Setup

GitHub limits unauthenticated API calls. To avoid rate limits:

1. Create a token: [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Scope required: `public_repo`
3. Set environment variable:

### Windows (PowerShell)

```powershell
setx GITHUB_TOKEN "your_token_here"
```

### macOS / Linux

```bash
export GITHUB_TOKEN=your_token_here
```

---

## 📊 Sample Output

```
===== Repository Evaluation =====
Project       : todo-app
Score         : 68/100
Level         : Intermediate

--- Summary ---
Clean structure, documentation missing, tests missing

--- Personalized Roadmap ---
1. Add a clear README.md with setup, usage, and screenshots
2. Introduce unit tests and basic test coverage
3. Commit more frequently with meaningful messages
4. Add CI/CD (GitHub Actions) for automated checks
```

---

## 🧭 Evaluation Criteria

| Dimension       | Description                     |
| --------------- | ------------------------------- |
| Code Structure  | File & folder organization      |
| Documentation   | README clarity and presence     |
| Testing         | Unit/integration test detection |
| Commits         | Frequency & consistency         |
| Tech Stack      | Language usage diversity        |
| Maintainability | Readability & extensibility     |

---

## 🚧 Known Limitations

* GitHub API may be blocked on some networks (college WiFi)
* Currently analyzes **top-level structure only**
* Deep code analysis can be extended via cloning fallback

---

## 🔮 Future Enhancements

* Local clone fallback when API is blocked
* File-level code quality & complexity scoring
* CI/CD detection (GitHub Actions)
* Web UI (FastAPI + React)
* PDF report generation
* Recruiter-style badge system (Bronze / Silver / Gold)

---

## 👨‍🏫 Ideal Use Cases

* 🎓 Students evaluating their GitHub projects
* 🧑‍🏫 Mentors reviewing mentee submissions
* 🏆 Hackathons / SIH / college evaluations
* 💼 Recruiters doing quick repo screening

---

## 🤝 Contribution

Pull requests are welcome! For major changes, please open an issue first.

---

## 📜 License

MIT License

---

> Built with ❤️ to help developers understand **where they stand and how to grow**.
