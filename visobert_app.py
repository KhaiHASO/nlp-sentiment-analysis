import streamlit as st
from visobert import (
    load_fill_mask_pipeline,
    load_sentiment_pipeline,
)


st.set_page_config(
    page_title="ViSoBERT Demo",
    page_icon="🇻🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)


VISOBERT_MASK_MODEL = "5CD-AI/visobert-14gb-corpus"  # fill-mask
VISOBERT_SENTIMENT_MODEL = "5CD-AI/vietnamese-sentiment-visobert"  # sentiment


@st.cache_resource
def load_fill_mask():
    return load_fill_mask_pipeline()


@st.cache_resource
def load_sentiment():
    return load_sentiment_pipeline()


st.markdown("""
<div style="text-align:center; padding: 1.25rem 0;">
  <h1>🇻🇳 ViSoBERT Demo</h1>
  <p style="font-size: 1.1rem; margin: 0;">Fill-Mask và Sentiment cho tiếng Việt</p>
  <p style="margin: .25rem 0 0 0; font-size: .95rem;">
    Model tham chiếu: <code>5CD-AI/visobert-14gb-corpus</code> và <code>5CD-AI/vietnamese-sentiment-visobert</code>
  </p>
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("### Cấu hình")
    mode = st.radio("Chế độ", ["Fill-Mask", "Sentiment"], index=0)
    st.markdown("---")

    if mode == "Fill-Mask":
        top_k = st.slider("Top-k gợi ý", min_value=1, max_value=20, value=10)
        st.caption("Dùng cho câu có token <mask>")
    else:
        st.caption("Phân tích cảm xúc tiếng Việt (POS/NEG,... tuỳ mô hình)")

st.divider()


if mode == "Fill-Mask":
    st.markdown("#### 🧩 Fill-Mask")
    default_text = "shop làm ăn như cái <mask>"
    text = st.text_input("Nhập câu có <mask>:", value=default_text, placeholder="Ví dụ: chất lượng dịch vụ quá <mask>")

    examples_col1, examples_col2 = st.columns(2)
    with examples_col1:
        if st.button("Ví dụ 1", use_container_width=True):
            text = "shop làm ăn như cái <mask>"
        if st.button("Ví dụ 2", use_container_width=True):
            text = "Chất lượng dịch vụ quá <mask>"
    with examples_col2:
        if st.button("Ví dụ 3", use_container_width=True):
            text = "Tôi thấy sản phẩm này <mask> tuyệt vời"
        if st.button("Ví dụ 4", use_container_width=True):
            text = "Giao hàng <mask> nhanh"

    run = st.button("Chạy fill-mask", type="primary")
    if run:
        if "<mask>" not in text:
            st.warning("Vui lòng chèn token <mask> vào câu.")
        else:
            with st.spinner("Đang suy luận..."):
                mask_filler = load_fill_mask()
                outputs = mask_filler(text, top_k=top_k)
            st.markdown("#### Kết quả")
            if isinstance(outputs, dict):
                outputs = [outputs]
            for i, cand in enumerate(outputs, 1):
                token_str = cand.get("token_str")
                score = float(cand.get("score", 0.0))
                st.write(f"{i:2d}) {token_str}  —  score: {score:.4f}")

else:
    st.markdown("#### 💬 Sentiment Analysis")
    text = st.text_area("Nhập câu/đoạn tiếng Việt:", height=120, placeholder="Ví dụ: Sản phẩm rất tốt và chất lượng.")

    sample_pos = "Hàng giao nhanh và đóng gói cẩn thận."
    sample_neg = "Trải nghiệm quá tệ, không bao giờ quay lại."
    colp, coln = st.columns(2)
    with colp:
        if st.button("Chèn ví dụ tích cực", use_container_width=True):
            text = sample_pos
    with coln:
        if st.button("Chèn ví dụ tiêu cực", use_container_width=True):
            text = sample_neg

    run = st.button("Phân tích cảm xúc", type="primary")
    if run:
        if not text.strip():
            st.warning("Vui lòng nhập văn bản.")
        else:
            with st.spinner("Đang phân tích..."):
                classifier = load_sentiment()
                result = classifier(text)[0]
                label = str(result.get("label", "")).upper()
                score = float(result.get("score", 0.0)) * 100.0
            if label in {"POSITIVE", "POS", "+"}:
                st.success(f"✅ Sentiment: {label} (Confidence: {score:.2f}%)")
                st.balloons()
            else:
                st.error(f"❌ Sentiment: {label} (Confidence: {score:.2f}%)")


