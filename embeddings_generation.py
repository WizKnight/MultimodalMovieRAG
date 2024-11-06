from sentence_transformers import SentenceTransformer
from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image

# Load SentenceTransformer model
text_model = SentenceTransformer("all-mpnet-base-v2")

# Load the clip model
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def generate_text_embeddings(text:str) -> list:
    """Generates text embeddings using SentenceTransformer"""
    return text_model.encode(text).tolist()

def generate_image_embeddings(image_path: str) -> list:
    """Generates image embeddings using Hugging Face Transformers CLIP."""
    image = Image.open(image_path)
    inputs = clip_processor(text=None, images=image, return_tensors="pt", padding=True)

    with torch.no_grad():
        image_features = clip_model.get_image_features(**inputs)

    return image_features.squeeze().tolist()

## For quick testing

#if __name__ == "__main__":
    # Example usage:
    text = "This is an example sentence."
    text_embedding = generate_text_embeddings(text)
    print("Text Embedding:", text_embedding)

    image_path = "E:\GitUploads\MultimodalMovieRAG\posters\A Quiet Place Day One.jpg"
    image_embedding = generate_image_embeddings(image_path)
    print("Image Embedding:", image_embedding)