# All imports at the top
import pandas as pd
import gradio as gr
from transformers import BertTokenizer, BertForSequenceClassification
import os

# Define the sentiment mapping (adjust if needed)
sentiment_mapping = {'positive': 2, 'negative': 0, 'neutral': 1}
reverse_sentiment_mapping = {v: k for k, v in sentiment_mapping.items()}

# Define the save directory for the model and tokenizer
# This path is relative to the app.py file
save_directory = "fine_tuned_bert_model"

# Load the fine-tuned model and tokenizer from the relative directory
# This assumes the 'fine_tuned_bert_model' folder is in your GitHub repo
try:
    loaded_tokenizer = BertTokenizer.from_pretrained(save_directory)
    loaded_model = BertForSequenceClassification.from_pretrained(save_directory)
except OSError:
    print("Model or tokenizer not found in the 'fine_tuned_bert_model' directory.")
    print("Please ensure this directory is uploaded to your GitHub repository.")
    exit()

# Define a function for prediction
def predict_sentiment(text):
    # Tokenize the input text
    inputs = loaded_tokenizer(text, return_tensors="pt", padding=True, truncation=True)

    # Make a prediction
    outputs = loaded_model(**inputs)
    logits = outputs.logits
    predictions = logits.argmax(dim=-1)

    # Map the prediction back to sentiment label
    predicted_sentiment = reverse_sentiment_mapping[predictions.item()]
    return predicted_sentiment

# Create the Gradio interface
interface = gr.Interface(
    fn=predict_sentiment,
    inputs=gr.Textbox(lines=2, placeholder="Enter text here to analyze sentiment..."),
    outputs="text",
    title="BERT Sentiment Analysis",
    description="Enter text to analyze its sentiment (Positive, Negative, or Neutral) using a fine-tuned BERT model.",
    examples=[
        ["I absolutely loved this movie, it was fantastic!"],
        ["The service was terrible, I'm very disappointed."],
        ["The weather is cloudy today with a chance of rain."],
        ["This product exceeded my expectations."],
        ["I have no strong feelings about this."]
    ]
)

# Launch the interface
print("Launching Gradio interface...")
interface.launch()
