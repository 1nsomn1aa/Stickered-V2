var modal = document.getElementById("newsletter-popup");
var span = document.getElementsByClassName("close-btn")[0];

setTimeout(function() {
    modal.style.display = "block";
}, 3000);

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

document.getElementById('newsletter-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var email = document.getElementById('email').value;

    fetch('/newsletter/signup/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ email: email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Thank you for subscribing!');
            modal.style.display = "none";
        } else {
            alert('Something went wrong. Please try again.');
        }
    })
    .catch(error => {
        alert('There was an error. Please try again.');
    });
});
