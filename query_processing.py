import pinecone
import os

from embeddings_generation import generate_text_embeddings, generate_image_embeddings

# Pinecone Constants
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

def init_pinecone():
    """Initializes the Pinecone connection."""
    return pinecone.Pinecone(api_key=PINECONE_API_KEY)


def query_pinecone(pinecone_instance, index_name: str, query_text: str, image_path: str, top_k: int = 10):
    """Queries the Pinecone index with text and image."""

    index = pinecone_instance.Index(index_name)

    # Generate embeddings for the query text and image
    text_embedding = generate_text_embeddings(query_text)
    image_embedding = generate_image_embeddings(image_path)

    # Combine the embeddings
    query_embedding = text_embedding + image_embedding

    # Perform the query
    result = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    return result


if __name__ == "__main__":
    pinecone_instance = init_pinecone()

    # Example usage
    query_text = "What is a movie about space adventure?"
    image_path = ".\posters\Apocalypse Z The Beginning of the End.jpg"
    
    query_result = query_pinecone(pinecone_instance, index_name="movie-rag", query_text=query_text, image_path=image_path)

    print(query_result)