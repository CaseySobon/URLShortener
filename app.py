# Import necessary modules
import os
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import string
import uuid

# Initialize Flask app
app = Flask(__name__)
# Configure SQLAlchemy with the database URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
# Initialize SQLAlchemy with app configuration
db = SQLAlchemy(app)

# Define Link model for SQLAlchemy
class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(80), unique=True, nullable=False)

# Create all database tables
with app.app_context():
    db.create_all()

# Define the characters to use in short URLs
chars = string.ascii_lowercase + string.ascii_uppercase + string.digits

# Function to encode a number into base62
def base62_encode(num):
    arr = []
    base = len(chars)
    while num:
        num, rem = divmod(num, base)
        arr.append(chars[rem])
    arr.reverse()
    return ''.join(arr)

# Define the route for the home page, which accepts both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def handle_url():
    # Initialize variables for the original URL, short URL, and any errors
    url = None
    short_url = None
    shorten_error = None  # Error for the "Shorten" section
    expand_error = None  # Error for the "Expand" section
    existing = False  # Flag to indicate if the original URL already exists
    domain = request.host_url.rstrip('/')  # Define domain here to be used in the template

    # If the request method is POST, process the form data
    if request.method == 'POST':
        # Get the original URL, custom short URL, short URL to expand, and new short URL option from the form
        original_url = request.form.get('url')
        custom_short_url = request.form.get('custom_short_url')
        short_url_input = request.form.get('short_url')
        new_short_url = request.form.get('new_short_url')

        # If an original URL was provided, process it
        if original_url:
            # Check if the original URL already exists in the database
            existing_link = Link.query.filter_by(original_url=original_url).first()
            # If the original URL exists and the user doesn't want a new short URL, return the existing short URL
            if existing_link and not new_short_url:
                short_url = domain + '/' + existing_link.short_url
                existing = True
            else:
                # If a custom short URL was provided, check if it's already in use
                if custom_short_url:
                    existing_link = Link.query.filter_by(short_url=custom_short_url).first()
                    if existing_link:
                        # If the custom short URL is already in use, set an error message
                        shorten_error = "Custom short URL is already in use, please choose another name"
                    else:
                        # If the custom short URL is not in use, create a new link with the original URL and custom short URL
                        link = Link(original_url=original_url, short_url=custom_short_url)
                        db.session.add(link)
                        db.session.commit()
                else:
                    # If no custom short URL was provided, create a new link with a placeholder short URL
                    placeholder = str(uuid.uuid4())
                    link = Link(original_url=original_url, short_url=placeholder)
                    db.session.add(link)
                    db.session.commit()
                    # Generate a new short URL using base62 encoding and update the link
                    short_url = base62_encode(link.id)
                    link.short_url = short_url
                    db.session.commit()

                # If there were no errors and the original URL didn't already exist, set the short URL
                if not shorten_error and not existing:
                    short_url = domain + '/' + link.short_url

        # If a short URL was provided to expand, process it
        elif short_url_input:
            # Remove the domain from the short URL
            short_url_input = short_url_input.split('/')[-1]
            # Check if the short URL exists in the database
            link = Link.query.filter_by(short_url=short_url_input).first()
            if link:
                # If the short URL exists, set the original URL
                url = link.original_url
            else:
                # If the short URL doesn't exist, set an error message
                expand_error = "URL doesn't exist"
            short_url = domain + '/' + short_url_input

    # Render the home page with the original URL, short URL, and any errors
    return render_template('index.html', url=url, short_url=short_url, shorten_error=shorten_error, expand_error=expand_error, existing=existing)
    
    

# Route to redirect from a short URL to the original URL
@app.route('/<short_url>')
def redirect_short_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first()
    if link:
        return redirect(link.original_url)
    else:
        return '404: URL not found', 404

# Route to expand a short URL into the original URL
@app.route('/expand/<short_url>')
def expand_short_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first()
    if link:
        return link.original_url
    else:
        return 'Error: URL not found', 404

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
