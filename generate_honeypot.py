import os
import openai
from datetime import datetime

import os
from openai import OpenAI
from datetime import datetime

# Create a client using your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_fake_content(html_content):
    """
    Sends the file content to the LLM, instructing it to preserve 
    functionality but add invisible/fake content for anti-scraping.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-3.5-turbo"
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a web developer generating fake/invisible HTML content to"
                    " protect against naive web scrapping. You will be given the entire"
                    " HTML file content and should keep all current functionality intact,"
                    " but add random fake/invisible HTML comments, sections, phone numbers,"
                    " emails, names, and text that appear plausible."
                )
            },
            {
                "role": "user",
                "content": (
                    "Here is the file content:\n\n"
                    f"{html_content}\n\n"
                    "Add at least 20 invisible or hidden fake elements such as:\n"
                    "- Comments with fake phone numbers, emails, or names\n"
                    "- <div style=\"display:none\"> elements with random text\n"
                    "- <span hidden> tags\n"
                    "- Multiple realistic-looking but fake content blocks\n"
                    "Return the full modified HTML file."
                )
            }
        ],
        temperature=0.9,
        max_tokens=4096,  # Adjust as needed, but be cautious of token limits
    )
    return response.choices[0].message.content


def main():
    docs_folder = "docs"
    
    # Get all files in the docs folder
    for filename in os.listdir(docs_folder):
        # Adjust this condition if you only want to modify .html files
        if filename.endswith(".html"):
            file_path = os.path.join(docs_folder, filename)
            
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()
            
            # Send content to LLM for modification
            updated_content = generate_fake_content(original_content)
            
            # Write the modified content back to the file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            
            print(f"{filename} updated with fake content on {datetime.now()}")

if __name__ == "__main__":
    main()
