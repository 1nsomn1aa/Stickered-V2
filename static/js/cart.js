document.querySelectorAll('.quantity-btn').forEach(button => {
    button.addEventListener('click', function() {
        const input = this.parentElement.querySelector('input[name="quantity"]');
        let value = parseInt(input.value);
        if (this.dataset.action === "decrease" && value > 1) {
            value--;
        }
        if (this.dataset.action === "increase") {
            value++;
        }
        input.value = value;
        this.closest('form').submit();
    });
});