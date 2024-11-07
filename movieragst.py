import streamlit as st
import pinecone
from PIL import Image
import requests
import os
from dotenv import load_dotenv

from query_processing import query_pinecone

load_dotenv()

# Access environment variables
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

TMDB_BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def init_pinecone():
    """Initializes the Pinecone connection."""
    return pinecone.Pinecone(api_key=PINECONE_API_KEY)

# Initialize Pinecone
pinecone_instance = init_pinecone()

# Streamlit App
st.title("Multimodal Movie Search")

# Text input for the query
query_text = st.text_input("Enter your query:")

# File uploader for the image
uploaded_image = st.file_uploader("Upload an image:", type=["jpg", "png", "jpeg"])

# Search button
if st.button("Search"):
    if query_text and uploaded_image is not None:
        # Perform the search
        query_result = query_pinecone(
            pinecone_instance,
            index_name="movie-rag",
            query_text=query_text,
            image_path=uploaded_image
        )

        # Display the response
        st.subheader("Search Results:")

        if query_result['matches']:
            for match in query_result['matches']:
                movie_info = match['metadata']
                with st.expander(movie_info['title']):
                    st.write(f"**Overview:** {movie_info['overview']}")
                    st.write(f"**Genres:** {', '.join(movie_info['genres'])}")
                    st.write(f"**Cast:** {', '.join(movie_info['cast'])}")

                    # Fetch and display the poster image in real-time
                poster_url = movie_info.get('poster_url')  
                if poster_url:
                    try:
                        st.image(poster_url, caption=movie_info['title'], use_container_width=True)
                    except Exception as e:
                        st.error(f"Error loading poster image: {e}")
                else:
                    st.warning("Poster not available for this movie.")
        else:
            st.info("No movies found matching your query.")
    else:
        st.warning("Please enter a query and upload an image.")