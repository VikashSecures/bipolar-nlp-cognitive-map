
from transformers import pipeline

# Load pre-trained BERT model for Named Entity Recognition (NER)
ner_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

# Input sentence
sentence = "Dr. Smith, a renowned psychiatrist, published a groundbreaking study on bipolar disorder treatment in the Journal of Psychiatry on March 10, 2024."

# Perform entity extraction
entities = ner_model(sentence)

# Display the entities
for entity in entities:
    print(f"Entity: {entity['word']}, Type: {entity['entity']}, Confidence: {entity['score']:.2f}")
