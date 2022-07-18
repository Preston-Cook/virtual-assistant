import json
import requests

from api_secrets import MOVIE_DB_API_KEY

def get_trending_media(prompt):
    
    # Check user's speech for keywords
    spec = 'movie' if 'movie' in prompt else 'tv'

    # Initialize service URL
    url = f'https://api.themoviedb.org/3/trending/{spec}/day?api_key={MOVIE_DB_API_KEY}'

    # Collect response through GET request
    response = requests.get(url)

    # Check HTTP response
    if response.status_code != 200:
        return 'Unable to fetch trending media data'
    
    # Convert json str to dict
    data = json.loads(response.text)

    # Check if user specified movie and pull top movies
    if spec == 'movie':
        trending_movies = [data['results'][i]['title'] for i in range(5)]
        return f'Currently, the top trending movies include {trending_movies[0]},{trending_movies[1]},{trending_movies[2]},{trending_movies[3]}, and {trending_movies[4]}'
    
    # Else check for shows
    trending_tv = [data['results'][i]['name'] for i in range(5)]
    return f'Currently, the top trending shows include {trending_tv[0]},{trending_tv[1]},{trending_tv[2]},{trending_tv[3]}, and {trending_tv[4]}'