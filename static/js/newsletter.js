document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('newsletter-form');
    const emailInput = document.getElementById('email');
    const popup = document.getElementById('newsletter-popup');
    const closeBtn = document.querySelector('.close-btn');

    if (!localStorage.getItem('subscribedToNewsletter')) {
        setTimeout(function () {
            popup.classList.add('show');
        }, 2000);
    }

    closeBtn.addEventListener('click', function () {
        popup.classList.remove('show');
    });

    window.onclick = function (event) {
        if (event.target === popup) {
            popup.classList.remove('show');
        }
    };

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const email = emailInput.value;

        fetch(newsletterSignupUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ email: email })
        })
        .then(response => response.json())
        .then(responseData => {
            if (responseData.success) {
                localStorage.setItem('subscribedToNewsletter', 'true');
                popup.classList.remove('show');

                setTimeout(() => {
                    window.location.href = '/?subscribed=1';
                }, 500);
            } else {
                alert(responseData.message || 'Something went wrong, please try again!');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Something went wrong, please try again!');
        });
    });
});
