document.querySelectorAll('input[name="quantity"]').forEach((input) => {
    input.addEventListener('change', function () {
        this.form.submit();
    });
});

document.querySelectorAll('.remove-form').forEach((form) => {
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const itemRow = this.closest('.row, tr');
        itemRow.style.transition = "opacity 0.5s ease-out, height 0.5s ease-out";
        itemRow.style.opacity = 0;
        itemRow.style.height = 0;
        setTimeout(() => {
            this.submit();
        }, 400);
    });
});