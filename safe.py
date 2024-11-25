import re
from urllib.parse import urlparse
import ssl
import socket
import requests
import os
from dotenv import load_dotenv


load_dotenv()

GOOGLE_SAFE_BROWSING_API_KEY = os.getenv('GOOGLE_SAFE_BROWSING_API_KEY')


MALICIOUS_DOMAINS=['evil.com', 'malware.com', 'phishing.net']

def is_valid_url(url):
    regex=re.compile(
      r'^(?:http|ftp)s?://'  # Protocol
      r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Domain
      r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
      r'(?::\d+)?'  # Port
      r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    return re.match(regex,url)is not None


#Check the ssl certification of a url

def check_ssl(url):
    parsed_url=urlparse(url)
    hostname=parsed_url.hostname

    try:
        context=ssl.create_default_context()
        with socket.create_connection((hostname,443)) as sock:
            with context.wrap_socket(sock,server_hostname=hostname)as secure_sock:
                secure_sock.getpeercert
        return True
    except:
        return False
    

def check_url_with_goggle_safebrowsing(url):
    api_url=f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_SAFE_BROWSING_API_KEY}"
    payload={
        "client": {
            "clientId": "your-app-name",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    response=requests.post(api_url,json=payload)
    result=response.json()
    return result.get("matches") is None  # Returns True if no threats are found

# Combine all checks into a single function
def check_link_safety(url):
    results = {
        'valid_url': False,
        'not_malicious': False,
        'has_ssl': False,
        'google_safe': False
    }

    # Check URL validity
    results['valid_url'] = is_valid_url(url)
    if not results['valid_url']:
        return False, "Invalid URL format", results

    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Check against malicious domains
    results['not_malicious'] = domain not in MALICIOUS_DOMAINS
    if not results['not_malicious']:
        return False, "Domain is in the list of known malicious websites", results

    # Check SSL certificate
    results['has_ssl'] = check_ssl(url)
    if not results['has_ssl']:
        return False, "Invalid or missing SSL certificate", results

    # Check with Google Safe Browsing API
    results['google_safe'] = check_url_with_goggle_safebrowsing(url)
    if not results['google_safe']:
        return False, "URL is flagged as unsafe by Google Safe Browsing", results

    return True, "The link appears to be safe", results




