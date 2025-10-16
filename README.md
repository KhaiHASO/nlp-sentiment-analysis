# Ứng Dụng Phân Tích Cảm Xúc DistilBERT

Ứng dụng web Streamlit đơn giản để phân tích cảm xúc sử dụng mô hình DistilBERT được fine-tune trên bộ dữ liệu SST-2 từ Hugging Face.

## 🎯 Tổng Quan Dự Án

Dự án này xây dựng một ứng dụng phân tích cảm xúc real-time sử dụng mô hình DistilBERT, cho phép người dùng nhập văn bản và nhận được kết quả phân tích cảm xúc (tích cực/tiêu cực) cùng với điểm tin cậy.

## ✨ Tính Năng

### Giao Diện Web
- **Streamlit UI**: Giao diện sạch sẽ, hiện đại với CSS tùy chỉnh
- **Phân Tích Real-time**: Phân tích cảm xúc tức thời khi người dùng nhập văn bản
- **Tải Model Trực Tiếp**: Tự động tải mô hình từ Hugging Face Hub
- **Caching Thông Minh**: Cache mô hình để tăng tốc các lần chạy tiếp theo
- **Input Đơn Giản**: Chỉ cần nhập văn bản và click phân tích

### Tính Năng Kỹ Thuật
- **Mô Hình DistilBERT**: Sử dụng `distilbert-base-uncased-finetuned-sst-2-english`
- **Phân Tích Cảm Xúc**: Phân loại văn bản thành POSITIVE hoặc NEGATIVE
- **Điểm Tin Cậy**: Hiển thị mức độ tin cậy của phân tích
- **Tự Động Tải**: Mô hình tự động tải về lần đầu chạy

## 🏗️ Kiến Trúc Hệ Thống

### 1. Kiến Trúc Tổng Quan
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   AI Model      │
│   (Streamlit)   │◄──►│   (Python)      │◄──►│   (DistilBERT)  │
│                 │    │                 │    │                 │
│ - Web Interface │    │ - Text Process  │    │ - Tokenization  │
│ - User Input    │    │ - Model Load    │    │ - Classification│
│ - Results Display│    │ - Cache Mgmt   │    │ - Confidence    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 2. Workflow Xử Lý
```
Input Text → Tokenization → Model Inference → Post-processing → Output
    ↓              ↓              ↓              ↓            ↓
User Input → Word Tokens → Neural Network → Softmax → Sentiment + Score
```

### 3. Kiến Trúc DistilBERT

#### 3.1 Cấu Trúc Mô Hình
```
Input Layer (Token Embeddings)
    ↓
Transformer Layers (6 layers thay vì 12 của BERT)
    ↓
Pooler Layer
    ↓
Classification Head (2 classes: POSITIVE/NEGATIVE)
    ↓
Output: [probability_negative, probability_positive]
```

#### 3.2 Chi Tiết Kiến Trúc
- **Embedding Layer**: Chuyển đổi tokens thành vectors 768 chiều
- **Transformer Layers**: 6 layers với Multi-Head Attention
- **Attention Heads**: 12 attention heads mỗi layer
- **Hidden Size**: 768 dimensions
- **Parameters**: ~66M (nhẹ hơn BERT ~40%)
- **Max Sequence Length**: 512 tokens

#### 3.3 Quá Trình Fine-tuning
- **Base Model**: DistilBERT-base-uncased
- **Dataset**: SST-2 (Stanford Sentiment Treebank v2)
- **Training**: Binary classification task
- **Accuracy**: ~91% trên test set

## 📁 Cấu Trúc Dự Án

```
nlp-sentiment-analysis/
├── app.py           # Ứng dụng Streamlit chính
├── distilbert.py    # Module model (load + analyze)
├── requirements.txt # Danh sách dependencies
├── README.md        # Tài liệu hướng dẫn
└── task1.png        # Mô tả task
```

## 🔧 Logic Source Code

### 1. File `app.py` - Ứng Dụng Streamlit

#### 1.1 Khởi Tạo và Cấu Hình
```python
# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Sentiment Analysis App",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

#### 1.2 Load Model với Caching
```python
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", 
                    model="distilbert-base-uncased-finetuned-sst-2-english")
```
**Giải thích**: 
- `@st.cache_resource`: Cache mô hình trong memory để tránh tải lại
- `pipeline()`: Wrapper của Hugging Face để sử dụng mô hình dễ dàng
- Model tự động tải về từ Hugging Face Hub lần đầu

#### 1.3 Xử Lý Input và Inference
```python
if analyze_clicked:
    if user_input.strip():
        with st.spinner("🤖 Đang phân tích cảm xúc..."):
            result = classifier(user_input)[0]
            label = result['label']
            score = round(result['score'] * 100, 2)
```
**Giải thích**:
- `classifier()`: Thực hiện inference trên mô hình
- `result[0]`: Lấy kết quả đầu tiên (có thể có nhiều câu)
- `label`: Nhãn phân loại (POSITIVE/NEGATIVE)
- `score`: Điểm tin cậy từ 0-1, chuyển thành phần trăm

#### 1.4 Hiển Thị Kết Quả
```python
if label == "POSITIVE":
    st.success(f"✅ **Sentiment: {label}** (Confidence: {score}%)")
    st.balloons()
else:
    st.error(f"❌ **Sentiment: {label}** (Confidence: {score}%)")
```

### 2. Module `distilbert.py` - Model Wrapper

```python
DEFAULT_MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"

def load_sentiment_pipeline(model_name: str = DEFAULT_MODEL_NAME):
    return pipeline("sentiment-analysis", model=model_name)

def analyze_text(classifier, text: str):
    result = classifier(text)[0]
    label = result.get("label", "").upper()
    if label.startswith("LABEL_"):
        label = "POSITIVE" if label.endswith("1") else "NEGATIVE"
    return {"label": label, "score": float(result.get("score", 0.0))}
```

## 🚀 Cài Đặt

### Sử dụng Conda (Khuyến nghị)
```bash
# Tạo môi trường conda mới
conda create -n sentiment-analysis python=3.9
conda activate sentiment-analysis

# Cài đặt PyTorch qua conda
conda install pytorch torchvision torchaudio cpuonly -c pytorch

# Cài đặt các dependencies khác qua pip
pip install streamlit transformers "numpy<2.0"
```

### Sử dụng pip
```bash
pip install -r requirements.txt
```

### Sửa lỗi NumPy (nếu cần)
Nếu gặp xung đột phiên bản NumPy, chạy:
```bash
pip install "numpy<2.0"
```

## 🎮 Cách Sử Dụng

### Chạy Ứng Dụng Streamlit (DistilBERT)
```bash
streamlit run distilbert_app.py
```

### Chạy Ứng Dụng Streamlit (ViSoBERT)
```bash
streamlit run visobert_app.py
```

### Chạy Ứng Dụng Streamlit (Multilingual 5-class)
```bash
streamlit run multilingual_app.py
```

<!-- CLI demo for ViSoBERT đã được loại bỏ để đơn giản hoá codebase. -->

## 📊 Demo Thực Hiện

### 1. Tải Mô Hình
- Tự động tải DistilBERT model fine-tuned trên SST-2
- Cache model để tăng tốc các lần chạy tiếp theo

### 2. Phân Tích Mẫu
- Phân tích 10 văn bản mẫu có sẵn
- Hiển thị kết quả sentiment và confidence score

### 3. Visualization
- Tạo biểu đồ tròn (pie chart) phân bố sentiment
- Tạo histogram phân bố confidence score
- Lưu kết quả thành `sentiment_analysis_results.png`

### 4. Chế Độ Tương Tác
- Cho phép người dùng test với văn bản tự nhập
- Nhập 'quit' để thoát

## 🤖 Chi Tiết Mô Hình

### Thông Số Kỹ Thuật
- **Mô Hình**: DistilBERT (phiên bản distilled của BERT)
- **Dataset**: SST-2 (Stanford Sentiment Treebank v2)
- **Task**: Binary sentiment classification (positive/negative)
- **Ngôn Ngữ**: Tiếng Anh
- **Nguồn**: Hugging Face Model Hub
- **Kích Thước**: ~66M parameters
- **Accuracy**: ~91% trên test set

### Kiến Trúc DistilBERT vs BERT
| Thông Số | BERT-base | DistilBERT |
|----------|-----------|------------|
| Layers | 12 | 6 |
| Parameters | 110M | 66M |
| Speed | 1x | 2x |
| Size | 440MB | 250MB |
| Accuracy | 100% | 97% |

## 📈 Kết Quả Đầu Ra

Demo sẽ:
- In kết quả phân tích sentiment cho các văn bản mẫu
- Hiển thị điểm tin cậy cho mỗi prediction
- Lưu visualization dưới dạng `sentiment_analysis_results.png`
- Cho phép test tương tác với văn bản tùy chỉnh

## 💡 Ví Dụ Kết Quả

```
1. Text: "This movie is absolutely fantastic!"
   Sentiment: POSITIVE (Confidence: 0.9998)

2. Text: "I hate this product, it's terrible."
   Sentiment: NEGATIVE (Confidence: 0.9999)

3. Text: "The weather is okay today."
   Sentiment: POSITIVE (Confidence: 0.6543)
```

## 🔍 Giải Thích Logic Phân Tích

### 1. Quá Trình Tokenization
```
Input: "I love this movie!"
↓
Tokens: ["[CLS]", "i", "love", "this", "movie", "!", "[SEP]"]
↓
Token IDs: [101, 1045, 2293, 2023, 3185, 999, 102]
```

### 2. Quá Trình Inference
```
Token Embeddings (768D) → Transformer Layers → Pooler → Classification Head
↓
Hidden States → Attention Weights → Contextual Representations → Logits
↓
Softmax → Probabilities → [P(negative), P(positive)]
```

### 3. Post-processing
```python
# Lấy label có probability cao nhất
label = "POSITIVE" if probabilities[1] > probabilities[0] else "NEGATIVE"
confidence = max(probabilities)
```

## 📋 Yêu Cầu Hệ Thống

- **Python**: 3.7+
- **PyTorch**: Framework deep learning
- **Transformers**: Thư viện Hugging Face
- **Streamlit**: Framework web app
- **Các dependencies**: Xem trong requirements.txt

## 🎯 Ứng Dụng Thực Tế

### 1. Social Media Monitoring
- Phân tích sentiment của posts, comments
- Theo dõi brand reputation
- Phát hiện crisis management

### 2. Customer Service
- Phân tích feedback khách hàng
- Tự động phân loại tickets
- Cải thiện chất lượng dịch vụ

### 3. Market Research
- Phân tích review sản phẩm
- Nghiên cứu thị trường
- Competitor analysis

## 🔧 Troubleshooting

### Lỗi Thường Gặp

1. **NumPy Version Conflict**
   ```bash
   pip install "numpy<2.0"
   ```

2. **CUDA Out of Memory**
   - Sử dụng CPU-only version của PyTorch
   - Giảm batch size

3. **Model Download Failed**
   - Kiểm tra kết nối internet
   - Sử dụng VPN nếu cần

4. **Streamlit Port Conflict**
   ```bash
   streamlit run app.py --server.port 8502
   ```

## 📚 Tài Liệu Tham Khảo

- [DistilBERT Paper](https://arxiv.org/abs/1910.01108)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [SST-2 Dataset](https://nlp.stanford.edu/sentiment/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 👥 Đóng Góp

Mọi đóng góp đều được chào đón! Vui lòng:
1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📄 License

Dự án này được phân phối dưới MIT License. Xem file `LICENSE` để biết thêm chi tiết.