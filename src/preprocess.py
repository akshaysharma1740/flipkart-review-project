import re
import spacy
import unicodedata

nlp = spacy.load("en_core_web_sm")

def clean_and_lemmatize(text):
    text = unicodedata.normalize('NFKC', text)
    text = text.lower()
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    doc = nlp(text)
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and token.is_alpha
    ]
    return " ".join(tokens)

def preprocess_reviews(reviews):
    return [clean_and_lemmatize(r) for r in reviews]
