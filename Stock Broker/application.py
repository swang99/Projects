import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    # Show portfolio of stocks
    holdings = db.execute("SELECT * FROM transactions WHERE buyerID = ?", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    amntcash = cash[0]['cash']
    # For an empty portfolio
    if not holdings:
        totalvalue = amntcash
        return render_template("index.html", amntcash=amntcash, totalvalue=totalvalue)
    # For an existing portfolio
    else:
        amntholdings = db.execute("SELECT SUM(amount) FROM transactions WHERE buyerID = ?", session["user_id"])
        amntstock = amntholdings[0]['SUM(amount)']
        totalvalue = amntcash + amntstock
        return render_template("index.html", holdings=holdings, amntcash=amntcash, totalvalue=totalvalue)


@app.route("/cash", methods=["GET", "POST"])
@login_required
def addcash():
    # Add or withdraw cash from an account
    if request.method == "GET":
        return render_template("cash.html")
    else:
        transct_cash = request.form.get("amount")
        db.execute("UPDATE users SET cash = cash + ?", transct_cash)
        flash("Your cash balance has been updated!")
        return redirect("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # Buy shares of stock
    if request.method == "GET":
        return render_template("buy.html")
    else:
        quote = lookup(request.form.get("symbol"))

        # Check whether symbol exists
        if quote == None:
            return apology("Invalid symbol")

        # Check whether there is enough cash
        else:
            cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            quote_amount = int(request.form.get("shares")) * quote["price"]
            if quote_amount > cash[0]['cash']:
                return apology("Can't afford")
            else:
                # Update cash balance
                db.execute("UPDATE users SET cash = ? WHERE id = ?", cash[0]['cash'] - quote_amount, session["user_id"])

                # Update SQL, new or existing symbol?
                own_shares = db.execute("SELECT shares FROM transactions WHERE ticker = ? AND buyerID = ?", quote["symbol"], session["user_id"])
                if not own_shares:
                    db.execute("INSERT INTO transactions (buyerID, ticker, name, shares, price, amount) VALUES (?, ?, ?, ?, ?, ?)",
                                session["user_id"], quote["symbol"], quote["name"], int(request.form.get("shares")), quote["price"], quote_amount)
                else:
                    total_shares = own_shares[0]['shares'] + int(request.form.get("shares"))
                    db.execute("UPDATE transactions SET shares = ?, amount = amount + ? WHERE ticker = ? AND buyerID = ?",
                                total_shares, quote_amount, quote["symbol"], session["user_id"])
                db.execute("INSERT INTO history (buyerID, ticker, shares, price) VALUES (?, ?, ?, ?)",
                            session["user_id"], quote["symbol"], int(request.form.get("shares")), quote["price"])
                flash('Buy transaction successful!')
                return redirect("/")


@app.route("/history")
@login_required
def history():
    # Show history of transactions
    history = db.execute("SELECT * FROM history WHERE buyerID = ?", session["user_id"])

    # For an empty history
    if not history:
        return apology("No history.")
    
    # For an existing history
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear() 

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username and password are both submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear() 
    
    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == 'GET':
        return render_template('quote.html')
    else:
        stockquote = lookup(request.form.get("symbol"))
        if stockquote == None:
            quote_err = request.form.get("symbol") + " does not exist"
            return render_template("quote.html", quote_err=quote_err)
        else:
            symbol = stockquote["symbol"]
            price = usd(stockquote["price"])
            name = stockquote["name"]
            return render_template('quoted.html', symbol=symbol, name=name, price=price)


@app.route("/register", methods=["GET", "POST"])
def register():
    # Register user
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # Check if passwords match
        if request.form.get("password") == request.form.get("confirmation"):
            password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        else:
            passerr = "Passwords do not match. Please check your inputs."
            return render_template('notmatchp.html', passerr=passerr)

        # Check if username is available
        username = request.form.get("username")
        count = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(count) != 0:
            usererr = username + " is already taken. Please enter a new username."
            return render_template("register.html", usererr=usererr)
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=username, password=password)
            return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # Sell shares of stock
    tickers = db.execute("SELECT ticker FROM transactions WHERE buyerID = ?", session["user_id"])
    if request.method == 'GET':
        return render_template("sell.html", tickers=tickers)
    else:
        quote = lookup(request.form.get("symbol"))
        all_shares = db.execute("SELECT shares FROM transactions WHERE ticker = ? AND buyerID = ?",
                             quote["symbol"], session["user_id"])
        shares = int(request.form.get("sellshares"))
        # Own enough shares to sell?
        if shares > all_shares[0]['shares']:
            return apology("You do not own that many shares.")
        else:
            cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            quote_amount = int(request.form.get("sellshares")) * quote["price"]
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", quote_amount, session["user_id"])

            # Some shares sold
            if shares < all_shares[0]["shares"]:
                db.execute("UPDATE transactions SET shares = shares - ?, amount = amount - ? WHERE ticker = ? AND buyerID = ?",
                            shares, quote_amount, quote["symbol"], session["user_id"])
            # All shares sold
            elif shares == all_shares[0]["shares"]:
                db.execute("DELETE FROM transactions WHERE ticker = ? AND buyerID = ?",
                            quote["symbol"], session["user_id"])
            db.execute("INSERT INTO history (buyerID, ticker, shares, price) VALUES (?, ?, ?, ?)",
                        session["user_id"], quote["symbol"], -shares, quote["price"])
            flash('Sell transaction successful!')
            return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)