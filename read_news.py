import os
import requests
from datetime import datetime, timedelta
from newspaper import Article


def get_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return f"Error retrieving article: {e}"

def get_article_text(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            article = Article(url)
            article.download(input_html=response.text)
            article.parse()
            return article.text
        else:
            return f"Error retrieving article: Status code {response.status_code}"
    except Exception as e:
        return f"Error retrieving article: {e}"

def get_stock_news(symbol, page_size=5):
    api_key = os.getenv('NEWSAPI_KEY')
    # Define the endpoint and parameters
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': symbol,
        'sortBy': 'publishedAt',
        'pageSize': page_size,
        'apiKey': api_key,
        'language': 'en'
    }
    
    # Make the request to the News API
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data['articles']
        dicts=[]
        # Process and print the top 5 news stories
        for i, article in enumerate(articles[:page_size], 1):
            article_text = get_article_text(article['url'])
            
            d=dict(Title=article['title'],
                    Description=article['description'],
                    PublishedAt=article['publishedAt'][:10],
                    URL=article['url'],
                    Text=article_text)
            dicts.append(d)
            
    else:
        print(f"Failed to fetch news. Status code: {response.status_code}")
    return dicts

