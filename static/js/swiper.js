const swiper = new Swiper('.mySwiper', {
    loop: true,
    spaceBetween: 20,
    slidesPerView: 1,
    autoplay: {
        delay: 4500,
        pauseOnMouseEnter: true,
    },
    breakpoints: {
        640: {
            slidesPerView: 1,
            spaceBetween: 10,
        },
        768: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        1024: {
            slidesPerView: 3,
            spaceBetween: 30,
        },
    },
});