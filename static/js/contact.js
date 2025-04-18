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

    function updateOpenStatus() {
        const statusText = document.getElementById("current-status-text");
        const now = new Date();
        const options = { timeZone: 'Europe/Dublin' };
        const irelandTime = new Date(now.toLocaleString('en-US', options));
        const day = irelandTime.getDay();
        const hour = irelandTime.getHours();

        let isOpen = false;

        if (day >= 1 && day <= 5) {
            if (hour >= 9 && hour < 18) {
                isOpen = true;
            }
        } else if (day === 6) {
            if (hour >= 10 && hour < 16) {
                isOpen = true;
            }
        }

        if (isOpen) {
            statusText.textContent = "OPEN";
            statusText.classList.remove("text-danger");
            statusText.classList.add("text-success");
        } else {
            statusText.textContent = "CLOSED";
            statusText.classList.remove("text-success");
            statusText.classList.add("text-danger");
        }
    }

    updateOpenStatus();

    setInterval(updateOpenStatus, 60000);
});