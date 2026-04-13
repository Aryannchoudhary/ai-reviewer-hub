// Review Interactive JS
document.addEventListener('DOMContentLoaded', function() {
    // Syntax highlight after load
    Prism.highlightAll();

    // Accordion functionality
    const accordions = document.querySelectorAll('.accordion');
    accordions.forEach(acc => {
        acc.querySelector('h2').addEventListener('click', function() {
            const content = this.parentElement.querySelector('.accordion-content');
            const icon = this.querySelector('.toggle-icon');
            content.style.display = content.style.display === 'block' ? 'none' : 'block';
            icon.textContent = content.style.display === 'block' ? '-' : '+';
        });
    });

    // Auto-hide optimized if empty
    if (!document.querySelector('.optimized-code code').textContent.trim()) {
        document.querySelector('.accordion').style.display = 'none';
    }
});

// Copy to clipboard
function copyCode(type) {
    let code;
    if (type === 'original') {
        code = document.querySelector('.original-code pre code').textContent;
    } else {
        code = document.querySelector('.optimized-code pre code')?.textContent || '';
    }
    navigator.clipboard.writeText(code).then(() => {
        showToast('Copied to clipboard!');
    });
}

// Accept suggestion (replace code and save)
function acceptSuggestion(reviewId) {
    const optimizedCode = document.querySelector('.optimized-code pre code').textContent;
    if (confirm('Accept this optimized code? It will update your review.')) {
        fetch(`/accept-suggestion/${reviewId}/`, {
            method: 'POST',
            headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value},
            body: JSON.stringify({optimized_code: optimizedCode})
        }).then(() => {
            document.querySelector('.original-code pre code').textContent = optimizedCode;
            Prism.highlightElement(document.querySelector('.original-code pre code'));
            showToast('Suggestion accepted!');
        });
    }
}




// Toast notification
function showToast(message) {
    const toast = document.createElement('div');
    toast.style.cssText = 'position:fixed;top:20px;right:20px;background:#10b981;color:white;padding:12px 20px;border-radius:8px;z-index:10000;';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// Issue highlighting in code (simple line numbers simulation)
function highlightIssues() {
    // Could parse errors for line numbers and highlight
    console.log('Issue highlighting ready');
}
highlightIssues();
