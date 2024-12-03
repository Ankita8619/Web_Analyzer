import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import ssl
import socket
import re

def is_https(url):
    return urlparse(url).scheme == 'https'

def check_ssl_certificate(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                certificate = ssock.getpeercert()
                return True
    except Exception as e:
        return False

def extract_contact_info(soup):
    emails = set()
    phones = set()

    for text in soup.stripped_strings:
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            emails.add(text)

    for text in soup.stripped_strings:
        phones_found = re.findall(r'\+?\d[\d -]{8,}\d', text)
        phones.update(phones_found)

    return emails, phones

def find_policy_links(soup):
    policy_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'privacy' in href.lower() or 'policy' in href.lower():
            policy_links.append(urljoin(url, href))

    return policy_links

def find_login_signup_links(soup):
    login_signup_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'login' in href.lower() or 'signup' in href.lower() or 'register' in href.lower():
            login_signup_links.append(urljoin(url, href))

    return login_signup_links

def analyze_login_form(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    input_details = []

    # Find input fields
    inputs = soup.find_all('input')
    for input_field in inputs:
        input_details.append({"name": input_field.get('name'), "type": input_field.get('type')})

    # Check for CAPTCHA
    captcha_present = bool(soup.find('div', {'class': 'g-recaptcha'}))

    return {"input_details": input_details, "captcha_present": captcha_present}

# Function to inspect cookies and tokens
def inspect_cookies_and_tokens(session, login_url, username, password):
    login_payload = {'username': username, 'password': password}
    login_response = session.post(login_url, data=login_payload)

    cookies_info = []
    # Check cookies
    for cookie in session.cookies:
        cookies_info.append({
            "name": cookie.name, 
            "secure": cookie.secure, 
            "httpOnly": cookie.has_nonstandard_attr('HttpOnly')
        })

    jwt_used = False
    # Check for JWT tokens in headers
    auth_header = login_response.headers.get('Authorization')
    if auth_header and 'Bearer' in auth_header:
        jwt_used = True

    return {"cookies": cookies_info, "jwt_used": jwt_used}

def analyze_session_management(session):
    session_management_info = {}

    # Check session ID length and randomness
    session_id = session.cookies.get('sessionid')
    if session_id and len(session_id) > 20:
        session_management_info["session_id"] = "long and likely random"
    else:
        session_management_info["session_id"] = "short or not random"

    # Check session expiration
    session_cookie = session.cookies.get('sessionid', domain='bekushal.com')
    if session_cookie:
        session_expiry = session_cookie.expires
        if session_expiry:
            session_management_info["session_expiration"] = f"expires at: {session_expiry}"
        else:
            session_management_info["session_expiration"] = "not set"
    else:
        session_management_info["session_cookie"] = "not found"

    return session_management_info

# Function to perform authorization checks
def authorization_checks(session, protected_url):
    protected_response = session.get(protected_url)
    access_status = ""

    if protected_response.status_code == 403:
        access_status = "restricted based on user roles"
    elif protected_response.status_code == 200:
        access_status = "access granted"
    else:
        access_status = "unexpected response"

    return {"access_status": access_status}

# Function to review HTTP headers
def review_http_headers(response):
    headers = response.headers
    security_headers_info = {}

    security_headers = [
        'Strict-Transport-Security',
        'Content-Security-Policy',
        'X-Content-Type-Options',
        'X-Frame-Options'
    ]

    for header in security_headers:
        security_headers_info[header] = header in headers

    return security_headers_info
def scrape_payment_elements(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')

    emails, phones = extract_contact_info(soup)
    policy_links = find_policy_links(soup)
    login_signup_links = find_login_signup_links(soup)
    forms = soup.find_all('form')
    scripts = soup.find_all('script')

    payment_security = []

    for form in forms:
        form_action = form.get('action')
        if form_action:
            full_url = urljoin(base_url, form_action)
            payment_security.append({
                "form_action": full_url,
                "secured": is_https(full_url)
            })

            input_fields = form.find_all('input')
            for field in input_fields:
                if field.get('type') in ['text', 'password', 'number']:
                    if 'card' in field.get('name', '').lower() or 'cvv' in field.get('name', '').lower():
                        payment_security.append({
                            "sensitive_input_field": field.get('name'),
                            "form_action": full_url
                        })

    for script in scripts:
        script_src = script.get('src')
        if script_src:
            full_script_url = urljoin(base_url, script_src)
            payment_security.append({
                "script_url": full_script_url,
                "secured": is_https(full_script_url)
            })

    # Analyze login form
    login_form_results = analyze_login_form(html_content, base_url)

    return {
        "emails": list(emails),
        "phones": list(phones),
        "policy_links": policy_links,
        "login_signup_links": login_signup_links,
        "payment_security": payment_security,
        "login_form_analysis": login_form_results
    }


def web_security_report(html_content, base_url, session=None, username=None, password=None, protected_url=None):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Check if the website is HTTPS
    domain = urlparse(base_url).netloc
    https_status = is_https(base_url)
    ssl_status = check_ssl_certificate(domain)

    # Extract contact info
    emails, phones = extract_contact_info(soup)

    # Find policy links and login/signup links
    policy_links = find_policy_links(soup)
    login_signup_links = find_login_signup_links(soup)

    # Scrape payment elements
    payment_security = scrape_payment_elements(html_content, base_url)

    # Analyze login form
    login_form_results = analyze_login_form(html_content, base_url)

    # Session management and authorization checks
    cookies_info, jwt_used = {}, False
    session_management_info, authorization_info = {}, {}
    if session and username and password:
        cookies_tokens = inspect_cookies_and_tokens(session, base_url, username, password)
        cookies_info = cookies_tokens.get("cookies", [])
        jwt_used = cookies_tokens.get("jwt_used", False)
        session_management_info = analyze_session_management(session)
        authorization_info = authorization_checks(session, protected_url)

    # Review HTTP headers
    headers_info = {}
    if session:
        response = session.get(base_url)
        headers_info = review_http_headers(response)

    # Enhanced Numerical Details
    numerical_data = {
        "https_status": {
            "title": "HTTPS Status",
            "value": int(https_status),
            "details": "Whether the website uses HTTPS (1 for Yes, 0 for No)."
        },
        "ssl_status": {
            "title": "SSL Certificate Status",
            "value": int(ssl_status),
            "details": "Whether the domain has a valid SSL certificate (1 for Yes, 0 for No)."
        },
        "total_emails": {
            "title": "Total Emails Found",
            "value": len(emails),
            "details": "Number of email addresses identified on the website."
        },
        "total_phones": {
            "title": "Total Phone Numbers Found",
            "value": len(phones),
            "details": "Number of phone numbers identified on the website."
        },
        "policy_links_count": {
            "title": "Policy Links Count",
            "value": len(policy_links),
            "details": "Number of links related to policies (Privacy, Terms, etc.)."
        },
        "login_signup_links_count": {
            "title": "Login/Signup Links Count",
            "value": len(login_signup_links),
            "details": "Number of links pointing to login or signup pages."
        },
        "captcha_present": {
            "title": "CAPTCHA Presence in Login Forms",
            "value": int(login_form_results["captcha_present"]),
            "details": "Indicates if CAPTCHA is present in login forms (1 for Yes, 0 for No)."
        },
        "security_headers_count": {
            "title": "Security Headers Count",
            "value": sum(headers_info.values()) if headers_info else 0,
            "details": "Number of essential security headers found in HTTP responses."
        }
    }

    # Enhanced One-Liner Details
    one_liner_data = [
        {"title": "HTTPS and SSL Status", 
         "details": f"Website uses HTTPS: {'Yes' if https_status else 'No'}, SSL Certificate: {'Valid' if ssl_status else 'Invalid'}."},
        {"title": "Contact Information", 
         "details": f"Found {len(emails)} email(s) and {len(phones)} phone number(s)."},
        {"title": "Policy Links", 
         "details": f"Identified {len(policy_links)} link(s) to privacy or policy pages."},
        {"title": "Login and Signup Links", 
         "details": f"Discovered {len(login_signup_links)} login or signup-related link(s)."},
        {"title": "Payment Security", 
         "details": f"Detected {len(payment_security['payment_security'])} payment security-related element(s)."},
        {"title": "Login Form Analysis", 
         "details": f"Login form contains CAPTCHA: {'Yes' if login_form_results['captcha_present'] else 'No'}."},
    ]

    # Final Report
    return {
        "emails": list(emails),
        "phones": list(phones),
        "policy_links": policy_links,
        "login_signup_links": login_signup_links,
        "payment_security": payment_security,
        "login_form_analysis": login_form_results,
        "session_management_info": session_management_info,
        "authorization_info": authorization_info,
        "headers_info": headers_info,
        "numerical_data": numerical_data,
        "one_liner_data": one_liner_data
    }
