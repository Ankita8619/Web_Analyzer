from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import urllib.parse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json
from database import ScrapedContent, get_db
from colorgrading import color_grading_report
from scraper import (find_properties, extract_css_from_webpage)
import requests
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
from typing import Optional
from fastapi.staticfiles import StaticFiles
from content_style_grading import visual_consistency_report
from ads_recommendation import generate_text_report
from ads_data import ad_topic_mapping
from responsive import responsive
from Seo_grading import seo_grading
from web_security import web_security_report, review_http_headers, inspect_cookies_and_tokens, analyze_session_management, authorization_checks
from methods import (run_link_checker, fetch_webpage, parse_html, extract_css_js_files, evaluate_file_sizes)
from database import SessionLocal, engine, get_db, Base, User, Report
from passlib.context import CryptContext
import shutil
import os
import base64
import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ScrapeRequest(BaseModel):
    url: str
    feature: Optional[str] = None
    sub_feature: Optional[str] = None
    query: Optional[str] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterRequest(BaseModel):
    email: str
    password: str
    username: str
    user_details: str
    sub_details: str
    profession: str

class LoginRequest(BaseModel):
    email: str
    password: str

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/register")
async def register_user(
    email: str = Form(...),
    password: str = Form(...),
    username: str = Form(...),
    user_details: str = Form(...),
    sub_details: str = Form(...),
    profession: str = Form(...),
    image: UploadFile = File(None),  # Optional file
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_password = get_password_hash(password)
    new_user = User(
        email=email,
        username=username,
        password=hashed_password,
        user_details=user_details,
        sub_details=sub_details,
        profession=profession
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Save user image
    if image:
        image_path = f"static/{new_user.user_id}.jpg"
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    return {"message": "User registered successfully", "user_id": new_user.user_id}

@app.post("/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {
        "user_id": user.user_id,
        "email": user.email,
        "username": user.username,
        "user_details": user.user_details,
        "sub_details": user.sub_details,
        "profession": user.profession,
        "days_left": user.days_left,
        "created_at": user.created_at,
        "image": f"/static/{user.user_id}.jpg"
    }

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "user_id": user.user_id,
        "email": user.email,
        "username": user.username,
        "user_details": user.user_details,
        "sub_details": user.sub_details,
        "profession": user.profession,
        "days_left": user.days_left,
        "created_at": user.created_at,
        "image": f"/static/{user.user_id}.jpg"
    }
    

class ReportRequest(BaseModel):
    user_id: int
    feature: str
    sub_feature: str
    data: dict
    url: str

@app.post("/save_report")
async def save_report(report_request: ReportRequest, db: Session = Depends(get_db)):
    new_report = Report(
        user_id=report_request.user_id,
        feature=report_request.feature,
        sub_feature=report_request.sub_feature,
        data=report_request.data,
        url=report_request.url
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return {"message": "Report saved successfully", "report_id": new_report.report_id}

@app.get("/reports/{user_id}")
def get_reports(user_id: int, db: Session = Depends(get_db)):
    reports = db.query(Report).filter(Report.user_id == user_id).all()
    if not reports:
        raise HTTPException(status_code=404, detail="No reports found")
    return reports

@app.get("/report/{report_id}")
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {
        "report_id": report.report_id,
        "user_id": report.user_id,
        "feature": report.feature,
        "sub_feature": report.sub_feature,
        "url": report.url,
        "data": report.data,
    }



class Scraper:
    def __init__(self, url, db: Session):
        self.url = url
        self.db = db
        self.html_elements = ""
        self.elements_properties = {}
        self.css = ""
        self.body_content = ""

    def fetch_and_parse(self):
        response = requests.get(self.url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        self.body_content = soup.body.get_text(separator=' ', strip=True) if soup.body else ""
        self.html_elements = str(soup)
        self.css = extract_css_from_webpage(self.url)
        
        # Convert to a Python dictionary if find_properties returns a JSON string
        print(1)
        properties = find_properties(self.url, [
            'background-color', 'color', 'font-family', 'font-size', 'font-weight',
            'margin', 'padding', 'text-align', 'justify-content', 'align-items'
        ])
        print(2)
        
        if isinstance(properties, str):  # If properties is a JSON string, convert it
            print(3)
            self.elements_properties = json.loads(properties)
        else:
            print(4)
            self.elements_properties = properties

    def save_to_db(self):
        # Print the type and value of elements_properties and css before serialization
        print("Before serialization:")
        print(f"Type of elements_properties: {type(self.elements_properties)}")
        print(f"Value of elements_properties: {self.elements_properties}")
        print(f"Type of css: {type(self.css)}")
        print(f"Value of css: {self.css}")

        # Serialize if needed
        elements_properties_serialized = json.dumps(self.elements_properties) if isinstance(self.elements_properties, dict) else self.elements_properties
        css_serialized = json.dumps(self.css) if isinstance(self.css, (list, tuple)) else self.css

        # Print the type and value of elements_properties and css after serialization
        print("After serialization:")
        print(f"Type of elements_properties_serialized: {type(elements_properties_serialized)}")
        print(f"Value of elements_properties_serialized: {elements_properties_serialized}")
        print(f"Type of css_serialized: {type(css_serialized)}")
        print(f"Value of css_serialized: {css_serialized}")

        # Create the ScrapedContent object
        scraped_content = ScrapedContent(
            url=self.url,
            html_elements=self.html_elements,
            elements_properties=elements_properties_serialized,  # JSON serialization here
            css=css_serialized,  # Serialize tuple or list
            body_content=self.body_content,
            created_at=datetime.datetime.utcnow()
        )

        # Add to the session
        self.db.add(scraped_content)

        try:
            # Commit the transaction
            self.db.commit()
            # Refresh to get the updated instance (ID and other auto-generated fields)
            self.db.refresh(scraped_content)
        except Exception as e:
            # Rollback in case of error
            self.db.rollback()
            raise ValueError(f"Error during commit: {e}")

    def load_from_db(self):
        return self.db.query(ScrapedContent).filter(ScrapedContent.url == self.url).first()

@app.post("/scrape")
async def scrape(scrape_request: ScrapeRequest, db: Session = Depends(get_db)):
    try:
        scraper = Scraper(scrape_request.url, db)
        existing_content = scraper.load_from_db()
        if existing_content:
            return {
                "message": "Content already exists in the database.",
                "data": existing_content
            }
        else:
            print(10)
            scraper.fetch_and_parse()
            print(11)
            scraper.save_to_db()
            print(12)
            return {
                "message": "Content scraped and saved successfully.",
                "data": {
                    "url": scraper.url,
                    "html_elements": scraper.html_elements,
                    "elements_properties": scraper.elements_properties,
                    "css": scraper.css,
                    "body_content": scraper.body_content
                }
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_html_content(db: Session, url: str):
    scraped_content = db.query(ScrapedContent).filter(ScrapedContent.url == url).first()
    if not scraped_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return scraped_content.html_elements

@app.post("/color_grading")
async def color_grading_endpoint(scrape_request: ScrapeRequest, db: Session = Depends(get_db)):
    try:
        scraper = Scraper(scrape_request.url, db)
        existing_content = scraper.load_from_db()
        if not existing_content:
            return {
                "message": "Content not found in the database."
            }
        elements_properties = json.loads(existing_content.elements_properties)
        grading_results = color_grading_report(elements_properties)
        print(grading_results)
        return {
            "message": "Color grading calculated successfully.",
            "results": grading_results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
import logging
import traceback

# Setup logging
logging.basicConfig(level=logging.INFO)

router = APIRouter()


@app.post("/content_style")
async def content_style_endpoint(scrape_request: ScrapeRequest, db: Session = Depends(get_db)):
    try:
        logging.info("Received Data: %s", scrape_request)  # Log received data
        
        # Check if the ScrapeRequest has the necessary data
        if not scrape_request.url:
            raise HTTPException(status_code=400, detail="URL is required.")
        
        # Retrieve elements properties from the database
        scraper = Scraper(scrape_request.url, db)
        existing_content = scraper.load_from_db()

        # Check if content was found in the database
        if not existing_content:
            raise HTTPException(status_code=404, detail="Content not found in the database.")
        
        elements_properties = json.loads(existing_content.elements_properties)
        html_content = existing_content.html_elements  # Assuming html_elements is already a JSON string

        # Log the retrieved HTML content and properties
        logging.info("HTML Content: %s", html_content)
        logging.info("Elements Properties: %s", elements_properties)
        
        # Send data to frontend for consistency checks
        return {
            "message": "Content style data retrieved successfully.",
            "html_content": html_content,
            "elements_properties": elements_properties
        }
    
    except Exception as e:
        logging.error("Error Details: %s", str(e))  # Log error message
        logging.error("Traceback: %s", traceback.format_exc())  # Log full stack trace
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")



@app.post("/check_links")
async def check_links(scrape_request: ScrapeRequest):
    links_report = run_link_checker(scrape_request.url)
    return {"message": "Link checking completed", "details": links_report}

@app.post("/evaluate_files")
async def evaluate_files(scrape_request: ScrapeRequest):
    html_content = fetch_webpage(scrape_request.url)
    if html_content:
        soup = parse_html(html_content)
        css_files, js_files, internal_css, internal_js = extract_css_js_files(soup, scrape_request.url)
        total_css_size, total_js_size = evaluate_file_sizes(css_files, js_files, internal_css, internal_js)
        return {
            "total_css_size_kb": total_css_size / 1024,
            "total_js_size_kb": total_js_size / 1024
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch the webpage")
    
@app.post("/responsive")
async def responsive_endpoint(scrape_request: ScrapeRequest, db: Session = Depends(get_db)):
    try:
        # Retrieve HTML and CSS from the database
        scraper = Scraper(scrape_request.url, db)
        existing_content = scraper.load_from_db()
        if not existing_content:
            return {
                "message": "Content not found in the database."
            }

        html_content = existing_content.html_elements
        css_content = [existing_content.css]  # Assuming css is a single string, if not modify accordingly

        # Calculate responsive design score
        responsive_results = responsive(html_content, css_content)

        return {
            "message": "Responsive design analysis completed successfully.",
            "results": responsive_results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/seo_grading")
async def seo_grading_endpoint(
    scrape_request: ScrapeRequest, 
    db: Session = Depends(get_db)
):
    try:
        # Retrieve html_content and css from the database
        scraper = Scraper(scrape_request.url, db)
        existing_content = scraper.load_from_db()
        if not existing_content:
            return {
                "message": "Content not found in the database."
            }
        
        html_content = existing_content.html_elements
        base_url = scraper.url

        # Extract title from HTML elements
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else None

        if not title:
            return {
                "message": "Title not found in the HTML content."
            }

        # Perform SEO grading
        seo_results = seo_grading(html_content, base_url, title)

        return {
            "message": "SEO grading completed successfully.",
            "results": seo_results
        }
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))

    
@app.post("/web_security_analysis")
async def web_security_analysis(scrape_request: ScrapeRequest, db: Session = Depends(get_db)):
    try:
        print("Received Data:", scrape_request)  # Log received data
        
        # Retrieve elements properties and html content from the database
        scraper = Scraper(scrape_request.url, db)
        existing_content = scraper.load_from_db()
        if not existing_content:
            return {"message": "Content not found in the database."}

        elements_properties = json.loads(existing_content.elements_properties)
        html_content = existing_content.html_elements

        # Perform web security analysis
        session = requests.Session()  # Create a session if needed
        base_url = scrape_request.url
        username = None  # Provide username if needed
        password = None  # Provide password if needed
        protected_url = None  # Provide protected URL if needed

        web_security_elements = web_security_report(html_content, base_url, session, username, password, protected_url)

        return {
            "message": "Web security analysis completed successfully.",
            "results": web_security_elements
        }
    except Exception as e:
        print("Error Details:", str(e))  # Log error details
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/ads_recommendation")
async def ads_recommendation_endpoint(scrape_request: ScrapeRequest, db: Session = Depends(get_db)):
    try:
        scraper = Scraper(scrape_request.url, db)
        existing_content = scraper.load_from_db()
        if not existing_content:
            return {
                "message": "Content not found in the database."
            }
        
        body_content = existing_content.body_content

        ad_topics = generate_text_report(body_content, ad_topic_mapping)

        return {
            "message": "Ads recommendation completed successfully.",
            "results": ad_topics
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
