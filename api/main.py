from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from numpy import dot
import pandas as pd
from gensim.models import KeyedVectors

# Load the model
model_path = "model.bin"  # Replace with your model path
embeddings_index = KeyedVectors.load_word2vec_format(model_path, binary=True)


# Helper Functions
# Calculates cosine similarity between two vectors.
def cosine_similarity(vec1, vec2):
    return dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


# Averages word vectors to create a sentence vector,
# handling out-of-vocabulary (OOV) words gracefully.
def get_sentence_vector(sentence, embeddings_index):
    word_vectors = []
    for word in sentence.split():
        if word in embeddings_index.key_to_index:  # Use key_to_index instead of vocab
            word_vectors.append(embeddings_index[word])  # Access word vector directly
    if not word_vectors:
        # Handle empty sentence or all OOV words
        return np.zeros(embeddings_index.vector_size)
    return np.mean(word_vectors, axis=0)


# Reading the Quranic date
json_file_path = "quran_data_v1_without_diacritic.json"
quranic_data = pd.read_json(json_file_path, encoding='utf-8')


app = Flask(__name__)
CORS(app)

@app.after_request
def ensure_utf8_encoding(response):
    response.charset = 'utf-8'
    return response


# Define an endpoint that takes a query as input and returns a JSON response
@app.route('/search', methods=['GET'])
def query_endpoint():
    query = request.args.get('query')
    quranic_searching_column = quranic_data["tafseer"]

    # Get sentence vectors for the list and query
    list_vectors = [get_sentence_vector(sentence, embeddings_index) for sentence in quranic_searching_column]
    query_vector = get_sentence_vector(query, embeddings_index)

    # Calculate cosine similarities between the query and each list item
    similarities = [cosine_similarity(query_vector, list_vector) for list_vector in list_vectors]
    print("similarities", similarities)

    # Convert the list of similarities to a NumPy array
    similarities_array = np.array(similarities)

    # Filter indices of values in similarities array that are greater than 0.61
    indices = np.where(similarities_array > 0.61)[0]

    # Filter the similarities array using the indices
    filtered_similarities = similarities_array[indices]

    # Sort the filtered similarities in descending order and get the sorted indices
    sorted_indices = np.argsort(filtered_similarities)[::-1]

    # Get the top 3 highest similarities and their corresponding indices
    top_3_indices = indices[sorted_indices[:3]]

    # Print the rows from quranic_data that match the top 3 indices
    print("Top 3 closest matches:")
    pd.set_option('display.max_colwidth', None)
    top_3_rows = quranic_data.iloc[top_3_indices].to_dict(orient='records')
    print(top_3_rows)

    # Return a JSON response
    response = {
        'query': query,
        'message': f'You sent the query: {query}',
        'data': top_3_rows
    }

    return jsonify(response)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
