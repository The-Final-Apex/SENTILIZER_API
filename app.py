from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
from utils import (
    sentiment_analyzer, to_morse, clean_text,
    detect_language, translate_text
)
from functools import wraps
import sqlite3

app = Flask(__name__)

# ========== CONFIG ========== #
API_KEY = "super-secret-key"  # 🔐 Change this to something secure!
DB_NAME = 'data.db'

# ========== HTML STATUS PAGE ========== #
HTML_STATUS_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sentilizer API</title>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0f172a;
            color: #f1f5f9;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        .container {
            background: #1e293b;
            padding: 2rem 3rem;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
            text-align: center;
        }
        h1 {
            font-size: 2rem;
            color: #38bdf8;
            margin-bottom: 0.5rem;
        }
        p {
            font-size: 1rem;
            margin: 0.5rem 0;
        }
        code {
            background-color: #334155;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>✅ Sentilizer API is Live</h1>
        <p>Available Endpoints:</p>
        <p>
            <code>/analyze</code> &middot; 
            <code>/morse</code> &middot; 
            <code>/save</code> &middot; 
            <code>/clean</code> &middot; 
            <code>/summary</code> &middot; 
            <code>/analyze_all</code> &middot;
            <code>/translate</code>
        </p>
    </div>
</body>
</html>
"""

# ========== API KEY PROTECTION ========== #
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get('x-api-key') != API_KEY:
            return jsonify(error="Unauthorized"), 401
        return f(*args, **kwargs)
    return decorated

# ========== INIT DATABASE ========== #
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS saved_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                content TEXT
            )
        ''')
        conn.commit()

init_db()

# ========== ROUTES ========== #
@app.route('/')
def home():
    return render_template_string(HTML_STATUS_PAGE)

@app.route('/analyze', methods=['POST'])
@require_api_key
def analyze_sentiment():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify(error="Missing 'text' field."), 400
    result = sentiment_analyzer(text)
    return jsonify(result)

@app.route('/morse', methods=['POST'])
@require_api_key
def morse_convert():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify(error="Missing 'text' field."), 400
    morse = to_morse(text)
    return jsonify(morse=morse)

@app.route('/save', methods=['POST'])
@require_api_key
def save_result():
    data = request.json
    content = data.get('content', '')
    if not content:
        return jsonify(error="Missing 'content' field."), 400
    strtime = datetime.now().strftime("%H:%M:%S")
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO saved_results (timestamp, content) VALUES (?, ?)", (strtime, content))
        conn.commit()
    return jsonify(message="Saved to database successfully")

@app.route('/clean', methods=['POST'])
@require_api_key
def clean_text_endpoint():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify(error="Missing 'text' field."), 400
    cleaned = clean_text(text)
    return jsonify(cleaned=cleaned)

@app.route('/summary', methods=['POST'])
@require_api_key
def summarize_text():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify(error="Missing 'text' field."), 400
    import nltk
    nltk.download('punkt')
    sentences = nltk.sent_tokenize(text)
    summary = sentences[0] if sentences else ''
    return jsonify(summary=summary)

@app.route('/analyze_all', methods=['POST'])
@require_api_key
def analyze_full():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify(error="Missing 'text' field."), 400
    cleaned = clean_text(text)
    result = sentiment_analyzer(cleaned)
    result['cleaned_text'] = cleaned
    return jsonify(result)

@app.route('/translate', methods=['POST'])
@require_api_key
def translate_endpoint():
    data = request.json
    text = data.get('text', '')
    target = data.get('target', 'en')
    if not text:
        return jsonify(error="Missing 'text' field."), 400
    lang = detect_language(text)
    translation = translate_text(text, target)
    return jsonify({
        'original_language': lang,
        'translation': translation
    })

if __name__ == '__main__':
    app.run(debug=True)

