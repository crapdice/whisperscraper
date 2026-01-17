try:
    from curl_cffi import requests as cffi_requests
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False
    import requests

def create_tls_session(impersonate="chrome120"):
    """
    Creates a session that impersonates a real browser's TLS fingerprint.
    
    Args:
        impersonate (str): The browser to impersonate (e.g., "chrome110", "safari15_3").
    
    Returns:
        Session: A curl_cffi session if installed, otherwise a standard requests Session (with a warning).
    """
    if HAS_CURL_CFFI:
        return cffi_requests.Session(impersonate=impersonate)
    else:
        print("WARNING: curl_cffi not installed. Using standard requests (No TLS Spoofing).")
        print("Run `pip install curl_cffi` to enable TLS masquerading.")
        return requests.Session()
