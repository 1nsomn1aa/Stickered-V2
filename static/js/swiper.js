document.addEventListener("DOMContentLoaded", function() {
    const swiper = new Swiper('.swiper-container', {
        loop: true, // Loop the slides
        autoplay: {
            delay: 3000, // 3 seconds per slide
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true, // Make the pagination dots clickable
        },
        effect: 'fade', // Fade transition between slides
    });
});