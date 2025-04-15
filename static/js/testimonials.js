let currentIndex = 0;
const testimonialsPerPage = window.innerWidth < 768 ? 1 : 3;

function showTestimonials(index) {
    const testimonials = document.querySelectorAll('.testimonial-card');
    testimonials.forEach((testimonial, i) => {
        testimonial.style.display = 'none';
        testimonial.classList.remove('show');
    });

    for (let i = index; i < index + testimonialsPerPage; i++) {
        const testimonial = testimonials[i];
        if (testimonial) {
            testimonial.style.display = 'block';
            setTimeout(() => testimonial.classList.add('show'), (i - index) * 100);
        }
    }
}

document.querySelector('.next-btn').addEventListener('click', function () {
    const testimonials = document.querySelectorAll('.testimonial-card');
    if (currentIndex + testimonialsPerPage < testimonials.length) {
        currentIndex += testimonialsPerPage;
        showTestimonials(currentIndex);
    }
});

document.querySelector('.prev-btn').addEventListener('click', function () {
    if (currentIndex - testimonialsPerPage >= 0) {
        currentIndex -= testimonialsPerPage;
        showTestimonials(currentIndex);
    }
});

window.addEventListener('resize', () => {
    location.reload();
});

showTestimonials(currentIndex);
