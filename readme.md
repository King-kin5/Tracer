Tracer

Tracer is a web-based application designed to track and manage phone numbers, check username availability across platforms, and verify the safety of URLs efficiently. Built using Flask, it offers a robust and scalable backend, providing real-time data through an intuitive interface.

Features

Phone Number Validation:
Validate and format international phone numbers using the phonenumbers library.

Username Availability Checker:
Check the availability of usernames across multiple social media platforms like Instagram, Facebook, GitHub, and more.

Link Safety Checker:
Verify URLs for safety using SSL validation and the Google Safe Browsing API.

Web-Based Interface:
Accessible through a simple, responsive web interface.

Concurrent Requests:
Handle multiple requests seamlessly with Gunicorn.


Technology Stack

Backend: Flask 3.0.3

API Requests: requests library

Phone Number Parsing: phonenumbers library

Username Checking: requests and custom logic

Link Safety Checking: Google Safe Browsing API

Deployment: Gunicorn

Configuration Management: python-dotenv


Prerequisites

Python 3.7 or higher


Installation

1. Clone the repository:

git clone https://github.com/King-kin5/Tracer.git
cd Tracer


2. Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


3. Install dependencies:

pip install -r requirements.txt



Usage

1. Run the application locally:

flask run


2. Access the application at http://localhost:5000.





Deployment

Deploy using Gunicorn:

gunicorn -w 4 -b 0.0.0.0:8000 app:app

Environment Variables

Create a .env file to manage environment-specific variables:

FLASK_APP=app
FLASK_ENV=development
GOOGLE_SAFE_BROWSING_API_KEY=your_api_key_here

Contributing

Contributions are welcome! Please fork the repository and create a pull request with your improvements or feature additions.