(function () {
    'use strict';

    const revealObserver = new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                entry.target.classList.add('in');
                revealObserver.unobserve(entry.target);
            });
        },
        { threshold: 0.06, rootMargin: "0px 0px -20px 0px" }
    );

    document.querySelectorAll(".reveal").forEach(function (element, index) {
        if (!element.style.transitionDelay) {
            element.style.transitionDelay = (Math.min(index, 6) * 0.06) + "s";
        }
        revealObserver.observe(element);
    });

})();


/*
============================================================
PAYMENT DROPDOWN
============================================================
*/
(function () {
    const dropdown = document.querySelector("#payment-dropdown");
    if (!dropdown) return;

    const button = dropdown.querySelector(".payment-dropdown__button");
    const selected = dropdown.querySelector(".payment-dropdown__selected");
    const hiddenInput = dropdown.querySelector("#cart-installments");
    const options = dropdown.querySelectorAll(".payment-dropdown__option");

    function closeDropdown() {
        dropdown.classList.remove("open");
        button.setAttribute("aria-expanded", "false");
    }

    /* ABRIR / FECHAR */
    button.addEventListener("click", function (event) {
    event.stopPropagation();
    const isOpen = dropdown.classList.toggle("open");
    button.setAttribute("aria-expanded", isOpen);
    });

    /* ESCOLHER PARCELA */
    options.forEach(function (option) {
        option.addEventListener("click", function () {
            const value = this.dataset.value;
            const text = this.querySelector("span").textContent;
            
            console.log("Parcela selecionada:", value);
            selected.textContent = text;
            hiddenInput.value = value;

            options.forEach(function (item) {
                item.classList.remove("active");
                item.setAttribute("aria-selected", "false");
            });

            this.classList.add("active");
            this.setAttribute("aria-selected", "true");

            closeDropdown();
        });
    });

    /* FECHAR CLICANDO FORA */
    document.addEventListener("click", function (event) {
        if (!dropdown.contains(event.target)) {
            closeDropdown();
        }
    });

    /* MELHORIA: fechar com Esc — acessibilidade de teclado,
       não alterada a lógica de seleção/POST. */
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && dropdown.classList.contains("open")) {
            closeDropdown();
            button.focus();
        }
    });

})();