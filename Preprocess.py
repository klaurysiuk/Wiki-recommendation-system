
import json
import re
import csv
import nltk
from nltk.stem import WordNetLemmatizer


def remove_brackets_content(text):
    text = re.sub(r'\(.*?\)', '', text)
    return re.sub(r'\[.*?\]', '', text)


def remove_templates(text):
    pattern = re.compile(r'\{\{.*?\}\}')
    while pattern.search(text):
        text = pattern.sub('', text)
    return text

def remove_section_titles(text):
    return re.sub(r'=+.*?=+', '', text)

def clean_wiki_text(text):
    text = remove_brackets_content(text)
    text = remove_templates(text)
    text = remove_section_titles(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
def filter_unique_articles(articles):
    seen_texts = set()
    unique_articles = []

    for article in articles:
        text = article.get('text', '')
        if text not in seen_texts:
            unique_articles.append(article)
            seen_texts.add(text)

    return unique_articles

def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    words = nltk.word_tokenize(text)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(lemmatized_words)

def main():
    try:
        with open('wiki.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        processed_data = []
        for article in data:
            url = article.get('url', '')
            title = article.get('title', '')
            text = article.get('text', '')

            text_processed = lemmatize_text(clean_wiki_text(text))

            processed_data.append({
                'url': url,
                'title': title,
                'text': text_processed
            })
        processed_data = filter_unique_articles(processed_data)

        csv_columns = ['url', 'title', 'text']
        with open('wiki_processed.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for article in processed_data:
                writer.writerow(article)

        print("Processing completed. Results saved to 'wiki_processed.csv'")

    except FileNotFoundError:
        print("Error: 'wiki.json' file not found")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in the input file")

if __name__ == "__main__":
    main()