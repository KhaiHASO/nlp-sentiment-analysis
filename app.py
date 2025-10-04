"""
Flask Web Application for DistilBERT Sentiment Analysis
Giao diện web phân tích cảm xúc tiếng Việt
"""

from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import json

app = Flask(__name__)

# Load the sentiment analysis model
print("Đang tải mô hình DistilBERT...")
classifier = pipeline("sentiment-analysis", 
                     model="distilbert-base-uncased-finetuned-sst-2-english")
print("Mô hình đã được tải thành công!")

@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    """API phân tích cảm xúc"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Vui lòng nhập văn bản cần phân tích'
            })
        
        # Phân tích cảm xúc
        result = classifier(text)
        
        # Chuyển đổi kết quả sang tiếng Việt
        label = result[0]['label']
        score = result[0]['score']
        
        if label == 'LABEL_1':
            sentiment = 'Tích cực'
            sentiment_emoji = '😊'
            color_class = 'positive'
        else:
            sentiment = 'Tiêu cực'
            sentiment_emoji = '😔'
            color_class = 'negative'
        
        # Tính phần trăm tin cậy
        confidence_percent = round(score * 100, 1)
        
        return jsonify({
            'success': True,
            'text': text,
            'sentiment': sentiment,
            'sentiment_emoji': sentiment_emoji,
            'color_class': color_class,
            'confidence': score,
            'confidence_percent': confidence_percent
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi khi phân tích: {str(e)}'
        })

@app.route('/examples')
def examples():
    """Lấy danh sách ví dụ mẫu"""
    sample_texts = [
        "Tôi rất thích bộ phim này!",
        "Sản phẩm này thật tệ, tôi không hài lòng.",
        "Thời tiết hôm nay ổn.",
        "Tôi yêu gia đình của mình.",
        "Đây là trải nghiệm tệ nhất từ trước đến giờ.",
        "Dịch vụ rất tuyệt vời và chuyên nghiệp.",
        "Tôi không chắc cảm nhận của mình về điều này.",
        "Cuốn sách này đã thay đổi hoàn toàn cuộc đời tôi!",
        "Đồ ăn thật kinh khủng và lạnh ngắt.",
        "Màn trình diễn của các diễn viên thật xuất sắc!"
    ]
    
    return jsonify({
        'examples': sample_texts
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
