document.addEventListener("DOMContentLoaded", function() {
    const reveals = document.querySelectorAll(".reveal");

    function revealOnScroll() {
        reveals.forEach((element, index) => {
            let windowHeight = window.innerHeight;
            let elementTop = element.getBoundingClientRect().top;
            let elementVisible = 100;

            if (elementTop < windowHeight - elementVisible) {
                element.style.transitionDelay = `${index * 0.1}s`;
                element.classList.add("active");
            }
        });
    }

    window.addEventListener("scroll", revealOnScroll);

    revealOnScroll();
});