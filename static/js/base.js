document.addEventListener("DOMContentLoaded", () => {



    const menuButton = document.querySelector(".menu-toggle");
    const nav = document.querySelector(".nav");
    const actions = document.querySelector(".header-actions");

    if (!menuButton || !nav || !actions) {
    return;
    }

    menuButton.addEventListener("click", () => {
        nav.classList.toggle("active");
        actions.classList.toggle("active");
    });

});



