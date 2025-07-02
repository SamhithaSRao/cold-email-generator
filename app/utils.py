import re

def clean_text(text):
    text = re.sub(r'<[^>]*?>', '', text)  # Remove HTML
    text = re.sub(r'http[s]?://\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special chars
    text = re.sub(r'\s{2,}', ' ', text)  # Collapse multiple spaces
    return text.strip()
