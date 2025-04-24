from sentence_transformers import SentenceTransformer, util
from .data import preprocessed_symptoms  # or use original_symptoms if aliasing


# Load the model once globally
model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight model

# Precompute symptom embeddings once and store them globally
symptom_embeddings = model.encode(preprocessed_symptoms, convert_to_tensor=True)

def match_symptom(user_input, preprocessed_symptoms, original_symptoms, threshold=0.55):
    try:
        # Generate embedding for the user input
        user_embedding = model.encode(user_input, convert_to_tensor=True)

        # Compute cosine similarity
        similarities = util.pytorch_cos_sim(user_embedding, symptom_embeddings).squeeze().tolist()

        # Find symptoms that meet the threshold
        matches = [
            (original_symptoms[i], score)
            for i, score in enumerate(similarities)
            if score >= threshold
        ]

        # Sort matches by score in descending order
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
    except Exception as e:
        print(f"Error during symptom matching: {e}")
        return []

def process_symptoms(user_input):
    # Get the matched symptoms directly without modifying the global variable
    return match_symptom(user_input, preprocessed_symptoms, preprocessed_symptoms, threshold=0.55)
