import streamlit as st
from multilingual import load_multilingual_pipeline, analyze_text


st.set_page_config(
    page_title="Multilingual Sentiment (5-class)",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def load_model():
    return load_multilingual_pipeline()


st.markdown(
    """
<div style="text-align:center; padding: 1.25rem 0;">
  <h1>🌍 Multilingual Sentiment (5-class)</h1>
  <p style="font-size: 1.1rem; margin: 0;">Model: <code>tabularisai/multilingual-sentiment-analysis</code></p>
  <p style="margin: .25rem 0 0 0; font-size: .95rem;">Very Negative / Negative / Neutral / Positive / Very Positive</p>
</div>
""",
    unsafe_allow_html=True,
)


with st.sidebar:
    st.markdown("### Hướng dẫn")
    st.markdown("Nhập câu ở bất kỳ ngôn ngữ nào trong 23 languages (có Tiếng Việt)")
    st.markdown("—")
    show_all = st.checkbox("Hiển thị toàn bộ điểm 5 lớp", value=True)


st.divider()


text = st.text_area(
    "Nhập câu/đoạn văn (đa ngôn ngữ):",
    height=140,
    placeholder="Ví dụ: Tôi rất thích sản phẩm này! / I don't like this service. / 这家餐厅很好吃！",
)

col1, col2 = st.columns(2)
with col1:
    if st.button("Ví dụ Tiếng Việt (tích cực)", use_container_width=True):
        text = "Sản phẩm rất tốt và chất lượng. Tôi sẽ giới thiệu cho bạn bè."
with col2:
    if st.button("Ví dụ English (tiêu cực)", use_container_width=True):
        text = "The customer service was disappointing and very slow."


run = st.button("Phân tích", type="primary")
if run:
    if not text.strip():
        st.warning("Vui lòng nhập văn bản.")
    else:
        with st.spinner("Đang phân tích..."):
            clf = load_model()
            result = analyze_text(clf, text)
        label = result["label"]
        score = result["score"] * 100.0
        if label in {"POSITIVE", "VERY POSITIVE"}:
            st.success(f"✅ Sentiment: {label} (Confidence: {score:.2f}%)")
        elif label in {"NEGATIVE", "VERY NEGATIVE"}:
            st.error(f"❌ Sentiment: {label} (Confidence: {score:.2f}%)")
        else:
            st.info(f"ℹ️ Sentiment: {label} (Confidence: {score:.2f}%)")

        if show_all:
            st.markdown("#### Chi tiết 5 lớp")
            cols = st.columns(5)
            for i, item in enumerate(result["all_scores"]):
                with cols[i]:
                    st.metric(item["label"].title(), f"{item['score']*100:.2f}%")


