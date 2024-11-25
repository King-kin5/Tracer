from flask import Flask, jsonify, request, render_template
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import logging
import os
from safe import check_link_safety
app = Flask(__name__,template_folder="templates",static_folder="static")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@app.route('/')
def index():
    try:
        # Log template directory information
        template_dir = os.path.join(app.root_path, 'templates')
        logger.info(f"Template directory path: {template_dir}")
        logger.info(f"Template directory exists: {os.path.exists(template_dir)}")
        if os.path.exists(template_dir):
            logger.info(f"Template directory contents: {os.listdir(template_dir)}")
        
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/home')
def home():
    try:
        template_dir = os.path.join(app.root_path, 'templates')
        logger.info(f"Template directory path: {template_dir}")
        logger.info(f"Template directory exists: {os.path.exists(template_dir)}")
        if os.path.exists(template_dir):
            logger.info(f"Template directory contents: {os.listdir(template_dir)}")
            
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in home route: {str(e)}")
        return f"Error: {str(e)}", 500



@app.route('/debug-info')
def debug_info():
    """Route to show debug information"""
    try:
        template_dir = os.path.join(app.root_path, 'templates')
        static_dir = os.path.join(app.root_path, 'static')
        
        debug_info = {
            'app_root_path': app.root_path,
            'template_folder': app.template_folder,
            'template_dir_exists': os.path.exists(template_dir),
            'template_dir_contents': os.listdir(template_dir) if os.path.exists(template_dir) else [],
            'static_dir_exists': os.path.exists(static_dir),
            'static_dir_contents': os.listdir(static_dir) if os.path.exists(static_dir) else [],
            'environment': app.config.get('ENV'),
            'debug_mode': app.debug,
        }
        return jsonify(debug_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/check_link', methods=['POST'])
def checklink():
    url = request.form.get('url')  # Get the URL from the form submission
    if not url:
        return render_template('result.html', data={"error": "URL is required"})
    try:
        is_safe, message, results = check_link_safety(url)
        # Combine results with additional metadata
        results.update({"is_safe": is_safe, "message": message})
        return render_template('result.html', data=results, results=results)
    except Exception as e:
        return render_template('result.html', data={"error": str(e)}, results=None)



# Add error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500





@app.route('/ip_tracker', methods=['POST'])
def ip_tracker():
    ip = request.form.get('ip')
    if not ip:
        return render_template('results.html', data={"error": "IP address is required"})
    try:
        req_api = requests.get(f"http://ipwho.is/{ip}")
        ip_data = req_api.json()
        if not ip_data.get("success", True):
            return render_template('results.html', data={"error": "Invalid IP address"})
        return render_template('results.html', data=ip_data)
    except Exception as e:
        return render_template('results.html', data={"error": str(e)})

@app.route('/phone_tracker', methods=['POST'])
def phone_tracker():
    phone = request.form.get('phone')
    if not phone:
        return render_template('results.html', data={"error": "Phone number is required"})
    try:
        parsed_number = phonenumbers.parse(phone, "ID")
        result = {
            "location": geocoder.description_for_number(parsed_number, "id"),
            "region_code": phonenumbers.region_code_for_number(parsed_number),
            "timezone": ', '.join(timezone.time_zones_for_number(parsed_number)),
            "operator": carrier.name_for_number(parsed_number, "en"),
            "is_valid_number": phonenumbers.is_valid_number(parsed_number),
            "is_possible_number": phonenumbers.is_possible_number(parsed_number),
            "international_format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "mobile_format": phonenumbers.format_number_for_mobile_dialing(parsed_number, "ID", with_formatting=True),
            "type": str(phonenumbers.number_type(parsed_number)),
            "e164_format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164),
            "country_code": parsed_number.country_code,
            "local_number": parsed_number.national_number
        }
        return render_template('results.html', data=result)
    except Exception as e:
        return render_template('results.html', data={"error": str(e)})

@app.route('/username_tracker', methods=['POST'])
def username_tracker():
    username = request.form.get('username')
    if not username:
        return render_template('results.html', data={"error": "Username is required"})
    try:
        results = {}
        social_media = [
            {"url": "https://www.facebook.com/{}", "name": "Facebook"},
            {"url": "https://www.x.com/{}", "name": "X"},
            {"url": "https://www.instagram.com/{}", "name": "Instagram"},
            {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
            {"url": "https://www.github.com/{}", "name": "GitHub"},
            {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
            {"url": "https://www.youtube.com/{}", "name": "Youtube"},
            {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
            {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
            {"url": "https://www.medium.com/@{}", "name": "Medium"},
            {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
            {"url": "https://www.telegram.me/{}", "name": "Telegram"},
        ]
        
        # Define headers to mimic browser behavior
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
        }

        for site in social_media:
            url = site['url'].format(username)
            try:
                # Use headers for all sites except Facebook
                if site['name'] == "Facebook":
                    response = requests.get(url, timeout=5)  # No headers for Facebook
                else:
                    response = requests.get(url, headers=headers, timeout=10)  # Use headers for other sites
                results[site['name']] = url if response.status_code == 200 else "Not Found"
            except requests.exceptions.Timeout:
                results[site['name']] = "Request Timed Out"
            except requests.exceptions.RequestException as e:
                results[site['name']] = f"Error: {str(e)}"

        return render_template('results.html', data=results)
    except Exception as e:
        return render_template('results.html', data={"error": str(e)})

if __name__ == '__main__':
    app.run()
