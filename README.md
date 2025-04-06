# 🕷️ SundAI LLM Honeypot Generator

This project injects misleading and invisible HTML content into webpages to protect against **naive web scrapers**. It uses **OpenAI's GPT models** to automatically generate and insert fake elements such as hidden `<div>`s, fake emails, phone numbers, and HTML comments, preserving the original page functionality while making it harder for bots to extract meaningful data.

---

## ✨ Features

- ✅ Automatically injects fake HTML content into all `.html` files in the `docs/` directory  
- ✅ Uses GPT-4 (or GPT-3.5-turbo) to generate realistic-looking fake data  
- ✅ Preserves all original content and functionality  
- ✅ Adds misleading elements like:
  - Hidden `<div>` and `<span>` blocks  
  - HTML comments with fake names/emails/phone numbers  
  - Invisible placeholder content  
- ✅ GitHub Actions workflow to automate content injection and PR creation

---

## 🧠 Why This Works

Naive web scrapers often rely on simple pattern matching and structural assumptions. By injecting:

- Comments with fake data
- Hidden but realistic-looking elements
- Obfuscated signals

...you can confuse and degrade the quality of the data collected by low-effort bots.

---

## 🧪 Example Fake Content


    <!-- Contact: lisa.rogers@protonmail.com | (408) 399-2828 -->
    <div style="display:none">Partner Login: shadow-access-27</div>
    <span hidden>Senior Developer: Alejandro Fuentes</span>


##  🛠️ Setup

1. Install Python Dependencies

    pip install openai

 2. Add Your OpenAI API Key
Set the environment variable in your terminal:

    export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx

Or define it as a GitHub Secret (OPENAI_API_KEY) if running in CI/CD.

🚀 Usage
To run locally:

    python generate_honeypot.py

This will:

Read all .html files in the docs/ folder

Use OpenAI to inject fake content

Overwrite the original files with the modified version

## ⚙️ GitHub Actions Automation
On every push to the main branch, the following workflow is triggered:

    .github/workflows/inject-fake-content.yml

#### 🔐 Secrets Needed
OPENAI_API_KEY: Your OpenAI API key (stored in GitHub Secrets)

# 🧰 Future Improvements

Image Poisining via NightShade to protect against image-based scraping

Add CLI options for batch size, verbosity, etc.

Scraper heuristics simulation for testing effectiveness

Additional fake formats (JSON-LD, microdata, etc.)


# 🧙‍♂️ Authors 🧑‍💻

Developed by Nicolas STAS, Ankit Baral, Anshul Agarwal, Mana Dhillon, Aleks Jakulin

Hacked together for SundAI — blending AI + deception to keep the web safe from bots.