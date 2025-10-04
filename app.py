# Sentiment Analysis App - DistilBERT + Streamlit
# pip install streamlit transformers torch

import streamlit as st
from transformers import pipeline

# Load model từ Hugging Face (lần đầu chạy sẽ tự tải về)
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", 
                    model="distilbert-base-uncased-finetuned-sst-2-english")

classifier = load_model()

# Giao diện web
st.title("🎭 Sentiment Analysis App")
st.write("Ứng dụng phân tích cảm xúc bằng DistilBERT (Positive / Negative)")

# Sample examples
st.subheader("📝 Sample Examples")
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
    st.write("**😊 Positive Examples (Clear & Obvious):**")
    for i, text in enumerate(positive_examples):
        if st.button(f"😊 {text[:35]}...", key=f"pos_{i}"):
            st.session_state.selected_text = text

with col2:
    st.write("**😔 Negative Examples (Clear & Obvious):**")
    for i, text in enumerate(negative_examples):
        if st.button(f"😔 {text[:35]}...", key=f"neg_{i}"):
            st.session_state.selected_text = text

st.divider()

# Input text
st.subheader("✍️ Enter Text to Analyze")
user_input = st.text_area(
    "Nhập câu hoặc đoạn văn bản:", 
    value=st.session_state.get('selected_text', ''),
    height=100
)

if st.button("🔍 Phân tích", type="primary"):
    if user_input.strip():
        with st.spinner("Đang phân tích..."):
            result = classifier(user_input)[0]
            label = result['label']
            score = round(result['score'] * 100, 2)
            
            # Hiển thị kết quả với style đẹp hơn
            if label == "POSITIVE":
                st.success(f"✅ **Sentiment: {label}** (Confidence: {score}%)")
                st.balloons()
            else:
                st.error(f"❌ **Sentiment: {label}** (Confidence: {score}%)")
            
            # Hiển thị thêm thông tin
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Confidence", f"{score}%")
            with col2:
                st.metric("Model", "DistilBERT")
            with col3:
                st.metric("Dataset", "SST-2")
    else:
        st.warning("⚠️ Vui lòng nhập văn bản để phân tích.")
