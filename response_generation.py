import pinecone
import os
from dotenv import load_dotenv

from query_processing import query_pinecone

load_dotenv()

# Pinecone Constants
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
#PINECONE_ENVIRONMENT = os.environ.get('PINECONE_ENVIRONMENT')

def init_pinecone():
    """Initializes the Pinecone connection."""
    return pinecone.Pinecone(api_key=PINECONE_API_KEY)

def generate_response(query_result: dict) -> str:
    """Generates a user-friendly response from the query result."""

    response = "Here are some movies that match your query:\n\n"

    if query_result['matches']:
        for match in query_result['matches']:
            movie_info = match['metadata']
            response += f"**Title:** {movie_info['title']}\n"
            response += f"**Overview:** {movie_info['overview']}\n"
            response += f"**Genres:** {', '.join(movie_info['genres'])}\n"
            response += f"**Cast:** {', '.join(movie_info['cast'])}\n"
            response += f"**Poster URL:** {movie_info['poster_url']}\n\n"
    else:
        response += "No movies found matching your query.\n"

    return response

if __name__ == "__main__":
    pinecone_instance = init_pinecone()

    # Example usage
    query_text = "What is a movie about superheroes?"
    image_path = ".\posters\Deadpool & Wolverine.jpg"

    query_result = query_pinecone(pinecone_instance, index_name="movie-rag", query_text=query_text, image_path=image_path)

    user_response = generate_response(query_result)

    print(user_response)