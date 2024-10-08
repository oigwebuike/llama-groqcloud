import re
from bs4 import BeautifulSoup

def clean_text(text: str) -> str:
    """
    Clean text by removing HTML tags, URLs, special characters, and redundant spaces.
    Args:
        text (str): The input string to be cleaned.
    Returns:
        str: The cleaned string.
    """

    # Remove HTML tags using BeautifulSoup
    text = BeautifulSoup(text, "html.parser").get_text()

    # Remove URLs using a regex pattern
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

    # Remove special characters and punctuations (keeping only alphanumeric and space)
    text = re.sub(r'[^A-Za-z0-9\s]+', '', text)

    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)

    # Trim leading and trailing whitespaces
    text = text.strip()
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text
    
    