from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=0)

def chunk_text(text, max_chunk=500):
    words = text.split()
    return [" ".join(words[i:i+max_chunk]) for i in range(0, len(words), max_chunk)]

def summarize_reviews(reviews, max_length=15, min_length=5):
    text = " ".join(reviews)
    chunks = chunk_text(text)
    summary_texts = [
        summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
        for chunk in chunks
    ]
    return " ".join(summary_texts)
