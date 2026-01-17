import requests
from .headers import get_random_headers

def create_stealth_session(referer="https://www.google.com/"):
    """
    Creates a requests.Session() pre-configured with random anti-bot headers.
    """
    session = requests.Session()
    session.headers.update(get_random_headers(referer))
    return session
