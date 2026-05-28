"""
Setup script for CAPTAIN AI
Install with: pip install -e .
Or publish: python setup.py sdist bdist_wheel
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="captain-ai",
    version="1.0.0",
    author="Captain AI",
    author_email="captain@example.com",
    description="⚓ Your AI Navigator for Web Intelligence - Search the web and get cited answers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/captaintharun0507/captain-ai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "duckduckgo-search>=3.8.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "streamlit>=1.28.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "captain=cli:main",
        ],
    },
    keywords="ai search web openai chatbot perplexity citations",
    project_urls={
        "Bug Reports": "https://github.com/captaintharun0507/captain-ai/issues",
        "Source": "https://github.com/captaintharun0507/captain-ai",
        "Documentation": "https://github.com/captaintharun0507/captain-ai#readme",
    },
)