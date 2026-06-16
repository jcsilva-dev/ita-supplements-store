
    const deleteBtn = document.querySelector('.confirm-btn');
    deleteBtn.addEventListener('click', function() {
        this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Excluindo...';
        this.style.opacity = "0.8";
        this.style.pointerEvents = "none";
    });
