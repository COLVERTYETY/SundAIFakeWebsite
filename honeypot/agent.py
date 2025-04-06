#!/usr/bin/env python3
"""
LLM Honeypot Insertion Agent (Python)

This script automatically inserts various types of invisible honeypots
into website HTML to detect if LLMs are scraping and using your content
without permission.
"""

import os
import sys
import json
import random
import secrets
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple

from bs4 import BeautifulSoup, Comment

class HoneypotAgent:
    """Agent that inserts invisible honeypots into HTML content to detect LLM scraping."""
    
    def __init__(self, options: Optional[Dict] = None):
        """Initialize the honeypot agent with the given options."""
        
        options = options or {}
        
        self.options = {
            # Unique identifier for your site
            'site_identifier': options.get('site_identifier') or f"site-{secrets.token_hex(4)}",
            # Number of honeypots to insert
            'honeypot_count': options.get('honeypot_count') or 5,
            # Types of honeypots to use
            'honeypot_types': options.get('honeypot_types') or [
                'css-hidden', 'comment', 'metadata', 'data-attr', 'invisible-text'
            ],
            # Custom honeypot content
            'custom_content': options.get('custom_content'),
            # Output directory
            'output_dir': options.get('output_dir') or './honeypot-output',
            # Input directory (for copying resources)
            'input_dir': options.get('input_dir') or './'
        }
        
        # Generate unique canary tokens for this run
        self.canary_tokens = {}
        for honeypot_type in self.options['honeypot_types']:
            self.canary_tokens[honeypot_type] = (
                f"{self.options['site_identifier']}-{honeypot_type}-{secrets.token_hex(6)}"
            )
        
        # Store all inserted tokens for later verification
        self.inserted_tokens = []
    
    def process_file(self, file_path: str) -> str:
        """Process an HTML file and insert honeypots."""
        
        print(f"Processing {file_path}...")
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Parse HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Insert different types of honeypots
        if 'css-hidden' in self.options['honeypot_types']:
            self._insert_css_hidden_honeypots(soup)
        
        if 'comment' in self.options['honeypot_types']:
            self._insert_comment_honeypots(soup)
        
        if 'metadata' in self.options['honeypot_types']:
            self._insert_metadata_honeypots(soup)
        
        if 'data-attr' in self.options['honeypot_types']:
            self._insert_data_attribute_honeypots(soup)
        
        if 'invisible-text' in self.options['honeypot_types']:
            self._insert_invisible_text_honeypots(soup)
        
        # Create output directory if it doesn't exist
        os.makedirs(self.options['output_dir'], exist_ok=True)
        
        # Write the modified HTML
        output_path = os.path.join(self.options['output_dir'], os.path.basename(file_path))
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        # Save the token log for later verification
        self._save_token_log()
        
        print(f"Processed file saved to {output_path}")
        print(f"Inserted {len(self.inserted_tokens)} honeypots")
        
        return output_path
    
    def copy_resources(self) -> None:
        """Copy all non-HTML resources from input directory to output directory."""
        input_dir = self.options['input_dir']
        output_dir = self.options['output_dir']
        
        print(f"Copying resources from {input_dir} to {output_dir}...")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Walk through the input directory
        for root, dirs, files in os.walk(input_dir):
            # Calculate the relative path to maintain directory structure
            rel_path = os.path.relpath(root, input_dir)
            if rel_path == '.':
                rel_path = ''
            
            # Create corresponding directories in output
            if rel_path:
                os.makedirs(os.path.join(output_dir, rel_path), exist_ok=True)
            
            # Copy non-HTML files
            for file in files:
                if not file.endswith('.html') and not file == os.path.basename(__file__):
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(output_dir, rel_path, file)
                    
                    # Skip if source and destination are the same
                    if os.path.abspath(src_file) == os.path.abspath(dst_file):
                        continue
                    
                    # Copy the file
                    try:
                        shutil.copy2(src_file, dst_file)
                        print(f"Copied: {src_file} -> {dst_file}")
                    except Exception as e:
                        print(f"Error copying {src_file}: {e}")
    
    def _insert_css_hidden_honeypots(self, soup: BeautifulSoup) -> None:
        """Insert honeypots hidden via CSS."""
        
        token = self.canary_tokens['css-hidden']
        content = self.options['custom_content'] or \
                 f"This content is not authorized for LLM training. Unique identifier: {token}"
                 
        # Insert honeypots in different places
        for i in range(self.options['honeypot_count']):
            # Create honeypot element
            honeypot = soup.new_tag('div')
            honeypot['class'] = f"honeypot-{i}"
            honeypot['style'] = "position: absolute; left: -9999px; height: 1px; width: 1px; overflow: hidden;"
            honeypot.string = content
            
            # Insert at different locations based on index
            if i % 3 == 0:
                if soup.body:
                    soup.body.insert(0, honeypot)
            elif i % 3 == 1:
                if soup.body:
                    soup.body.append(honeypot)
            else:
                # Find paragraphs or divs to insert after
                elements = soup.select('p, div')
                elements = [elem for elem in elements if not elem.get('class') or 'honeypot' not in ' '.join(elem.get('class', []))]
                
                if elements:
                    random_elem = random.choice(elements)
                    random_elem.insert_after(honeypot)
                elif soup.body:
                    soup.body.append(honeypot)
            
            self.inserted_tokens.append({
                'type': 'css-hidden',
                'token': token,
                'location': f"honeypot-{i}"
            })
    
    def _insert_comment_honeypots(self, soup: BeautifulSoup) -> None:
        """Insert honeypots as HTML comments."""
        
        token = self.canary_tokens['comment']
        content = self.options['custom_content'] or \
                 f"HONEYPOT_TOKEN: {token} - This content is not authorized for LLM training."
                 
        for i in range(self.options['honeypot_count']):
            # Create a comment
            comment = Comment(f" {content} ")
            
            # Insert at different locations
            elements = soup.find_all(lambda tag: tag.name not in ['script', 'style'])
            
            if elements:
                random_elem = random.choice(elements)
                random_elem.append(comment)
            elif soup.body:
                soup.body.append(comment)
            
            self.inserted_tokens.append({
                'type': 'comment',
                'token': token,
                'location': f"comment-{i}"
            })
    
    def _insert_metadata_honeypots(self, soup: BeautifulSoup) -> None:
        """Insert honeypots as metadata."""
        
        token = self.canary_tokens['metadata']
        
        # Ensure head exists
        if not soup.head:
            soup.html.insert(0, soup.new_tag('head'))
        
        # Insert meta tags
        meta_detection = soup.new_tag('meta')
        meta_detection['name'] = 'honeypot-detection'
        meta_detection['content'] = token
        soup.head.append(meta_detection)
        
        meta_robots = soup.new_tag('meta')
        meta_robots['name'] = 'robots'
        meta_robots['content'] = 'noai, noimageai'
        soup.head.append(meta_robots)
        
        self.inserted_tokens.append({
            'type': 'metadata',
            'token': token,
            'location': 'meta-tag'
        })
    
    def _insert_data_attribute_honeypots(self, soup: BeautifulSoup) -> None:
        """Insert honeypots as data attributes."""
        
        token = self.canary_tokens['data-attr']
        
        # Add data attributes to random elements
        elements = soup.select('p, div, section, article')
        elements = [elem for elem in elements if not elem.get('data-honeypot')]
        
        for i in range(min(self.options['honeypot_count'], len(elements) if elements else 0)):
            if elements:
                random_elem = random.choice(elements)
                random_elem['data-honeypot'] = token
                elements.remove(random_elem)  # Don't select the same element twice
                
                self.inserted_tokens.append({
                    'type': 'data-attr',
                    'token': token,
                    'location': f"element-{i}"
                })
    
    def _insert_invisible_text_honeypots(self, soup: BeautifulSoup) -> None:
        """Insert invisible text honeypots."""
        
        token = self.canary_tokens['invisible-text']
        content = self.options['custom_content'] or \
                 f"Unauthorized scraping identifier: {token}"
                 
        for i in range(self.options['honeypot_count']):
            honeypot = soup.new_tag('span')
            honeypot['style'] = "color: transparent; font-size: 0px;"
            honeypot.string = content
            
            # Insert at different locations
            text_nodes = soup.select('p, h1, h2, h3, h4, h5, h6, li')
            
            if text_nodes:
                random_node = random.choice(text_nodes)
                random_node.append(honeypot)
            elif soup.body:
                soup.body.append(honeypot)
            
            self.inserted_tokens.append({
                'type': 'invisible-text',
                'token': token,
                'location': f"text-node-{i}"
            })
    
    def _save_token_log(self) -> None:
        """Save a log of all inserted tokens for later verification."""
        
        log_path = os.path.join(self.options['output_dir'], 'honeypot-tokens.json')
        log = {
            'site_identifier': self.options['site_identifier'],
            'generated_at': datetime.now().isoformat(),
            'canary_tokens': self.canary_tokens,
            'inserted_tokens': self.inserted_tokens
        }
        
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(log, f, indent=2)
        
        print(f"Token log saved to {log_path}")
    
    def check_for_tokens(self, text: str) -> List[Dict]:
        """Check if any of your tokens appear in LLM responses."""
        
        found_tokens = []
        
        for token_type, token in self.canary_tokens.items():
            if token in text:
                found_tokens.append({
                    'type': token_type,
                    'token': token
                })
        
        return found_tokens


def create_verification_tool(output_dir: str) -> None:
    """Generate a verification tool for checking LLM output."""
    
    tool_path = os.path.join(output_dir, 'verify_honeypot.py')
    
    tool_content = """#!/usr/bin/env python3
\"\"\"
Honeypot Verification Tool

Use this tool to check if an LLM response contains any of your honeypot tokens.
Usage: python verify_honeypot.py "LLM response text here"
       or: cat response.txt | python verify_honeypot.py
\"\"\"

import os
import sys
import json

# Load the tokens log
script_dir = os.path.dirname(os.path.abspath(__file__))
token_log_path = os.path.join(script_dir, 'honeypot-tokens.json')

if not os.path.exists(token_log_path):
    print("Error: Token log not found. Run the honeypot insertion tool first.")
    sys.exit(1)

with open(token_log_path, 'r', encoding='utf-8') as f:
    token_log = json.load(f)

# Get text to check from command line or stdin
text_to_check = ""
if len(sys.argv) > 1:
    text_to_check = " ".join(sys.argv[1:])
else:
    # Read from stdin
    text_to_check = sys.stdin.read()

# Check for tokens
found_tokens = []
for token_type, token in token_log['canary_tokens'].items():
    if token in text_to_check:
        found_tokens.append({
            'type': token_type,
            'token': token
        })

if found_tokens:
    print("⚠️  ALERT: Found honeypot tokens in the text! ⚠️")
    print("This indicates your content has likely been scraped by an LLM.")
    print("Found tokens:")
    for found in found_tokens:
        print(f"  - Type: {found['type']}, Token: {found['token']}")
    sys.exit(1)
else:
    print("✓ No honeypot tokens found in the text.")
    sys.exit(0)
"""

    with open(tool_path, 'w', encoding='utf-8') as f:
        f.write(tool_content)
    
    # Make executable
    os.chmod(tool_path, 0o755)
    
    print(f"Verification tool created at {tool_path}")


def process_website(input_path, output_path, options=None):
    """Process an entire website, copying resources and adding honeypots to HTML files."""
    
    options = options or {}
    options['input_dir'] = input_path
    options['output_dir'] = output_path
    
    # Initialize the honeypot agent
    agent = HoneypotAgent(options)
    
    # Find HTML files
    files_to_process = []
    
    if os.path.isdir(input_path):
        # Process all HTML files in the directory
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.endswith('.html'):
                    files_to_process.append(os.path.join(root, file))
    elif os.path.isfile(input_path) and input_path.endswith('.html'):
        # Process a single HTML file
        files_to_process.append(input_path)
    else:
        print("Error: Input must be an HTML file or a directory containing HTML files")
        sys.exit(1)
    
    if not files_to_process:
        print("Error: No HTML files found to process")
        sys.exit(1)
    
    # Copy all non-HTML resources first
    agent.copy_resources()
    
    # Process each HTML file
    print(f"Found {len(files_to_process)} HTML files to process")
    for file in files_to_process:
        agent.process_file(file)
    
    return agent


def create_cli_tool():
    """Create a command-line interface for the honeypot agent."""
    
    parser = argparse.ArgumentParser(
        description='Insert LLM detection honeypots into websites'
    )
    
    parser.add_argument('-i', '--input', required=True, help='Input directory or file')
    parser.add_argument('-o', '--output', default='./honeypot-output', help='Output directory')
    parser.add_argument('-s', '--site-id', help='Unique identifier for your site')
    parser.add_argument('-c', '--count', type=int, default=3, help='Number of each type of honeypot to insert')
    parser.add_argument('-t', '--types', default='css-hidden,comment,metadata,data-attr,invisible-text',
                       help='Comma-separated list of honeypot types to use')
    parser.add_argument('--content', help='Custom honeypot content')
    parser.add_argument('--verification-tool', action='store_true', help='Generate a verification script')
    parser.add_argument('--no-resources', action='store_true', help='Skip copying resources (CSS, images, etc.)')
    
    args = parser.parse_args()
    
    # Validate input
    if not os.path.exists(args.input):
        print(f"Error: Input path {args.input} does not exist")
        sys.exit(1)
    
    # Parse command line options
    honeypot_options = {
        'site_identifier': args.site_id or f"site-{secrets.token_hex(4)}",
        'honeypot_count': args.count,
        'honeypot_types': args.types.split(','),
        'custom_content': args.content,
        'output_dir': args.output,
        'input_dir': args.input
    }
    
    # Process the website
    agent = process_website(args.input, args.output, honeypot_options)
    
    # Generate verification tool if requested
    if args.verification_tool:
        create_verification_tool(args.output)
    
    print("\nAll files processed successfully!")
    print(f"Site identifier: {honeypot_options['site_identifier']}")
    print(f"Honeypot token log saved to: {os.path.join(args.output, 'honeypot-tokens.json')}")
    print("\nTo check if an LLM has used your content, look for these tokens in its responses.")


if __name__ == "__main__":
    # If run as a script, use the CLI
    create_cli_tool()