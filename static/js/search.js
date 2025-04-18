document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.search-wrapper').forEach(function (wrapper) {
        const input = wrapper.querySelector('.search-input');
        const toggle = wrapper.querySelector('.search-toggle');
        const form = wrapper.closest('form');

        toggle.addEventListener('click', function (e) {
            if (!input.classList.contains('expanded')) {
                e.preventDefault();
                input.classList.add('expanded');
                input.focus();
            } else if (input.value.trim() === '') {
                e.preventDefault();
                input.focus();
            }
        });

        form.addEventListener('submit', function (e) {
            if (input.value.trim() === '') {
                e.preventDefault();
                input.classList.add('expanded');
                input.focus();
            }
        });
    });
});
