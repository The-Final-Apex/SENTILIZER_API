import string
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator
from langdetect import detect

nltk.download('vader_lexicon')
nltk.download('punkt')

sid = SentimentIntensityAnalyzer()


MORSE_DICT = {
    'a': "._", 'b': "_...", 'c': "_._.", 'd': "_..", 'e': ".", 'f': ".._.",
    'g': "__.", 'h': "....", 'i': "..", 'j': ".___", 'k': "_._", 'l': "._..",
    'm': "__", 'n': "_.", 'o': "___", 'p': ".__.", 'q': "__._", 'r': "._.",
    's': "...", 't': "_", 'u': ".._", 'v': "..._", 'w': ".__", 'x': "_.._",
    'y': "_.__", 'z': "__..", ' ': " "
}

def clean_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    sentences = nltk.sent_tokenize(text)
    sentences = [s[0].upper() + s[1:] if len(s) > 1 else s.upper() for s in sentences]
    return ' '.join(sentences)

def sentiment_analyzer(paragraph, threshold=0.5):
    sentiment_score = sid.polarity_scores(paragraph)
    if sentiment_score['compound'] < threshold:
        sentiment = 'neutral'
        suggestions = []
    else:
        sentiment = 'positive' if sentiment_score['compound'] > 0 else 'negative'
        suggestions = {
            'positive': ['Try to make more specific statements.', 'Consider adding more supporting details.'],
            'negative': ['Focus on one clear point instead of multiple.',
                         'Use less negative language and more neutral or positive language.'],
            'neutral': ['Consider adding more details or evidence to clarify your point.']
        }.get(sentiment, [])

    result = {
        'confidence': sentiment_score.pop('compound'),
        'positive': sentiment_score.pop('pos'),
        'negative': sentiment_score.pop('neg'),
        'neutral': sentiment_score.pop('neu'),
        'mood': sentiment
    }

    return {
        'sentiment_score': result,
        'suggestions': suggestions
    }

def to_morse(text):
    return ' '.join(MORSE_DICT.get(char, '') for char in text.lower())



def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def translate_text(text, target_lang='en'):
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return {
            'translated_text': translated,
            'src_lang': detect_language(text),
            'target_lang': target_lang
        }
    except Exception as e:
        return {'error': str(e)}
