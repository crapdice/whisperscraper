from urllib.parse import quote

def get_google_cache_url(url):
    """
    Returns the Google Cache URL for a given target URL.
    Useful for retrieving static content without hitting the origin server.
    """
    return f"http://webcache.googleusercontent.com/search?q=cache:{quote(url)}"
