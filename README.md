# WhisperScraper 🤫

**WhisperScraper** is a lightweight, stealth-focused Python library designed to bypass modern anti-bot systems. Unlike massive frameworks that try to do everything, WhisperScraper provides modular, "drop-in" tools to harden your existing `requests` or `playwright` scripts against detection.

## ⚡ Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/crapdice/whisperscraper.git
```

*Note: For TLS masquerading features, ensure you have `curl_cffi` installed (`pip install curl_cffi`).*

---

## 🎯 Core Capabilities

| Module | Purpose | Key Function | Why Use It? |
| :--- | :--- | :--- | :--- |
| **`tls`** | **Network Identity** | `create_tls_session()` | Bypasses JA3/JA4 fingerprinting by mimicking real Chrome/Safari SSL handshakes. |
| **`stealth`** | **Browser Fingerprint** | `stealth_spoof_canvas()` | Injects randomized noise into Canvas/Audio APIs to prevent consistent device tracking. |
| **`stealth`** | **Behavior** | `human_type()` | Simulates realistic human typing speeds, mistakes, and corrections to defeat behavioral analysis. |
| **`headers`** | **Request Hygiene** | `get_random_headers()` | Rotates modern, realistic User-Agents and matching HTTP headers. |

---

## 📖 Usage Guide

### 1. The Network Layer (Requests)

Most simple bots are blocked because their SSL handshake says "I am Python", even if their User-Agent says "I am Chrome".

#### ✅ The Fix: TLS Masquerading
Use `create_tls_session` to drop in a replacement for `requests.Session` that impersonates a real browser at the packet level.

```python
from whisperscraper.tls import create_tls_session

# Impersonate Chrome 120 (mimics the exact SSL Ciphers & Extensions)
session = create_tls_session(impersonate="chrome120")

# Use just like a normal requests session
response = session.get("https://incredibly-protected-site.com")
print(response.status_code)
```

### 2. The Browser Layer (Playwright)

Headless browsers leak information (like `navigator.webdriver = true`) and have consistent hardware fingerprints (Canvas, WebGL) that make them easy to track.

#### ✅ The Fix: Fingerprint Spoofing
Inject scripts that add tiny amounts of random noise to hardware APIs. This makes your bot look like a unique user every session, rather than a consistent bot.

```python
from playwright.async_api import async_playwright
from whisperscraper.stealth import (
    stealth_mask_webdriver, 
    stealth_spoof_canvas, 
    stealth_spoof_audio
)

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Apply stealth masks BEFORE loading the page
        await stealth_mask_webdriver(page)  # Hides 'navigator.webdriver'
        await stealth_spoof_canvas(page)    # Randomizes Canvas readout
        await stealth_spoof_audio(page)     # Randomizes AudioContext readout

        await page.goto("https://bot.sannysoft.com")
        await browser.close()
```

### 3. The Behavioral Layer (Interaction)

Anti-bot vendors (like Cloudflare Turnstile or reCAPTCHA v3) analyze *how* you interact. Instant clicking and text injection are red flags.

#### ✅ The Fix: Human Emulation
Simulate the messy reality of human input: mouse jitter, variable typing speeds, and typos.

```python
from whisperscraper.stealth import human_type, human_mouse_move

# inside your playwright async function...

# Move mouse in a human-like curve (Bezier) with random jitter
await human_mouse_move(page)

# Type with random delays and occasional backspace corrections
await human_type(page, "#search-input", "premium organic bananas")
```

### 4. Utilities

#### Google Cache Passthrough
Sometimes the best way to bypass a WAF is to not hit it at all.

```python
from whisperscraper.utils import get_google_cache_url

target = "https://www.nytimes.com/section/technology"
safe_url = get_google_cache_url(target)

# safe_url is now: http://webcache.googleusercontent.com/search?q=cache:...
print(f"Scraping static snapshot from: {safe_url}")
```

---

## 🛡️ "Grey Hat" Engineering

This library implements techniques discussed in our [Bot Evasion Techniques Guide](bot_evasion_techniques.html). It focuses on **emulation over evasion**—instead of trying to hide, we try to blend in.

*Disclaimer: This library is for educational and testing purposes. Ensure you comply with the Terms of Service of any website you interact with.*
