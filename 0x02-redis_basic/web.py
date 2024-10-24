#!/usr/bin/env python3
""" Web cache and tracker """
import requests
import redis
from functools import wraps

# Connect to a local Redis instance
store = redis.Redis(host="localhost", port=6379, db=0)


def count_url_access(method):
    """Decorator counting how many times a URL is accessed"""

    @wraps(method)
    def wrapper(url):
        cached_key = f"cached:{url}"
        count_key = f"count:{url}"

        # Increment the access count
        store.incr(count_key)

        # Check if the URL content is cached
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        # Fetch the HTML content if not cached
        html = method(url)

        # Cache the HTML content with an expiration time of 10 seconds
        store.setex(cached_key, 10, html)
        return html

    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """Returns HTML content of a URL"""
    try:
        res = requests.get(url)
        res.raise_for_status()  # Raise an error for bad responses
        return res.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""
