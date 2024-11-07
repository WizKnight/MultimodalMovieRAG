import gradio as gr
import pinecone
import tempfile
import os

from query_processing import query_pinecone

# Pinecone Constants
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

def init_pinecone():
    """Initializes the Pinecone connection."""
    return pinecone.Pinecone(api_key=PINECONE_API_KEY)

# Initialize Pinecone
pinecone_instance = init_pinecone()

def multimodal_movie_search(query_text: str, uploaded_image, top_k=5):
    """Performs the multimodal movie search."""
    if query_text and uploaded_image is not None:
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
            uploaded_image.save(temp_image.name)
            image_path = temp_image.name
        
        query_result = query_pinecone(
            pinecone_instance,
            index_name="movie-rag",
            query_text=query_text,
            image_path=image_path
        )
        
        results = []
        
        for match in query_result['matches']:
            movie_info = match['metadata']
            results.append(
                (
                    movie_info['title'],
                    movie_info['overview'],
                    ', '.join(movie_info['genres']),
                    ', '.join(movie_info['cast']),
                    movie_info['poster_url']
                )
            )
        return results[:top_k]
    
    else:
        return []
    
# Gradio Interface

iface = gr.Interface(
    fn = multimodal_movie_search,
    inputs=[
        gr.Textbox(lines=2, placeholder="Enter your query ..."),
        gr.Image(type="pil")
    ],
    outputs=gr.components.DataFrame(
        headers=["Title", "Overview", "Genres", "Cast", "Poster URL"],
        type="array",
    ),
    title="Multimodal Movie Search"
)
        
iface.launch(share=True)