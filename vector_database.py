import csv
import os
from typing import List, Dict
import unicodedata
import re

import pinecone

from embeddings_generation import generate_text_embeddings, generate_image_embeddings

# Pinecone Constants
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

def init_pinecone():
    """Initializes the Pinecone connection."""
    return pinecone.Pinecone(api_key=PINECONE_API_KEY)

def create_index(pinecone_instance, index_name: str, dimension: int):
    """Creates a Pinecone index if it doesn't exist."""

    if index_name not in pinecone_instance.list_indexes().names():
        pinecone_instance.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine"
        )
    else:  
        index_info = pinecone_instance.describe_index(index_name)
        dimension = index_info.dimension

    return dimension

def upsert_data(pinecone_instance, index_name: str, data: list):
    """Upserts data into the Pinecone index."""
    index = pinecone_instance.Index(index_name)

    # Upsert data in batches of 100
    batch_size = 100
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]

        # Ensure vector IDs are ASCII
        for j, (vector_id, values, metadata) in enumerate(batch):
            try:
                vector_id.encode('ascii')
            except UnicodeEncodeError:
                # Replace non-ASCII characters with their closest ASCII equivalents
                ascii_id = unicodedata.normalize('NFKD', vector_id).encode('ascii', 'ignore').decode('ascii')
                batch[j] = (ascii_id, values, metadata)  # Update the batch with the ASCII ID

        index.upsert(batch)

def load_movie_data(csv_file: str = "movies.csv") -> List[Dict]:
    """Loads movie data from the CSV file."""
    movie_data = []
    poster_files = os.listdir("posters")  # Get the list of files in the posters directory

    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Extract the movie title from the row['title'] (this should match the poster filenames)
            movie_title = row['title']  

            # Sanitize the title to match the filename format
            sanitized_title = re.sub(r'[\\/:"*?<>|]+', '', movie_title) + ".jpg"

            # Find the corresponding poster file (case-insensitive)
            poster_file = next((f for f in poster_files if f.lower() == sanitized_title.lower()), None)

            if poster_file:
                poster_path = os.path.join("posters", poster_file)
                row["poster_url"] = poster_path
                movie_data.append(row)
            else:
                print(f"Warning: Poster file not found for {movie_title} (Sanitized: {sanitized_title})")

    return movie_data


if __name__ == "__main__":
    pinecone_instance = init_pinecone()
    create_index(pinecone_instance, "movie-rag",1280)

    movie_data = load_movie_data()  # Load data from movies.csv

    upsert_data_list = []
    for movie in movie_data:
        text_embedding = generate_text_embeddings(movie["overview"])
        image_path = movie["poster_url"]

        # Check if the image file exists before generating embeddings
        if os.path.exists(image_path):
            try:
                image_embedding = generate_image_embeddings(image_path)
            except Exception as e:
                print(f"Error generating image embedding for {movie['title']}: {e}")
                image_embedding = None
        else:
            print(f"Skipping image embedding for {movie['title']} due to missing file: {image_path}")
            image_embedding = None

        # Ensure embeddings are lists and not None
        if text_embedding is None or image_embedding is None:
            print(f"Skipping movie {movie['title']} due to missing embedding.")
            continue

        if not isinstance(text_embedding, list) or not isinstance(image_embedding, list):
            print(f"Skipping movie {movie['title']} due to invalid embedding format.")
            continue

        upsert_data_list.append((
            movie["title"],  # Using movie title as ID
            text_embedding + image_embedding, 
            {
                "title": movie["title"],
                "overview": movie["overview"],
                "genres": movie["genres"].split(', ') if movie["genres"] else [],
                "cast": movie["cast"].split(', ') if movie["cast"] else [],
                "poster_url": movie["poster_url"]
            }
        ))

    upsert_data(pinecone_instance, "movie-rag", upsert_data_list)