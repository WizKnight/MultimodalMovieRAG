# Multimodal Movie Search 🍿

This project demonstrates a multimodal movie search engine using Retrieval Augmented Generation (RAG) techniques.
It allows users to search for movies using both text queries and images.

## Features 🚅

*   **Multimodal Search:** Search for movies using a combination of text and images.
*   **Efficient Retrieval:** Uses Pinecone vector database for fast and efficient similarity search.
*   **Interactive Interface:** Provides a user-friendly interface built with Gradio.

## How it works 🛠️

1.  **Data Preparation:**
    *   Movie data (title, overview, genres, cast, poster URL) is fetched from the TMDB API.
    *   Movie posters are downloaded and stored locally.
2.  **Embedding Generation:**
    *   Text embeddings are generated for movie overviews using SentenceTransformer.
    *   Image embeddings are generated for movie posters using Hugging Face Transformers CLIP.
3.  **Vector Database:**
    *   Text and image embeddings are combined and stored in a Pinecone index.
4.  **Query Processing:**
    *   User provides a text query and an image.
    *   Embeddings are generated for the query text and image.
    *   Embeddings are combined into a single query vector.
5.  **Similarity Search:**
    *   The query vector is used to search for similar movies in the Pinecone index.
6.  **Retrieval and Display:**
    *   The most similar movies are retrieved from Pinecone.
    *   Movie information and posters are displayed in the Gradio interface.

## Setup and Usage 🤳

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/WizKnight/MultimodalMovieRAG.git](https://github.com/WizKnight/MultimodalMovieRAG.git)
    ```

2.  **Create a virtual environment:**
    ```bash
    python3.10 -m venv .venv 
    source .venv/bin/activate  # On Linux/macOS
    .venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Pinecone:**
    *   Create a Pinecone account and an index.
    *   Set the `PINECONE_API_KEY` API key variable with your Pinecone credentials.

5.  **Run the data preparation script:**
    ```bash
    python data_preparation.py
    ```
    This will fetch movie data, download posters, and store them in the `posters` directory.

6.  **Run the vector database script:**
    ```bash
    python vector_database.py
    ```
    This will generate embeddings for the movie data and upsert them into the Pinecone index.

7.  **Run the Gradio app:**
    ```bash
    python movierag.py
    ```
    This will launch the Gradio interface in your web browser.

## Usage

1.  Enter your text query in the textbox.
2.  Upload an image using the image uploader.
3.  Click the "Search" button.
4.  The app will display the most similar movies with their information and posters.

## Demo Video

[![Multimodal Movie Search Demo](add_link.gif)](https://www.loom.com/)

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the [Apache-2.0 license]([LICENSE](https://github.com/WizKnight/MultimodalMovieRAG/blob/main/LICENSE))
