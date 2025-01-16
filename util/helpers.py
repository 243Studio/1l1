import random
import re
from flask import render_template, session, redirect
from functools import wraps
from datetime import datetime



def generate_slug(num = 7, custom_slug=""):
    try:
        if(custom_slug == ""):
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            return ''.join([random.choice(alphabet) for _ in range(num)])
        else:
            return slugify(custom_slug)
    except (ValueError, TypeError):
        return None

def slugify(str):
    return str.replace(" ", "-")

def check_url(str):
    url_pattern = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    if(re.match(url_pattern,str)):
        return True
    return False

def check_email(str):
    email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if(re.match(email_pattern, str)):
        return True
    return False
def calculate_credit_cost(num):
    result = 0
    try:
        if type(num) == int:
            num = int(num)
            if num >= 7:
                result = 1
            elif(num == 6):
                result = 2
            elif(num == 5):
                result = 3
            else:
                result = 4

            return result
    except (ValueError, TypeError):
        return result


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def convert_to_local_time(utc_time):
    client_timezone = pytz.timezone("Africa/Kinshasa")
    
    return datetime.astimezone(utc_time, client_timezone).strftime("%Y-%m-%d %H:%M")
#.strftime("%Y-%m-%d %H:%M:%S")