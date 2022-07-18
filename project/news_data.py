import json
import requests

from api_secrets import NEWS_API_KEY

def get_news(prompt):

    # split prompt data to check for keywords
    pieces = prompt.split()

    # Check if the user requested news ON something
    if 'on' in pieces or 'about' in pieces:
        if 'on' in pieces:
            subject = pieces[pieces.index('on') + 1].lower()
        else:
            subject =  pieces[pieces.index('about') + 1].lower()
        
        # Narrow Search to solely include subject 
        url = f'https://newsapi.org/v2/everything?q={subject}&apiKey={NEWS_API_KEY}'
    
    else:
        # Give general US news
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'

    # Call API via GET request
    response = requests.get(url)

    # Check for HTTP response errors
    if response.status_code != 200:
        return "I'm unable to gather data on the news"
    
    # Convert string to dict
    news_data = json.loads(response.text)

    # Collect headlines from response
    headlines = [news_data['articles'][i]['title'] for i in range(3)]
    
    # Output formatted data with headlines
    return f'In the news: {headlines[0]}, {headlines[1]}, and {headlines[2]}'