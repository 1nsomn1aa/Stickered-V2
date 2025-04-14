document.querySelectorAll('.search-toggle').forEach(function (toggle) {
    toggle.addEventListener('click', function () {
        const input = this.closest('.search-wrapper').querySelector('.search-input');
        input.classList.toggle('expanded');
        if (input.classList.contains('expanded')) {
            input.focus();
        }
    });
});