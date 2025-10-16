# Sentiment Analysis App - DistilBERT + Streamlit
# pip install streamlit transformers torch

import streamlit as st
from distilbert import load_sentiment_pipeline, analyze_text, DEFAULT_MODEL_NAME

# Page config (phải đặt ở đầu)
st.set_page_config(
    page_title="Sentiment Analysis App",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load model từ Hugging Face (lần đầu chạy sẽ tự tải về)
@st.cache_resource
def load_model(model_name: str = DEFAULT_MODEL_NAME):
    return load_sentiment_pipeline(model_name)

# Sidebar
with st.sidebar:
    st.markdown("## ℹ️ Thông tin ứng dụng")
    st.markdown("""
    **🎭 Sentiment Analysis App**
    
    Ứng dụng phân tích cảm xúc sử dụng mô hình DistilBERT được huấn luyện trên bộ dữ liệu SST-2.
    
    **✨ Tính năng:**
    - Phân tích cảm xúc real-time
    - 30 sample examples rõ ràng
    - Hiển thị confidence score
    - Giao diện thân thiện
    
    **🤖 Model:**
    - **DistilBERT**: Mô hình BERT được tối ưu
    - **Dataset**: SST-2 (Stanford Sentiment Treebank)
    - **Accuracy**: ~91% trên test set
    """)
    
    st.markdown("---")
    st.markdown("### 🧠 Chọn mô hình")
    model_name = st.selectbox(
        "Hugging Face model",
        options=[
            DEFAULT_MODEL_NAME,
            "distilbert-base-uncased",
            "bert-base-uncased",
            "nlptown/bert-base-multilingual-uncased-sentiment",
        ],
        index=0,
        help="Chọn model để thử nghiệm. Một số model có thể cần mapping label khác",
    )
    classifier = load_model(model_name)
    st.markdown("### 📊 Thống kê")
    st.metric("Sample Examples", "30")
    st.metric("Model Size", "~66M params")
    st.metric("Supported Language", "English")
    
    st.markdown("---")
    st.markdown("### 🎯 Cách sử dụng")
    st.markdown("""
    1. **Click** vào sample examples
    2. **Hoặc nhập** văn bản của bạn
    3. **Click** "Phân tích cảm xúc"
    4. **Xem** kết quả và confidence
    """)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .example-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    .example-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .negative-card {
        border-left-color: #dc3545;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .result-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #e9ecef;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎭 Sentiment Analysis App</h1>
    <p style="font-size: 1.2rem; margin: 0;">Ứng dụng phân tích cảm xúc bằng DistilBERT (Positive / Negative)</p>
</div>
""", unsafe_allow_html=True)

# Sample examples
st.markdown("### 📝 Sample Examples")
st.markdown("*Click vào bất kỳ câu nào để tự động điền vào ô phân tích*")
sample_texts = [
    # Clear Positive Examples
    "I absolutely love this movie!",
    "This product is amazing and perfect!",
    "I love spending time with my family.",
    "The service was excellent and professional.",
    "This book completely changed my life!",
    "The actors' performance was outstanding!",
    "This is fantastic and wonderful!",
    "The sunset was beautiful tonight.",
    "I'm so grateful for your help.",
    "The concert was absolutely incredible!",
    "Thank you for the wonderful gift.",
    "This is the best day ever!",
    "I'm so happy and excited!",
    "This food is delicious and tasty.",
    "The weather is perfect today.",
    
    # Clear Negative Examples
    "This product is terrible and awful.",
    "This is the worst experience ever.",
    "The food was disgusting and cold.",
    "I hate this software, it's buggy.",
    "I'm disappointed with the quality.",
    "This movie was boring and pointless.",
    "I'm so angry and frustrated.",
    "This is horrible and disgusting.",
    "I hate waiting in long lines.",
    "This traffic is terrible and annoying.",
    "I'm sad and disappointed.",
    "This is awful and terrible.",
    "I hate this place completely.",
    "This is disgusting and horrible.",
    "I'm very upset and angry."
]

# Tạo 2 cột cho sample examples
col1, col2 = st.columns(2)

# Chia rõ ràng positive và negative
positive_examples = sample_texts[:15]  # 15 câu đầu là positive
negative_examples = sample_texts[15:]  # 15 câu sau là negative

with col1:
    st.markdown("#### 😊 Positive Examples")
    st.markdown("*Click để sử dụng*")
    
    # Tạo container cho positive examples
    for i, text in enumerate(positive_examples):
        with st.container():
            if st.button(f"😊 {text}", key=f"pos_{i}", use_container_width=True):
                st.session_state.selected_text = text
                st.rerun()

with col2:
    st.markdown("#### 😔 Negative Examples")
    st.markdown("*Click để sử dụng*")
    
    # Tạo container cho negative examples
    for i, text in enumerate(negative_examples):
        with st.container():
            if st.button(f"😔 {text}", key=f"neg_{i}", use_container_width=True):
                st.session_state.selected_text = text
                st.rerun()

st.divider()

# Input text section
st.markdown("### ✍️ Enter Text to Analyze")
st.markdown("*Nhập văn bản hoặc click vào sample examples ở trên*")

# Tạo container cho input
with st.container():
    user_input = st.text_area(
        "Nhập câu hoặc đoạn văn bản:", 
        value=st.session_state.get('selected_text', ''),
        height=120,
        placeholder="Ví dụ: I love this product! hoặc This is terrible..."
    )
    
    # Button với styling đẹp
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_clicked = st.button("🔍 Phân tích cảm xúc", type="primary", use_container_width=True)

if analyze_clicked:
    if user_input.strip():
        with st.spinner("🤖 Đang phân tích cảm xúc..."):
            result = analyze_text(classifier, user_input)
            label = result['label']
            score = round(result['score'] * 100, 2)
            
            # Container cho kết quả
            st.markdown("### 📊 Kết quả phân tích")
            
            # Hiển thị kết quả chính
            if label == "POSITIVE":
                st.success(f"✅ **Sentiment: {label}** (Confidence: {score}%)")
                st.balloons()
            else:
                st.error(f"❌ **Sentiment: {label}** (Confidence: {score}%)")
            
            # Metrics với styling đẹp
            st.markdown("#### 📈 Chi tiết phân tích")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{score}%</h3>
                    <p>Confidence</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>DistilBERT</h3>
                    <p>Model</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>SST-2</h3>
                    <p>Dataset</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                sentiment_icon = "😊" if label == "POSITIVE" else "😔"
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{sentiment_icon}</h3>
                    <p>Sentiment</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Hiển thị văn bản đã phân tích
            st.markdown("#### 📝 Văn bản đã phân tích:")
            st.info(f'"{user_input}"')
            
    else:
        st.warning("⚠️ Vui lòng nhập văn bản để phân tích.")
