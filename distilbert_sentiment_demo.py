"""
DistilBERT Fine-tuned on SST-2 Sentiment Analysis Demo
Based on Hugging Face transformers library
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_distilbert_model():
    """Load DistilBERT model fine-tuned on SST-2 dataset"""
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    
    print(f"Loading model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    
    return tokenizer, model

def create_sentiment_pipeline():
    """Create sentiment analysis pipeline"""
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    classifier = pipeline("sentiment-analysis", model=model_name)
    return classifier

def analyze_sentiment(classifier, text):
    """Analyze sentiment of input text"""
    result = classifier(text)
    return result

def demo_sentiment_analysis():
    """Demo function showing sentiment analysis capabilities"""
    print("=== DistilBERT Sentiment Analysis Demo ===\n")
    
    # Load the model
    classifier = create_sentiment_pipeline()
    
    # Sample texts for testing
    sample_texts = [
        "This movie is absolutely fantastic!",
        "I hate this product, it's terrible.",
        "The weather is okay today.",
        "I love spending time with my family.",
        "This is the worst experience ever.",
        "The service was excellent and professional.",
        "I'm not sure how I feel about this.",
        "This book changed my life completely!",
        "The food was disgusting and cold.",
        "Amazing performance by the actors!"
    ]
    
    print("Analyzing sentiment for sample texts:\n")
    
    results = []
    for i, text in enumerate(sample_texts, 1):
        result = analyze_sentiment(classifier, text)
        label = result[0]['label']
        score = result[0]['score']
        
        # Convert LABEL_0/1 to POSITIVE/NEGATIVE
        sentiment = "POSITIVE" if label == "LABEL_1" else "NEGATIVE"
        
        print(f"{i:2d}. Text: \"{text}\"")
        print(f"    Sentiment: {sentiment} (Confidence: {score:.4f})")
        print()
        
        results.append({
            'text': text,
            'sentiment': sentiment,
            'confidence': score
        })
    
    return results

def visualize_results(results):
    """Create visualization of sentiment analysis results"""
    df = pd.DataFrame(results)
    
    # Count sentiments
    sentiment_counts = df['sentiment'].value_counts()
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Pie chart
    ax1.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', 
            colors=['lightcoral', 'lightblue'])
    ax1.set_title('Sentiment Distribution')
    
    # Confidence distribution
    ax2.hist(df['confidence'], bins=10, alpha=0.7, color='skyblue', edgecolor='black')
    ax2.set_xlabel('Confidence Score')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Confidence Score Distribution')
    ax2.axvline(df['confidence'].mean(), color='red', linestyle='--', 
                label=f'Mean: {df["confidence"].mean():.3f}')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('sentiment_analysis_results.png', dpi=300, bbox_inches='tight')
    plt.show()

def interactive_demo():
    """Interactive demo for custom text input"""
    print("\n=== Interactive Sentiment Analysis ===")
    print("Enter your own text for sentiment analysis (type 'quit' to exit):\n")
    
    classifier = create_sentiment_pipeline()
    
    while True:
        user_input = input("Enter text: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            print("Please enter some text.")
            continue
        
        try:
            result = analyze_sentiment(classifier, user_input)
            label = result[0]['label']
            score = result[0]['score']
            sentiment = "POSITIVE" if label == "LABEL_1" else "NEGATIVE"
            
            print(f"Sentiment: {sentiment}")
            print(f"Confidence: {score:.4f}")
            print("-" * 50)
            
        except Exception as e:
            print(f"Error analyzing text: {e}")

def main():
    """Main function to run the demo"""
    try:
        # Run the demo
        results = demo_sentiment_analysis()
        
        # Create visualization
        print("Creating visualization...")
        visualize_results(results)
        
        # Interactive demo
        interactive_demo()
        
    except Exception as e:
        print(f"Error running demo: {e}")
        print("Make sure you have installed all required dependencies:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()
