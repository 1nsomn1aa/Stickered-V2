document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.querySelector('.mobile-navbar');
    const mobileNav = document.getElementById('mobileNav');

    mobileNav.addEventListener('show.bs.collapse', () => {
        navbar.classList.add('nav-open');
    });

    mobileNav.addEventListener('hide.bs.collapse', () => {
        setTimeout(() => {
            navbar.classList.remove('nav-open');
        }, 350);
    });
});