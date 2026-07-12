// front end/script.js

const questionInput = document.getElementById('questionInput');
const askButton = document.getElementById('askButton');
const buttonText = document.getElementById('buttonText');
const resultDiv = document.getElementById('result');

// Enter key support
questionInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        askQuestion();
    }
});

// Focus on load
questionInput.focus();

async function askQuestion() {
    const question = questionInput.value.trim();

    if (!question) {
        resultDiv.innerHTML = `
            <div class="error">⚠️ يرجى كتابة سؤال قبل البحث</div>
        `;
        return;
    }

    // Show loading
    askButton.disabled = true;
    buttonText.innerHTML = '<span class="spinner"></span> جاري البحث...';
    resultDiv.innerHTML = `
        <div style="text-align:center; padding:40px 0; color:rgba(255,255,255,0.3);">
            <span style="font-size:2rem;">⏳</span>
            <p style="margin-top:10px;">جاري البحث عن إجابة...</p>
        </div>
    `;

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question })
        });

        const data = await response.json();

        if (response.ok) {
            let sourcesHtml = '';
            if (data.sources && data.sources.length > 0) {
                sourcesHtml = `
                    <div class="sources-section">
                        <div class="sources-label">📚 المصادر</div>
                        ${data.sources.map((src, index) => `
                            <div class="source-item">
                                <div class="source-id">مصدر ${index + 1}</div>
                                ${src.length > 300 ? src.substring(0, 300) + '...' : src}
                            </div>
                        `).join('')}
                    </div>
                `;
            }

            resultDiv.innerHTML = `
                <div class="answer-section">
                    <div class="question-label">❓ سؤالك</div>
                    <div class="question-text">${data.question}</div>
                    <div class="answer-text">${data.answer}</div>
                    ${sourcesHtml}
                </div>
            `;
        } else {
            resultDiv.innerHTML = `
                <div class="error">❌ ${data.error || 'حدث خطأ ما'}</div>
            `;
        }

    } catch (error) {
        resultDiv.innerHTML = `
            <div class="error">❌ خطأ في الاتصال: ${error.message}</div>
        `;
    } finally {
        askButton.disabled = false;
        buttonText.innerHTML = '🔍 اسأل';
    }
}

// Expose function globally
window.askQuestion = askQuestion;