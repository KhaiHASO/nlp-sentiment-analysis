# DistilBERT Sentiment Analysis Demo

This project demonstrates sentiment analysis using DistilBERT fine-tuned on the SST-2 dataset from Hugging Face.

## Features

### Web Interface
- **Giao diện đẹp**: Thiết kế hiện đại, thân thiện với người dùng
- **Hỗ trợ tiếng Việt**: Giao diện hoàn toàn bằng tiếng Việt
- **Phân tích tương tác**: Nhập văn bản và nhận kết quả ngay lập tức
- **Ví dụ mẫu**: 10 câu mẫu có sẵn để thử nghiệm
- **Hiển thị trực quan**: Biểu đồ độ tin cậy và emoji cảm xúc
- **Responsive**: Tương thích với mọi thiết bị

### Technical Features
- **DistilBERT Model**: Sử dụng `distilbert-base-uncased-finetuned-sst-2-english` từ Hugging Face
- **Sentiment Analysis**: Phân loại văn bản thành tích cực/tiêu cực
- **Confidence Score**: Hiển thị độ tin cậy của kết quả phân tích
- **Real-time**: Phân tích nhanh chóng và chính xác

## Installation

### Using conda (Recommended)
```bash
# Create a new conda environment
conda create -n sentiment-analysis python=3.9
conda activate sentiment-analysis

# Install PyTorch via conda
conda install pytorch torchvision torchaudio cpuonly -c pytorch

# Install other dependencies via pip
pip install transformers datasets accelerate scikit-learn numpy pandas matplotlib seaborn
```

### Using pip
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface (Khuyến nghị)
```bash
# Với conda
conda activate sentiment-analysis
python app.py

# Với pip
python app.py
```
Sau đó mở trình duyệt và truy cập: `http://localhost:5000`

### Command Line Interface
```bash
# Với conda
conda activate sentiment-analysis
python distilbert_sentiment_demo.py

# Với pip
python distilbert_sentiment_demo.py
```

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
