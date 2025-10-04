// Main JavaScript for Sentiment Analysis Web App
// Giao diện tương tác phân tích cảm xúc

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const textInput = document.getElementById('textInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const clearBtn = document.getElementById('clearBtn');
    const resultsSection = document.getElementById('resultsSection');
    const resultCard = document.getElementById('resultCard');
    const examplesList = document.getElementById('examplesList');
    const loadingOverlay = document.getElementById('loadingOverlay');

    // Initialize app
    init();

    function init() {
        loadExamples();
        bindEvents();
    }

    function bindEvents() {
        // Analyze button click
        analyzeBtn.addEventListener('click', analyzeText);
        
        // Clear button click
        clearBtn.addEventListener('click', clearInput);
        
        // Enter key in textarea (Ctrl+Enter to submit)
        textInput.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                analyzeText();
            }
        });
        
        // Auto-resize textarea
        textInput.addEventListener('input', autoResizeTextarea);
    }

    function loadExamples() {
        fetch('/examples')
            .then(response => response.json())
            .then(data => {
                displayExamples(data.examples);
            })
            .catch(error => {
                console.error('Lỗi khi tải ví dụ:', error);
            });
    }

    function displayExamples(examples) {
        examplesList.innerHTML = '';
        
        examples.forEach((example, index) => {
            const exampleBtn = document.createElement('button');
            exampleBtn.className = 'btn btn-example';
            exampleBtn.textContent = example;
            exampleBtn.title = 'Nhấp để sử dụng ví dụ này';
            
            exampleBtn.addEventListener('click', function() {
                textInput.value = example;
                autoResizeTextarea();
                textInput.focus();
            });
            
            examplesList.appendChild(exampleBtn);
        });
    }

    async function analyzeText() {
        const text = textInput.value.trim();
        
        if (!text) {
            showError('Vui lòng nhập văn bản cần phân tích');
            return;
        }

        showLoading(true);
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();
            
            if (data.success) {
                displayResult(data);
            } else {
                showError(data.error || 'Có lỗi xảy ra khi phân tích');
            }
        } catch (error) {
            console.error('Lỗi:', error);
            showError('Lỗi kết nối. Vui lòng thử lại.');
        } finally {
            showLoading(false);
        }
    }

    function displayResult(data) {
        const { text, sentiment, sentiment_emoji, color_class, confidence_percent } = data;
        
        resultCard.innerHTML = `
            <div class="result-content">
                <div class="sentiment-display">
                    <span class="sentiment-emoji">${sentiment_emoji}</span>
                    <span class="sentiment-text">${sentiment}</span>
                </div>
                <div class="confidence-display">
                    <div class="confidence-label">Độ tin cậy</div>
                    <div class="confidence-bar">
                        <div class="confidence-fill ${color_class}" style="width: ${confidence_percent}%"></div>
                    </div>
                    <div class="confidence-percent">${confidence_percent}%</div>
                </div>
            </div>
            <div class="analyzed-text">
                "${text}"
            </div>
        `;
        
        resultCard.className = `result-card ${color_class}`;
        resultsSection.style.display = 'block';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
        // Add success animation
        resultCard.style.animation = 'none';
        setTimeout(() => {
            resultCard.style.animation = 'fadeIn 0.5s ease';
        }, 10);
    }

    function showError(message) {
        // Create error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-notification';
        errorDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i>
            <span>${message}</span>
        `;
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #e74c3c;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
            z-index: 1001;
            display: flex;
            align-items: center;
            gap: 10px;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(errorDiv);
        
        // Remove after 4 seconds
        setTimeout(() => {
            errorDiv.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(errorDiv);
            }, 300);
        }, 4000);
    }

    function clearInput() {
        textInput.value = '';
        resultsSection.style.display = 'none';
        textInput.style.height = 'auto';
        textInput.focus();
    }

    function autoResizeTextarea() {
        textInput.style.height = 'auto';
        textInput.style.height = Math.min(textInput.scrollHeight, 200) + 'px';
    }

    function showLoading(show) {
        if (show) {
            loadingOverlay.classList.add('show');
        } else {
            loadingOverlay.classList.remove('show');
        }
    }

    // Add CSS animations for notifications
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
        
        .error-notification {
            font-family: 'Inter', sans-serif;
            font-weight: 500;
        }
    `;
    document.head.appendChild(style);

    // Add keyboard shortcuts info
    const shortcutsInfo = document.createElement('div');
    shortcutsInfo.innerHTML = `
        <small style="color: #7f8c8d; font-size: 0.85rem;">
            <i class="fas fa-keyboard"></i> 
            Mẹo: Sử dụng Ctrl+Enter để phân tích nhanh
        </small>
    `;
    shortcutsInfo.style.marginTop = '10px';
    shortcutsInfo.style.display = 'flex';
    shortcutsInfo.style.alignItems = 'center';
    shortcutsInfo.style.gap = '5px';
    
    const inputGroup = document.querySelector('.input-group');
    inputGroup.appendChild(shortcutsInfo);
});
