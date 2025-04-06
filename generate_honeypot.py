import openai
import os
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = "Generate fake but realistic HTML comments and invisible elements (e.g., <div style='display:none'>) about tech topics or products. Include fake emails, fake names so that a naive scraping of the website results in fake information overload"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

fake_content = response['choices'][0]['message']['content']

# Inject into your HTML file
html_path = "./docs/index.html"
with open(html_path, "a") as f:
    f.write(f"\n<!-- Fake Content Generated  @ {datetime.now()} -->\n")
    f.write(fake_content)
