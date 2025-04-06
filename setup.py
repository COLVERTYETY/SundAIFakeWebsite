from setuptools import setup, find_packages

setup(
    name="llm-honeypot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4>=4.9.0",
    ],
    entry_points={
        "console_scripts": [
            "llm-honeypot=honeypot.agent:create_cli_tool",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Tool to insert invisible honeypots into websites to detect LLM scraping",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/llm-honeypot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
