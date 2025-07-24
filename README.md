# 🧠 Sentiment & Morse Analyzer

## This project contains:

> 🧹 A Flask API that analyzes sentiment and converts text to Morse code.

> 💽 A CustomTkinter GUI client that communicates with the API.

### 📁 Project Structure
    
    sentiment_api/         # Flask API backend
    │   ├— app.py
    │   └— utils.py
    
    sentiment_frontend/    # GUI Client (CustomTkinter)
    │   ├— app.py
    │   └— config.py


## ⚙️ Requirements

### Install Python dependencies:

    pip install flask nltk customtkinter requests

### Linux users may also need:

    sudo apt install python3-tk

## 🚀 How to Run

### 1. Start the API

  cd sentiment_api
  python app.py

You should see:

  Running on http://127.0.0.1:5000/

> Visit that URL in your browser to confirm the API is running.

### 2. Start the GUI Client

In another terminal, go to the sentiment_frontend/ directory:

  cd sentiment_frontend
  python app.py

You’ll see a desktop GUI window appear.

### 🧺 Features

✅ Sentiment Analysis

Detects whether the text is positive, neutral, or negative.

Provides suggestions based on the mood.

Displays a confidence score.

✅ Morse Code Translator

Converts input text into Morse code.

✅ Save Results

Saves analysis results to rating.txt on the backend.

🧠 Endpoints (for developers)

Endpoint

Method

Description

/

GET

HTML "API running" page

/analyze

POST

Analyze sentiment of text

/morse

POST

Convert text to Morse code

/save

POST

Save analysis result

📝 Example Request (for /analyze)

POST /analyze
{
  "text": "I really enjoy working with Python!"
}

📌 Notes

Make sure the API is running before starting the GUI.

You can change the API base URL in sentiment_frontend/config.py.

📄 License

This project is open source and free to use.

README IS INCOMEPLETE!!
