from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from urllib.parse import urlparse

def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url

def is_valid_robots_content(content):
    # Basic validation for common robots.txt lines (User-agent, Disallow, Allow, Sitemap)
    lines = content.splitlines()
    for line in lines:
        if line.strip().startswith(("User-agent", "Disallow", "Allow", "Sitemap", "Crawl-delay", "Host")):
            return True
    return False

def check_robots_txt(base_url):
    robots_url = base_url + "/robots.txt"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        # Send request with a User-Agent header to mimic a browser
        response = requests.get(robots_url, headers=headers, allow_redirects=True)

        # Check if the status code is 200 (OK)
        if response.status_code == 200:
            # Check if the content of the robots.txt follows standard patterns
            if is_valid_robots_content(response.text):
                return True
            else:
                return False  # Not a valid robots.txt format
        elif response.status_code == 404:
            return "robots.txt file not found"
        elif response.status_code == 403:
            return "access to robots.txt is forbidden"
        elif response.status_code == 529:
            return "server error"
        else:
            return f"unexpected status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Error checking robots.txt: {e}"

def get_website_info(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the title
    title = soup.title.string if soup.title else 'No title found'

    # Extract all headings (h1, h2, h3, etc.)
    headings = []
    for level in range(1, 7):  # h1 to h6
        for heading in soup.find_all(f'h{level}'):
            headings.append(heading.text.strip())

    return title, headings

def calculate_cosine_similarity(query, title, headings):
    # Combine the query, title, and headings into a single list
    documents = [query, title] + headings

    # Use TfidfVectorizer to convert the text to vectors
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()

    # Compute cosine similarity between the query and the title/headings
    query_vector = vectors[0]  # First vector is the query
    title_vector = vectors[1]  # Second vector is the title
    heading_vectors = vectors[2:]  # Remaining vectors are the headings

    # Calculate similarities
    title_similarity = cosine_similarity([query_vector], [title_vector]).flatten()[0]
    heading_similarities = cosine_similarity([query_vector], heading_vectors).flatten()

    return title_similarity, heading_similarities

def seo_grading(html_content, base_url, query=None):
    soup = BeautifulSoup(html_content, 'html.parser')
    query = query if query else soup.title.string if soup.title else 'No query provided'

    # Extract title and headings
    title, headings = get_website_info(html_content)

    # Calculate cosine similarities
    title_similarity, heading_similarities = calculate_cosine_similarity(query, title, headings)

    # Check robots.txt status
    robots_txt_status = check_robots_txt(base_url)

    # Extract meta tags
    meta_description = soup.find('meta', attrs={'name': 'description'})
    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})

    # Count images and alt text coverage
    images = soup.find_all('img')
    images_with_alt = [img for img in images if img.get('alt')]

    # Count internal and external links
    links = soup.find_all('a', href=True)
    internal_links = [link for link in links if urlparse(link['href']).netloc == urlparse(base_url).netloc]
    external_links = [link for link in links if urlparse(link['href']).netloc != urlparse(base_url).netloc]

    # Numerical Details
    numerical_data = {
        "title_similarity": {
            "title": "Title Similarity",
            "value": round(title_similarity, 2),
            "details": "Cosine similarity between the query and the webpage title."
        },
        "average_heading_similarity": {
            "title": "Average Heading Similarity",
            "value": round(sum(heading_similarities) / len(heading_similarities), 2) if heading_similarities else 0,
            "details": "Average cosine similarity between the query and all headings."
        },
        "robots_txt_status": {
            "title": "Robots.txt Validity",
            "value": 1 if robots_txt_status == True else 0,
            "details": "Indicates if robots.txt is valid (1 for Yes, 0 for No)."
        },
        "meta_description_presence": {
            "title": "Meta Description Presence",
            "value": 1 if meta_description else 0,
            "details": "Indicates if a meta description tag is present (1 for Yes, 0 for No)."
        },
        "meta_keywords_presence": {
            "title": "Meta Keywords Presence",
            "value": 1 if meta_keywords else 0,
            "details": "Indicates if a meta keywords tag is present (1 for Yes, 0 for No)."
        },
        "images_with_alt_ratio": {
            "title": "Alt Text Coverage",
            "value": round(len(images_with_alt) / len(images), 2) if images else 0,
            "details": "Ratio of images with alt text to total images."
        },
        "internal_links_count": {
            "title": "Internal Links Count",
            "value": len(internal_links),
            "details": "Number of links pointing to the same domain."
        },
        "external_links_count": {
            "title": "External Links Count",
            "value": len(external_links),
            "details": "Number of links pointing to external domains."
        }
    }

    # One-Liner Details
    one_liner_data = [
        {"title": "Title and Headings", 
        "details": f"High similarity ensures relevance to user queries and improves SEO by aligning content with search intent."},

        {"title": "Robots.txt File", 
        "details": f"A valid robots.txt file allows proper crawling and indexing of important pages, optimizing search engine efficiency."},

        {"title": "Meta Tags", 
        "details": f"Meta descriptions improve click-through rates, and although meta keywords are less relevant now, they indicate optimization efforts."},

        {"title": "Alt Text for Images", 
        "details": f"Proper alt text enhances accessibility, boosts image search rankings, and improves overall SEO by helping search engines interpret images."},

        {"title": "Internal vs External Links", 
        "details": f"Internal links aid navigation and distribute link equity, while external links add credibility and enrich content."},

        {"title": "SEO Readiness Score", 
        "details": f"This score aggregates performance across content relevance, accessibility, and technical optimization."}
    ]



    # Final Report
    return {
        "title": title,
        "headings": headings,
        "numerical_data": numerical_data,
        "one_liner_data": one_liner_data,
        "robots_txt_status": robots_txt_status,
        "meta_description": meta_description["content"] if meta_description else None,
        "meta_keywords": meta_keywords["content"] if meta_keywords else None
    }

