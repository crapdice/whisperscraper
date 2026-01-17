# WhisperScraper

WhisperScraper is a lightweight, stealth-focused web scraping library for Python. It provides utilities to bypass common bot detection systems by simulating human behavior and randomizing browser fingerprints.

## Features

- **Randomized Headers & User-Agents**: Generate realistic browser headers to mimic real traffic.
- **Stealth Session**: A pre-configured `requests.Session` that handles cookies and headers automatically.
- **Playwright Stealth**:
  - **Human-Like Typing**: Simulate realistic typing with random delays and typos.
  - **Mouse Jitter**: Randomized mouse movements.
  - **Webdriver Masking**: Automatically hide the `navigator.webdriver` property.

## Installation

```bash
pip install .
```

## Usage

### 1. Requests (Stealth Session)

```python
from whisperscraper.session import create_stealth_session

session = create_stealth_session(referer="https://google.com")
response = session.get("https://example.com")
```

### 2. Playwright (Stealth Actions)

```python
from whisperscraper.stealth import human_type, human_mouse_move, stealth_mask_webdriver

# Inside your Playwright async function
await stealth_mask_webdriver(page)
await human_mouse_move(page)
await human_type(page, "#search-input", "my query")
```
