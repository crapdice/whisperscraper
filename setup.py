from setuptools import setup, find_packages

setup(
    name="whisperscraper",
    version="0.1.0",
    description="A stealth-focused web scraping library.",
    author="Antigravity",
    packages=find_packages(),
    install_requires=[
        "requests",
        "playwright",
        "curl_cffi" 
    ],
    python_requires=">=3.8",
)
