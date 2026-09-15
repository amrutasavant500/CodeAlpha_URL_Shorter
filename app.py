from flask import Flask, request, jsonify, redirect, render_template
import sqlite3
import secrets
import string
from urllib.parse import urlparse

app = Flask(__name__)
DB_NAME = "urls.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            long_url TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    


def make_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def valid_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json(silent=True) or {}
    long_url = data.get("url", "").strip()

    if not long_url:
        return jsonify({"error": "URL is required"}), 400

    if not valid_url(long_url):
        return jsonify({"error": "Enter a valid URL starting with http:// or https://"}), 400

    conn = sqlite3.connect(DB_NAME)

    # Return the existing short link if this URL was already stored.
    existing = conn.execute(
        "SELECT short_code FROM urls WHERE long_url = ?", (long_url,)
    ).fetchone()

    if existing:
        code = existing[0]
    else:
        while True:
            code = make_short_code()
            try:
                conn.execute(
                    "INSERT INTO urls (short_code, long_url) VALUES (?, ?)",
                    (code, long_url)
                )
                conn.commit()
                break
            except sqlite3.IntegrityError:
                pass

    conn.close()

    short_url = request.host_url.rstrip("/") + "/" + code
    return jsonify({
        "original_url": long_url,
        "short_code": code,
        "short_url": short_url
    })


@app.route("/<short_code>")
def redirect_to_original(short_code):
    conn = sqlite3.connect(DB_NAME)
    row = conn.execute(
        "SELECT long_url FROM urls WHERE short_code = ?", (short_code,)
    ).fetchone()
    conn.close()

    if not row:
        return "Short URL not found", 404

    return redirect(row[0])
# Database la ithe call kara - if chya var
init_db()

if __name__ == "__main__":
    print("\nURL Shortener is running!")
    print("Open: http://127.0.0.1:5000\n")
    app.run(debug=True)

if __name__ == "__main__":
    init_db()
    print("\nURL Shortener is running!")
    print("Open: http://127.0.0.1:5000\n")
    app.run(debug=True)
