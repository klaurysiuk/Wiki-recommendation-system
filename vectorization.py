import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('wiki_processed.csv', encoding='utf-8')
documents = df['text'].astype(str).tolist()
tfidf = TfidfVectorizer(use_idf=True, smooth_idf=False)
tfidf_matrix = tfidf.fit_transform(documents)
df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), index=df['title'], columns=tfidf.get_feature_names_out())
print(df_tfidf)

query = "korean civil war"
query_vec = tfidf.transform([query])
similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
results = pd.DataFrame({
    'title': df['title'],
    'url': df['url'],
    'similarity': similarities
})
results_sorted = results.sort_values(by='similarity', ascending=False)
top_articles = results_sorted.head(10)
print(top_articles)