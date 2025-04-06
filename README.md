# LLM Honeypot Agent (Python)

A Python tool that automatically inserts invisible honeypots into your website to detect if Large Language Models (LLMs) are scraping and using your content without permission.

## How It Works

The agent inserts unique "canary tokens" throughout your website in various invisible ways. These tokens are designed to be:

1. **Invisible to human visitors** - They won't affect the user experience
2. **Detectable in LLM outputs** - If an LLM scrapes your site and uses the content, these tokens may appear in its responses
3. **Uniquely identifiable** - Each token is specific to your site and the type of honeypot used

## Installation

### From PyPI (recommended)

```bash 
pip install llm-honeypot
```

### From Source

```bash
git clone https://github.com/yourusername/llm-honeypot
cd llm-honeypot
pip install -e .
```

## Dependencies

- Python 3.6+
- BeautifulSoup4

## Usage

### Command Line Interface

Process all HTML files in a directory:

```bash
llm-honeypot --input ./my-website --output ./protected-website
```

Process a single HTML file:

```bash
llm-honeypot --input ./index.html --output ./protected
```

### Advanced Options

```bash
# Customize the site identifier (used in generating unique tokens)
llm-honeypot --input ./my-website --site-id my-company-website

# Set the number of honeypots of each type to insert
llm-honeypot --input ./my-website --count 5

# Specify which honeypot types to use
llm-honeypot --input ./my-website --types css-hidden,comment,metadata

# Provide custom content for the honeypots
llm-honeypot --input ./my-website --content "This content is from example.com and not authorized for AI training."

# Generate a verification tool
llm-honeypot --input ./my-website --verification-tool
```

### Programmatic Usage

You can also use the honeypot agent as a Python library:

```python
from honeypot.agent import HoneypotAgent

# Create an agent with custom options
agent = HoneypotAgent({
    'site_identifier': 'my-blog',
    'honeypot_count': 3,
    'honeypot_types': ['css-hidden', 'comment', 'invisible-text'],
    'custom_content': 'Content from example.com - not authorized for AI training.'
})

# Process HTML files
agent.process_file('./blog/index.html')

# Later, check if an LLM response contains your tokens
llm_output = "Here's some generated text..."
found_tokens = agent.check_for_tokens(llm_output)

if found_tokens:
    print('ALERT: Found evidence of unauthorized content scraping!')
    print(found_tokens)
```

## Honeypot Types

The tool can insert several types of honeypots:

1. **css-hidden**: Content hidden using CSS techniques (position off-screen, zero height/width, etc.)
2. **comment**: HTML comments containing canary tokens
3. **metadata**: Meta tags with unique identifiers
4. **data-attr**: Data attributes added to HTML elements
5. **invisible-text**: Text with zero font size or transparent color

## Checking for Unauthorized Usage

After processing your site:

1. Deploy the protected version of your website
2. A JSON file (`honeypot-tokens.json`) is generated in the output directory containing all the tokens inserted into your site
3. To detect if an LLM has used your content without permission, check if any of these tokens appear in its responses

If you generated a verification tool:

```bash
# Check a file containing LLM output
python verify_honeypot.py < llm-response.txt

# Or pass text directly
python verify_honeypot.py "Here is some text that might contain your tokens..."
```

## Limitations

- Honeypots may not be effective against all LLM systems, especially those with advanced data cleaning pipelines
- This is a detection mechanism, not a prevention mechanism
- Some very aggressive data cleaning might remove these tokens
- False positives are possible but unlikely due to the uniqueness of the generated tokens

## Legal Considerations

This tool is intended for legitimate use in detecting unauthorized use of your content. Please ensure you have legal rights to the website you're modifying, and consider adding explicit terms of service prohibiting scraping your site for AI training.

## License

MIT