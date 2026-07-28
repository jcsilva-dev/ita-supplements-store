/**
 * base.js
 * Responsabilidade única: controlar abertura/fechamento do menu mobile (offcanvas).
 * Sem dependências externas.
 *
 * Nota sobre a revisão: o lado por onde o painel abre (esquerda/direita) é
 * decidido inteiramente pelo CSS (.nav / --shadow-menu), não por este
 * arquivo — por isso o bug do painel abrindo do lado oposto ao botão foi
 * corrigido só no CSS. Este JS não precisou de nenhuma lógica nova.
 */

(function () {
  "use strict";

  const menuToggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav");
   
  // Se o header não tiver esses elementos nesta página, não faz nada.
  if (!menuToggle || !nav) return;

  const menuIcon = menuToggle.querySelector("i");
  const ICON_OPEN = "fa-bars";
  const ICON_CLOSE = "fa-xmark";

  // Overlay é criado dinamicamente (não é necessário alterar o HTML/Django).
  const overlay = document.createElement("div");
  overlay.className = "nav-overlay";
  overlay.setAttribute("aria-hidden", "true");
  document.body.appendChild(overlay);

  let isOpen = false;

  function openMenu() {
    isOpen = true;
    nav.classList.add("is-open");
    menuToggle.setAttribute("aria-expanded", "true");
    menuToggle.setAttribute("aria-label", "Fechar menu de navegação");

    if (menuIcon) {
      menuIcon.classList.remove(ICON_OPEN);
      menuIcon.classList.add(ICON_CLOSE);
    }

    // A visibilidade do overlay é 100% controlada pelo CSS via
    // "body.menu-open .nav-overlay" (ver header.css, §8). Não existe uma
    // classe ".is-visible" no CSS, então adicioná-la aqui era código morto
    // — removido nesta revisão, sem nenhuma mudança de comportamento.
    document.body.classList.add("menu-open"); // scroll lock + overlay
    document.addEventListener("keydown", handleEscape);
  }

  function closeMenu() {
    isOpen = false;
    nav.classList.remove("is-open");
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Abrir menu de navegação");

    if (menuIcon) {
      menuIcon.classList.remove(ICON_CLOSE);
      menuIcon.classList.add(ICON_OPEN);
    }

    document.body.classList.remove("menu-open");
    document.removeEventListener("keydown", handleEscape);
  }

  function toggleMenu() {
    isOpen ? closeMenu() : openMenu();
  }

  function handleEscape(event) {
    if (event.key === "Escape") {
      closeMenu();
      menuToggle.focus();
    }
  }

  // Abrir/fechar ao clicar no botão
  menuToggle.addEventListener("click", toggleMenu);

  // Fechar ao clicar no overlay (fora do menu)
  document.addEventListener("click", function (event) {

    if (!isOpen) return;

    const clickedInsideMenu = nav.contains(event.target);
    const clickedToggle = menuToggle.contains(event.target);

    if (!clickedInsideMenu && !clickedToggle) {
        closeMenu();
    }

  });

  // Fechar ao clicar em qualquer link dentro do menu
  nav.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", closeMenu);
  });
  // Se a tela crescer para o breakpoint desktop, garante estado limpo
  const desktopQuery = window.matchMedia("(min-width: 768px)");
  desktopQuery.addEventListener("change", function (event) {
    if (event.matches && isOpen) {
      closeMenu();
    }
  });
})();


