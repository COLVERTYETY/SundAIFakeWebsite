import os
from openai import OpenAI
from datetime import datetime

# Create a client using your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Generate fake content using GPT-4 or GPT-3.5
response = client.chat.completions.create(
    model="gpt-4",  # or "gpt-3.5-turbo"
    messages=[
        {"role": "system", "content": "You are a web developer generating fake/invisible HTML content."},
        {"role": "user", "content": "Generate a mix of realistic and absurd fake HTML comments and <div style='display:none'> sections, as if hidden on a corporate tech landing page."}
    ]
)

# Extract the generated content
fake_content = response.choices[0].message.content

# Inject the fake content into your HTML
html_path = "docs/index.html"
with open(html_path, "a") as f:
    f.write(f"\n<!-- Fake Content Generated {datetime.now()} -->\n")
    f.write(fake_content)
