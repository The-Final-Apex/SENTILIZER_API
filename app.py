from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
from utils import sentiment_analyzer, to_morse

app = Flask(__name__)

HTML_STATUS_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sentiment & Morse API</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #121212;
            color: #f8f8f8;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        .status {
            font-size: 1.5rem;
            background: #1e1e1e;
            padding: 1.5rem 2rem;
            border: 1px solid #333;
            border-radius: 10px;
            box-shadow: 0 0 10px #0f0;
        }
    </style>
</head>
<body>
    <div class="status">
        ✅ Sentiment & Morse API is running!<br>
        <small>Endpoints: <code>/analyze</code>, <code>/morse</code>, <code>/save</code></small>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_STATUS_PAGE)
@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify(error="Missing 'text' field."), 400
    result = sentiment_analyzer(text)
    return jsonify(result)

@app.route('/morse', methods=['POST'])
def morse_convert():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify(error="Missing 'text' field."), 400
    morse = to_morse(text)
    return jsonify(morse=morse)

@app.route('/save', methods=['POST'])
def save_result():
    data = request.json
    content = data.get('content', '')
    if not content:
        return jsonify(error="Missing 'content' field."), 400
    with open('rating.txt', 'a') as f:
        strtime = datetime.now().strftime("%H:%M:%S")
        f.write(f'{strtime}: {content}\n\n')
    return jsonify(message="Saved successfully")

if __name__ == '__main__':
    app.run(debug=True)

