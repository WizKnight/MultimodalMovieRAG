import requests
import os
from dotenv import load_dotenv
from typing import List, Dict
import urllib3
import re
import csv

load_dotenv()

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def fetch_movie_data(page: int = 1, session: requests.Session = None) -> List[Dict]:
    """Fetches movie data from TMDB API."""

    all_movies = []
    for page_num in range(1, 6):  # Fetch data from pages 1 to 6
        url = f"{TMDB_BASE_URL}/discover/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "page": page_num,
        }

        if session is None:
            session = requests

        response = session.get(url, params=params)
        response.raise_for_status()
        all_movies.extend(response.json()['results'])
    return all_movies

def extract_relevant_info(movies: List[Dict], session: requests.Session = None) -> List[Dict]:
    """Extracts relevant information from the movie data."""

    if session is None:
        session = requests

    processed_movies = []
    for movie in movies:
        genre_names = []
        for genre_id in movie["genre_ids"]:
            # Fetch genre details using the genre ID
            genre_url = f"{TMDB_BASE_URL}/genre/movie/list"
            genre_params = {
                "api_key": TMDB_API_KEY
            }
            genre_response = session.get(genre_url, params=genre_params)
            genre_response.raise_for_status()
            genres_data = genre_response.json()['genres']

            # Find the genre name with the matching ID
            for genre in genres_data:
                if genre['id'] == genre_id:
                    genre_names.append(genre['name'])
                    break

        # Fetch cast details
        cast_url = f"{TMDB_BASE_URL}/movie/{movie['id']}/credits"
        cast_params = {
            "api_key": TMDB_API_KEY
        }
        cast_response = session.get(cast_url, params=cast_params)
        cast_response.raise_for_status()
        cast_data = cast_response.json()['cast'][:5]  # Get top 5 cast members

        cast_names = [cast_member['name'] for cast_member in cast_data]

        processed_movies.append({
            "title": movie["title"],
            "overview": movie["overview"],
            "genres": genre_names,
            "cast": cast_names,
            "poster_url": f"{IMAGE_BASE_URL}{movie['poster_path']}" if movie['poster_path'] else None
        })
    return processed_movies

def download_posters(movies: List[Dict], output_dir: str = "posters"):
    """Downloads movie posters."""

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for movie in movies:
        if movie['poster_url']:
            try:
                response = requests.get(movie['poster_url'], stream=True)
                response.raise_for_status()

                # Construct the filename using the movie title from the movie data
                filename = re.sub(r'[\\/:"*?<>|]+', '', movie['title']) + ".jpg"
                image_path = os.path.join(output_dir, filename)

                with open(image_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

            except requests.exceptions.RequestException as e:
                print(f"Error downloading poster for {movie['title']}: {e}")
                    
def save_movie_data_to_csv(movies: List[Dict], output_file: str = "movies.csv"):
    """Saves the processed movie data to a CSV file."""

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'overview', 'genres', 'cast', 'poster_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for movie in movies:
            writer.writerow(movie)
                    

if __name__ == "__main__":
    # Configure requests to use urllib3
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=100,
        pool_maxsize=100,
        max_retries=urllib3.Retry(total=5, backoff_factor=0.1)
    )
    session = requests.Session()
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    # Use the session object for making requests
    movies = fetch_movie_data(session=session)
    processed_movies = extract_relevant_info(movies, session=session)
    download_posters(processed_movies)
    save_movie_data_to_csv(processed_movies)