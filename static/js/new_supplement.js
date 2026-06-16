
    document.querySelectorAll('.image-form-card input[type="file"]').forEach(input => {

        input.addEventListener('change', function() {

            const card = this.closest('.image-form-card');
            const preview = card.querySelector('.image-preview');
            const img = card.querySelector('img');
            const file = this.files[0];

            if (file) {

                const reader = new FileReader();

                reader.onload = e => {

                    img.src = e.target.result;

                    preview.style.display = 'block';

                    card.style.borderStyle = 'solid';
                    card.style.borderColor = 'var(--accent-color)';

                }

                reader.readAsDataURL(file);

            }

        });

    });
