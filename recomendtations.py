import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

df = pd.read_csv('wiki_processed.csv', encoding='utf-8')
documents = df['text'].astype(str).tolist()

tfidf = TfidfVectorizer(use_idf=True, smooth_idf=False)
tfidf_matrix = tfidf.fit_transform(documents)

def recommend_similar_articles(visited_titles, top_n=10):
    visited_indices = []
    for title in visited_titles:
        if title in df['title'].values:
            idx = df.index[df['title'] == title][0]
            visited_indices.append(idx)
        else:
            print(f"Article '{title}' not found in the database.")

    if not visited_indices:
        print("No visited articles found.")
        return pd.DataFrame()

    user_profile = tfidf_matrix[visited_indices].mean(axis=0)
    user_profile = np.asarray(user_profile)

    similarities = cosine_similarity(user_profile, tfidf_matrix).flatten()

    results = pd.DataFrame({
        'title': df['title'],
        'url': df['url'],
        'similarity': similarities
    })

    results = results[~results['title'].isin(visited_titles)]

    recommendations = results.sort_values(by='similarity', ascending=False).head(top_n)
    return recommendations

visited_articles = [
    "Day of the Foundation of the Republic",
    "Nonviolent resistance"
]

top_recommendations = recommend_similar_articles(visited_articles, top_n=10)
print("\nTop Recommended Articles:")
print(top_recommendations)
