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
                    " emails and text that appear plausible."
                )
            },
            {
                "role": "user",
                "content": (
                    "Here is the file content:\n\n"
                    f"{html_content}\n\n"
                    "Add at least 50 invisible or hidden fake elements such as:\n"
                    "- Comments with fake phone numbers and emails.\n"
                    "- <div style=\"display:none\"> elements with random text\n"
                    "- <span hidden> tags\n"
                    "- Multiple realistic-looking but fake content blocks\n"
                    "Make sure to add a lot of fake content. Add long lists of email adresses. etc\n"
                    "Do not mension the fake data, do not mention web scrappers.\n"
                    "Do not  not include teh word fake.\n"
                    "Add invisible text where you ramble about organic mushroom farming.\n"
                    "Return the full modified HTML file.\n"
                    "Answer only with the modified HTML content file, make sure to keep all existing functionallities intact.\n"
                )
            }
        ],
        temperature=0.5,
        max_tokens=4096*2,  # Adjust as needed, but be cautious of token limits
    )
    return response.choices[0].message.content

def inject_hidden_names(html_content, names):
    """
    Injects hidden names into the HTML content using various techniques.
    """
    hidden_blocks = "\n".join([
        f'<span hidden>{name}</span>' for name in names
    ] + [
        f'<div style="display:none">{name}</div>' for name in names
    ] + [
        f'<!-- Name: {name} -->' for name in names
    ])
    
    # You can choose where to insert this — here we inject it before </body> if available
    if "</body>" in html_content:
        html_content = html_content.replace("</body>", hidden_blocks + "\n</body>")
    else:
        html_content += "\n" + hidden_blocks
    return html_content

def main():
    docs_folder = "docs"

    banned_names = ["Brian Hood", "Jonathan Turley", "Jonathan Zittrain", "David Faber", "David Mayer","Guido Scorza"]
    banned_names = banned_names * 10  # Repeat the list to ensure we have enough names to inject
    # Get all files in the docs folder
    for filename in os.listdir(docs_folder):
        # Adjust this condition if you only want to modify .html files
        if filename.endswith(".html"):
            file_path = os.path.join(docs_folder, filename)
            
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()
            
            # Send content to LLM for modification
            updated_content = generate_fake_content(original_content)
            # Check if the first line of the updated content includes "```html"
            if updated_content.startswith("```html"):
                updated_content = "\n".join(updated_content.split("\n")[1:])
            # Inject hidden names into the updated content
            updated_content = inject_hidden_names(updated_content, banned_names)
            # Write the modified content back to the file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            
            print(f"{filename} updated with fake content on {datetime.now()}")

if __name__ == "__main__":
    main()
