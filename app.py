import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.user_agent import UserAgent

from helpers import apology, login_required, generate_slug, check_url, calculate_credit_cost, check_email

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Home page"""
    try:
        return redirect("/show")
        ##return render_template("index.html", user = session["username"])
    except ValueError:
        return apology("There is an error")


@app.route("/link/<slug>")
@login_required
def link(slug):
    """redirect"""
    try:
        if slug == "":
            return apology("slug is empty")
        result = db.execute("SELECT DISTINCT title, description, origin FROM links WHERE destination = ?", slug)[0]
        user_agent = request.user_agent
        print(user_agent)
        print("platform:", user_agent.platform)
        if not result:
            return apology("That shortend link doesn't exist")
        db.execute("UPDATE views SET count = count + 1, last_viewed = CURRENT_TIMESTAMP  WHERE  link_id = (SELECT id FROM links WHERE destination = ?)", slug)
        return redirect(result['origin'])
    except ValueError:
        return apology("There is an error")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/show")
@login_required
def show():
    try:
        links = db.execute('''
                           SELECT title, origin, destination, description, views.count as views
                           FROM links
                           JOIN views
                           ON links.id = views.link_id
                           WHERE links.user_id =?
                           ''', session["user_id"])
        credit = db.execute("SELECT amount FROM credit WHERE user_id = ?", session["user_id"])[0]['amount']
        last_login = db.execute("SELECT date(last_login, 'localtime') as last_login FROM users WHERE id = ?", session["user_id"])[0]['last_login']
        print(credit)
        return render_template("show.html", links = links, credit = credit, last_login = last_login)
    except ValueError:
        return apology("Error")
    except IndexError:
        return redirect("/login")



@app.route("/create", methods = ["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        try:
            title = request.form.get("title")
            credit_cost = 0
            if not title:
                return apology("There is no title")

            slug = request.form.get("slug")
            if slug:
                if len(slug.replace(" ","")) > 10:
                    return apology("This cannot be more than 10 characters")
                else:
                    credit_cost = 5
            description = request.form.get("description")
            if not description:
                return apology("There is not description")
            origin = request.form.get("origin")

            char_number = request.form.get("character")
            if(len(char_number) != 0):
                char_number = int(char_number)
                if not char_number and len(slug) == 0:
                    return apology("There is no character number")
                if (char_number > 7 or char_number < 4) and len(slug) == 0:
                    return apology("Incorrect number of characters")
                credit_cost = calculate_credit_cost(char_number)
            user_credit = db.execute("SELECT amount FROM credit WHERE user_id = ?", session["user_id"])[0]['amount']
            if (user_credit < credit_cost):
                return apology("Not enough credit")
            if check_url(origin) == False:
                return apology("Not a url")

            destination = generate_slug(char_number, slug)


            db.execute("INSERT INTO links (title, description, origin, destination, user_id) VALUES(?,?,?,?,?)",title, description, origin, destination, session['user_id'])
            link_id = db.execute("SELECT last_insert_rowid()")[0]["last_insert_rowid()"]
            db.execute("INSERT INTO views (link_id) VALUES (?);", link_id)
            db.execute("UPDATE credit  SET  amount = amount - ? WHERE user_id = ? ", credit_cost, session['user_id'])

            print("successfully added the data")
            return redirect("/show")
        except ValueError:
            return apology("Value Error")
    else:
        return render_template("create.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        try:
            email = request.form.get("email")
            username = request.form.get("username")
            password = request.form.get("password")
            password_confirm = request.form.get("confirmation")

            if not email:
                return apology("Please input the email")

            if check_email(email)==False:
                return apology("Incorrect email address")
            if not username or not password:
                return apology("cannot create an account")
            if password_confirm != password:
                return apology("You entered different password")
            hash = generate_password_hash(password)
            db.execute("INSERT INTO users (email, username, hash) VALUES(?, ?, ?)", email, username, hash)
            user_info = int(db.execute("SELECT id FROM users WHERE username = ?", username)[0]['id'])
            db.execute("INSERT INTO credit (user_id) VALUES(?) ",user_info)
        except ValueError:
            return apology("Value error")

        return redirect("/")
    return render_template("register.html")

