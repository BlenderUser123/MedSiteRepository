document.addEventListener('DOMContentLoaded', function() {
    // Форма записи
    const form = document.getElementById('appointment-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            
            fetch('/appointments', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const messageDiv = document.getElementById('form-message');
                if (data.success) {
                    messageDiv.className = 'form-message success';
                    messageDiv.textContent = '✅ ' + data.message;
                    form.reset();
                } else {
                    messageDiv.className = 'form-message error';
                    messageDiv.textContent = '❌ ' + data.message;
                }
            })
            .catch(error => {
                const messageDiv = document.getElementById('form-message');
                messageDiv.className = 'form-message error';
                messageDiv.textContent = '❌ Ошибка соединения. Попробуйте позже.';
            });
        });
    }

    // Установка минимальной даты в календаре (сегодня)
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
    }
});