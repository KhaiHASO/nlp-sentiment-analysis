# DistilBERT Sentiment Analysis Demo

Simple Streamlit web application for sentiment analysis using DistilBERT fine-tuned on the SST-2 dataset from Hugging Face.

## Features

### Web Interface
- **Streamlit UI**: Clean, modern interface
- **Real-time Analysis**: Instant sentiment analysis
- **Direct Model Loading**: Downloads model directly from Hugging Face
- **Caching**: Model cached for faster subsequent runs
- **Simple Input**: Just type and click analyze

### Technical Features
- **DistilBERT Model**: Uses `distilbert-base-uncased-finetuned-sst-2-english` from Hugging Face
- **Sentiment Analysis**: Classifies text as POSITIVE or NEGATIVE
- **Confidence Score**: Shows confidence level of analysis
- **Auto Download**: Model downloads automatically on first run

## Installation

### Using conda (Recommended)
```bash
# Create a new conda environment
conda create -n sentiment-analysis python=3.9
conda activate sentiment-analysis

# Install PyTorch via conda
conda install pytorch torchvision torchaudio cpuonly -c pytorch

# Install other dependencies via pip
pip install streamlit transformers "numpy<2.0"
```

### Using pip
```bash
pip install -r requirements.txt
```

### Fix NumPy compatibility issue (if needed)
If you encounter NumPy version conflicts, run:
```bash
pip install "numpy<2.0"
```

## Usage

### Run Streamlit App
```bash
# With conda
conda activate sentiment-analysis
streamlit run app.py

# With pip
streamlit run app.py
```
Then open your browser and go to: `http://localhost:8501`

## What the Demo Does

1. **Loads the Model**: Downloads and loads the DistilBERT model fine-tuned on SST-2
2. **Sample Analysis**: Analyzes 10 pre-loaded sample texts
3. **Visualization**: Creates pie chart and histogram of results
4. **Interactive Mode**: Allows you to test your own text inputs

## Model Details

- **Model**: DistilBERT (distilled version of BERT)
- **Dataset**: SST-2 (Stanford Sentiment Treebank v2)
- **Task**: Binary sentiment classification (positive/negative)
- **Language**: English
- **Source**: Hugging Face Model Hub

## Output

The demo will:
- Print sentiment analysis results for sample texts
- Display confidence scores for each prediction
- Save a visualization as `sentiment_analysis_results.png`
- Allow interactive testing of custom text

## Example Output

```
1. Text: "This movie is absolutely fantastic!"
   Sentiment: POSITIVE (Confidence: 0.9998)

2. Text: "I hate this product, it's terrible."
   Sentiment: NEGATIVE (Confidence: 0.9999)
```

## Requirements

- Python 3.7+
- PyTorch
- Transformers library
- Other dependencies listed in requirements.txt
