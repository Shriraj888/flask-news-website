from flask import Flask, render_template, request, jsonify
import os
import re
from datetime import datetime, timedelta
import secrets
from dotenv import load_dotenv

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

# Mock news data for demonstration (no API required)
MOCK_NEWS_DATA = {
    'general': [
        {
            'title': 'Breaking: Revolutionary AI Technology Transforms Healthcare',
            'content': 'Scientists have developed groundbreaking artificial intelligence that can diagnose diseases with unprecedented accuracy, potentially revolutionizing medical care worldwide.',
            'author': 'Dr. Sarah Johnson',
            'date': 'December 15, 2024 at 10:30 AM',
            'url': '#',
            'image_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=400&fit=crop',
            'source': 'Tech Medical Journal'
        },
        {
            'title': 'Global Climate Summit Reaches Historic Agreement',
            'content': 'World leaders unite on ambitious new climate targets, promising unprecedented cooperation to combat global warming and protect the environment.',
            'author': 'Environmental Correspondent',
            'date': 'December 14, 2024 at 2:15 PM',
            'url': '#',
            'image_url': 'https://images.unsplash.com/photo-1569163139394-de44aa2aa3f5?w=800&h=400&fit=crop',
            'source': 'Global News Network'
        },
        {
            'title': 'Space Exploration Milestone: Mars Colony Planning Begins',
            'content': 'International space agencies announce detailed plans for the first permanent human settlement on Mars, marking a new era in space exploration.',
            'author': 'Space Reporter',
            'date': 'December 13, 2024 at 6:45 PM',
            'url': '#',
            'image_url': 'https://images.unsplash.com/photo-1446776876964-6cf67f04d350?w=800&h=400&fit=crop',
            'source': 'Space Today'
        }
    ],
    'technology': [
        {
            'title': 'Quantum Computing Breakthrough Achieved',
            'content': 'Researchers successfully demonstrate quantum advantage in practical applications, bringing quantum computing closer to everyday use.',
            'author': 'Tech Editor',
            'date': 'December 15, 2024 at 9:00 AM',
            'url': '#',
            'image_url': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=400&fit=crop',
            'source': 'Quantum Weekly'
        },
        {
            'title': 'New Programming Language Revolutionizes Development',
            'content': 'A new programming language promises to make software development faster, safer, and more accessible to developers worldwide.',
            'author': 'Code Analyst',
            'date': 'December 14, 2024 at 11:30 AM',
            'url': '#',
            'image_url': 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&h=400&fit=crop',
            'source': 'Developer News'
        }
    ],
    'business': [
        {
            'title': 'Sustainable Energy Investments Reach Record High',
            'content': 'Global investments in renewable energy technologies hit unprecedented levels, signaling a major shift towards sustainable business practices.',
            'author': 'Business Analyst',
            'date': 'December 15, 2024 at 8:15 AM',
            'url': '#',
            'image_url': 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=800&h=400&fit=crop',
            'source': 'Business Today'
        }
    ],
    'sports': [
        {
            'title': 'World Cup Preparations Underway',
            'content': 'Teams from around the globe are making final preparations for the upcoming World Cup, promising an exciting tournament ahead.',
            'author': 'Sports Reporter',
            'date': 'December 15, 2024 at 7:30 AM',
            'url': '#',
            'image_url': 'https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=800&h=400&fit=crop',
            'source': 'Sports Central'
        }
    ],
    'health': [
        {
            'title': 'New Treatment Shows Promise for Rare Diseases',
            'content': 'Medical researchers announce breakthrough treatment that could help millions of patients suffering from rare genetic disorders.',
            'author': 'Medical Correspondent',
            'date': 'December 14, 2024 at 3:20 PM',
            'url': '#',
            'image_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=400&fit=crop',
            'source': 'Health Science Daily'
        }
    ],
    'science': [
        {
            'title': 'Ocean Exploration Reveals New Species',
            'content': 'Deep-sea exploration mission discovers dozens of new marine species, expanding our understanding of ocean biodiversity.',
            'author': 'Marine Biologist',
            'date': 'December 13, 2024 at 4:45 PM',
            'url': '#',
            'image_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&h=400&fit=crop',
            'source': 'Ocean Research Institute'
        }
    ],
    'entertainment': [
        {
            'title': 'Award Season Kicks Off with Surprise Nominations',
            'content': 'This year\'s entertainment awards feature unexpected nominees, showcasing diverse talent from around the world.',
            'author': 'Entertainment Reporter',
            'date': 'December 12, 2024 at 5:00 PM',
            'url': '#',
            'image_url': 'https://images.unsplash.com/photo-1489599162718-d8d60bc20cdf?w=800&h=400&fit=crop',
            'source': 'Entertainment Weekly'
        }
    ]
}

def fetch_news(category='general', country='us', page_size=10):
    """
    Fetch mock news articles for demonstration
    
    Args:
        category (str): News category
        country (str): Country code (ignored in mock version)
        page_size (int): Number of articles to fetch
    
    Returns:
        list: List of mock news articles
    """
    # Get articles for the requested category, fallback to general
    articles = MOCK_NEWS_DATA.get(category, MOCK_NEWS_DATA['general']).copy()
    
    # If we need more articles, add some from other categories
    if len(articles) < page_size:
        for cat_name, cat_articles in MOCK_NEWS_DATA.items():
            if cat_name != category:
                articles.extend(cat_articles)
                if len(articles) >= page_size:
                    break
    
    # Limit to requested page size
    return articles[:page_size]

def format_date(date_string):
    """Format date string to readable format"""
    if not date_string:
        return 'Unknown Date'
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
    """News page route - displays mock news articles"""
    category = request.args.get('category', 'general')
    
    # Fetch news articles
    news_articles = fetch_news(category=category, page_size=12)
    
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
    page_size = min(int(request.args.get('page_size', 10)), 20)
    
    articles = fetch_news(category=category, page_size=page_size)
    
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
