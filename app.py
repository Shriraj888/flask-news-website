from flask import Flask, render_template, request, jsonify
import os
import requests
from datetime import datetime
import re
from dotenv import load_dotenv
import secrets

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Production configuration with enhanced security
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_urlsafe(32))
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Security headers
@app.after_request
def after_request(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# News API configuration
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
NEWS_API_BASE_URL = 'https://newsapi.org/v2'

# Validate API key
if not NEWS_API_KEY:
    print("WARNING: NEWS_API_KEY environment variable not set!")
    print("Please set your NewsAPI key in the .env file or environment variables.")

# Cache for API responses (simple in-memory cache)
NEWS_CACHE = {}
CACHE_DURATION = 300  # 5 minutes

def fetch_news(category='general', country='us', page_size=10):
    """
    Fetch news articles from News API with caching
    
    Args:
        category (str): News category
        country (str): Country code
        page_size (int): Number of articles to fetch
    
    Returns:
        list: List of processed news articles
    """
    # Check if API key is available
    if not NEWS_API_KEY:
        print("NEWS_API_KEY not found. Please set it in your .env file.")
        return []
    
    # Create cache key
    cache_key = f"{category}_{country}_{page_size}"
    current_time = datetime.now().timestamp()
    
    # Check cache first
    if cache_key in NEWS_CACHE:
        cached_data, timestamp = NEWS_CACHE[cache_key]
        if current_time - timestamp < CACHE_DURATION:
            return cached_data
    
    try:
        url = f"{NEWS_API_BASE_URL}/top-headlines"
        params = {
            'apiKey': NEWS_API_KEY,
            'category': category,
            'country': country,
            'pageSize': min(page_size, 20)  # Limit to 20 articles max
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') == 'ok':
            articles = []
            for article in data.get('articles', []):
                # Skip articles with removed content
                if article.get('title') == '[Removed]' or not article.get('title'):
                    continue
                    
                processed_article = {
                    'title': article.get('title', 'No Title'),
                    'content': article.get('description', 'No description available.'),
                    'author': article.get('author', 'Unknown Author'),
                    'date': format_date(article.get('publishedAt')),
                    'url': article.get('url', '#'),
                    'image_url': article.get('urlToImage'),
                    'source': article.get('source', {}).get('name', 'Unknown Source')
                }
                articles.append(processed_article)
            
            # Cache the results
            NEWS_CACHE[cache_key] = (articles, current_time)
            
            return articles
        else:
            print(f"API Error: {data.get('message', 'Unknown error')}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return []
    except Exception as e:
        print(f"General Error: {e}")
        return []

def format_date(date_string):
    """Format ISO date string to readable format"""
    if not date_string:
        return 'Unknown Date'
    
    try:
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return dt.strftime('%B %d, %Y at %I:%M %p')
    except:
        return date_string

# Routes
@app.route('/')
def home():
    """Home page route"""
    # Get featured news for the homepage
    featured_articles = fetch_news(category='general', page_size=3)
    return render_template('index.html', title='Flask News Website', featured_articles=featured_articles)

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html', title='About Us')

@app.route('/news')
def news():
    """News page route - fetches news from API"""
    category = request.args.get('category', 'general')
    country = request.args.get('country', 'us')
    
    # Fetch news articles from API
    news_articles = fetch_news(category=category, country=country, page_size=12)
    
    # Available categories for the filter
    categories = [
        {'value': 'general', 'label': 'General'},
        {'value': 'business', 'label': 'Business'},
        {'value': 'entertainment', 'label': 'Entertainment'},
        {'value': 'health', 'label': 'Health'},
        {'value': 'science', 'label': 'Science'},
        {'value': 'sports', 'label': 'Sports'},
        {'value': 'technology', 'label': 'Technology'}
    ]
    
    return render_template('news.html', 
                         title='Latest News', 
                         articles=news_articles, 
                         categories=categories,
                         current_category=category)

@app.route('/api/news/<category>')
def api_news(category):
    """API endpoint for fetching news by category"""
    country = request.args.get('country', 'us')
    page_size = min(int(request.args.get('page_size', 10)), 20)  # Limit to 20 articles max
    
    articles = fetch_news(category=category, country=country, page_size=page_size)
    
    return jsonify({
        'status': 'success',
        'category': category,
        'articles': articles,
        'total': len(articles)
    })

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page route with enhanced form handling"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validation
        errors = []
        
        if not name or len(name) < 2:
            errors.append('Name must be at least 2 characters long.')
        
        if not email:
            errors.append('Email is required.')
        elif not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            errors.append('Please provide a valid email address.')
        
        if not subject or len(subject) < 5:
            errors.append('Subject must be at least 5 characters long.')
        
        if not message or len(message) < 10:
            errors.append('Message must be at least 10 characters long.')
        
        if errors:
            return jsonify({
                'status': 'error',
                'message': ' '.join(errors)
            })
        
        try:
            # In production, save to database or send email
            print(f"Contact form submission - Name: {name}, Email: {email}, Subject: {subject}")
            
            return jsonify({
                'status': 'success',
                'message': f'Thank you {name}! Your message has been received. We\'ll get back to you within 24 hours.'
            })
            
        except Exception as e:
            print(f"Error processing contact form: {e}")
            return jsonify({
                'status': 'error',
                'message': 'An error occurred while processing your message. Please try again.'
            })
    
    return render_template('contact.html', title='Contact Us')

@app.errorhandler(404)
def page_not_found(e):
    """404 error handler"""
    return render_template('404.html', title='Page Not Found'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """500 error handler"""
    return render_template('404.html', title='Server Error'), 500

if __name__ == '__main__':
    # Production-ready server configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(
        debug=debug,
        host='0.0.0.0',
        port=port
    )
