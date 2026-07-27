(function () {
  'use strict';

  /* ── Scroll Reveal ── */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  }, { threshold: 0.06, rootMargin: '0px 0px -24px 0px' });
  document.querySelectorAll('.reveal').forEach(function (el, i) {
    if (!el.style.transitionDelay) el.style.transitionDelay = (Math.min(i, 6) * 0.07) + 's';
    io.observe(el);
  });

  /* ── Gallery ── */
  (function () {
    var slides  = Array.from(document.querySelectorAll('.gallery__slide'));
    var thumbs  = Array.from(document.querySelectorAll('.gallery__thumb'));
    var counter = document.getElementById('js-counter');
    if (!slides.length) return;

    var cur = 0;

    function go(n) {
      slides[cur].classList.remove('is-active');
      thumbs[cur] && thumbs[cur].classList.remove('is-active');
      cur = (n + slides.length) % slides.length;
      slides[cur].classList.add('is-active');
      thumbs[cur] && thumbs[cur].classList.add('is-active');
      if (counter) counter.textContent = (cur + 1) + ' / ' + slides.length;
    }

    document.getElementById('js-prev')
      && document.getElementById('js-prev').addEventListener('click', function () { go(cur - 1); });
    document.getElementById('js-next')
      && document.getElementById('js-next').addEventListener('click', function () { go(cur + 1); });

    thumbs.forEach(function (t) {
      t.addEventListener('click', function () { go(parseInt(t.dataset.thumb, 10)); });
    });

    /* touch swipe */
    var sx = 0;
    var stage = document.getElementById('js-stage');
    if (stage) {
      stage.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
      stage.addEventListener('touchend',   function (e) {
        var dx = e.changedTouches[0].clientX - sx;
        if (Math.abs(dx) > 40) go(dx < 0 ? cur + 1 : cur - 1);
      }, { passive: true });
    }
  }());

  /* ── Variant Selector & Purchase Summary ──
     Fonte única de verdade para tudo o que depende da variante
     selecionada, da quantidade e do parcelamento escolhidos:
     preço, chips, alerta de estoque, subtotal e parcela.
     Sempre lê a variante atualmente marcada (nunca a primeira
     carregada) e deve ser chamada sempre que variante, quantidade
     ou parcelamento mudarem. */
  (function () {
    var grid = document.getElementById('js-variant-grid');
    if (!grid) return;

    function toNumber(value) {
      return parseFloat(value.replace(",", "."));
    }

    window.updatePurchaseSummary = function () {
      var selected = document.querySelector('.variant-card__input:checked');
      if (!selected) return;

      var finalPrice    = toNumber(selected.dataset.discountPrice);
      var originalPrice = toNumber(selected.dataset.originalPrice);
      var percentage    = selected.dataset.percent;

      /* preço principal */
      var priceEl = document.getElementById('js-price');
      if (priceEl) {
        priceEl.textContent = finalPrice.toLocaleString('pt-BR', {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2
        });
      }

      var priceOld = document.getElementById('js-price-old');
      if (priceOld) {
        priceOld.textContent = originalPrice.toLocaleString('pt-BR', {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2
        });
      }

      var discount = document.getElementById('js-discount');
      if (discount) {
        discount.textContent = percentage + '% OFF';
      }

      /* variante escondida (form) */
      var hidden = document.getElementById('js-variant-hidden');
      if (hidden) hidden.value = selected.value;

      /* chips */
      var brandEl = document.getElementById('js-brand');
      if (brandEl) brandEl.textContent = selected.dataset.brand || '—';

      var stockEl = document.getElementById('js-stock');
      if (stockEl) stockEl.textContent = selected.dataset.stock;

      var flavorChip = document.getElementById('js-flavor-chip');
      var sizeChip   = document.getElementById('js-size-chip');

      if (selected.dataset.flavor) {
        var flavorEl = document.getElementById('js-flavor');
        if (flavorEl) flavorEl.textContent = selected.dataset.flavor;
        if (flavorChip) flavorChip.classList.remove('hidden-chip');
      } else if (flavorChip) {
        flavorChip.classList.add('hidden-chip');
      }

      if (selected.dataset.size) {
        var sizeEl = document.getElementById('js-size');
        if (sizeEl) sizeEl.textContent = selected.dataset.size;
        if (sizeChip) sizeChip.classList.remove('hidden-chip');
      } else if (sizeChip) {
        sizeChip.classList.add('hidden-chip');
      }

      /* alerta de estoque */
      var stock = parseInt(selected.dataset.stock, 10);

      var box = document.getElementById("js-stock-alert");

      if (box) {

          if (stock <= 0) {

              box.innerHTML = `
                  <div class="stock-alert stock-alert--out">
                      <span class="stock-alert__icon"></span>

                      <div>
                          <strong>Produto indisponível</strong><br>
                          Esta opção está sem estoque no momento.
                      </div>
                  </div>
              `;

          }

          else if (stock <= 3) {

              box.innerHTML = `
                  <div class="stock-alert stock-alert--low">
                      <span class="stock-alert__icon"></span>

                      <div>
                          <strong>Últimas ${stock} unidades</strong><br>
                          Estoque limitado para esta opção.
                      </div>

                      <div class="stock-bar">
                          <div class="stock-bar__fill stock-bar__fill--low"></div>
                      </div>
                  </div>
              `;

          }

          else if (stock <= 10) {

              box.innerHTML = `
                  <div class="stock-alert stock-alert--medium">
                      <span class="stock-alert__icon"></span>

                      <div>
                          Restam apenas <strong>${stock}</strong> unidades em estoque.
                      </div>

                      <div class="stock-bar">
                          <div class="stock-bar__fill stock-bar__fill--medium"></div>
                      </div>
                  </div>
              `;

          }

          else {

              box.innerHTML = "";

          }

      }

      /* subtotal = preço da variante selecionada × quantidade */
      var qtyInput = document.getElementById('js-qty');
      var qty = parseInt((qtyInput && qtyInput.value) || 1, 10);
      var subtotal = finalPrice * qty;

      var subtotalElement = document.getElementById('js-subtotal');
      if (subtotalElement) {
        subtotalElement.textContent = subtotal.toLocaleString('pt-BR', {
          style: 'currency',
          currency: 'BRL'
        });
      }

      /* parcelamento: usa a opção atualmente selecionada no dropdown */
      var trigger = document.getElementById('js-installments-trigger-label');
      var option  = document.querySelector('.installments-option[aria-selected="true"]');

      if (trigger && option) {
        var parcelas = parseInt(option.dataset.value, 10);
        var valorParcela = subtotal / parcelas;

        trigger.textContent =
          parcelas +
          'x de R$ ' +
          valorParcela.toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          });
      }
    };

    /* delegação de evento no grid: qualquer troca de variante
       passa pelo único ponto de atualização */
    grid.addEventListener('change', function (e) {
      if (e.target && e.target.classList.contains('variant-card__input')) {
        window.updatePurchaseSummary();
      }
    });
  }());

  /* ── Toggle Reviews ── */
  (function () {
    var btn    = document.getElementById('js-toggle-fb');
    var items  = document.querySelectorAll('.js-fb-item.is-hidden');
    var hidden = Array.from(items);
    var open   = false;
    if (!btn || !hidden.length) return;

    btn.addEventListener('click', function () {
      open = !open;
      hidden.forEach(function (el) { el.classList.toggle('is-hidden', !open); });
      btn.innerHTML = open
  ? '− Ver menos'
  : '+ Ver mais';
    });
  }());

  /* ── Lightbox ── */
  (function () {
    var box   = document.getElementById('js-lightbox');
    var img   = document.getElementById('js-lb-img');
    var close = document.getElementById('js-lb-close');
    var prev  = document.getElementById('js-lb-prev');
    var next  = document.getElementById('js-lb-next');
    if (!box) return;

    var imgs = [], cur = 0;

    function open(list, idx) {
      imgs = list; cur = idx;
      img.src = imgs[cur];
      box.classList.add('is-open');
      document.body.style.overflow = 'hidden';
    }
    function close_() {
      box.classList.remove('is-open');
      document.body.style.overflow = '';
    }
    function step(d) {
      cur = (cur + d + imgs.length) % imgs.length;
      img.src = imgs[cur];
    }

    document.querySelectorAll('.js-lb-trigger').forEach(function (el) {
      el.addEventListener('click', function () {
        open(JSON.parse(el.dataset.images), parseInt(el.dataset.index, 10));
      });
    });

    close && close.addEventListener('click', close_);
    prev  && prev.addEventListener('click', function () { step(-1); });
    next  && next.addEventListener('click', function () { step(1); });
    box.addEventListener('click', function (e) { if (e.target === box) close_(); });
    document.addEventListener('keydown', function (e) {
      if (!box.classList.contains('is-open')) return;
      if (e.key === 'Escape') close_();
      if (e.key === 'ArrowLeft')  step(-1);
      if (e.key === 'ArrowRight') step(1);
    });
  }());

}());



(function () {
  var select = document.getElementById('js-installments-select');
  if (!select) return;

  var trigger      = document.getElementById('js-installments-trigger');
  var triggerLabel = document.getElementById('js-installments-trigger-label');
  var list         = document.getElementById('js-installments-list');
  var hiddenInput  = document.getElementById('js-installments-value');
  var activeIndex  = -1;

  function formatBRL(value) {
    return value.toLocaleString("pt-BR", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  }

  function optionLabel(item) {
    return item.times + 'x de R$ ' + formatBRL(item.value);
  }

  function getOptions() {
    return Array.prototype.slice.call(list.querySelectorAll('.installments-option'));
  }

  function closeList() {
    list.hidden = true;
    trigger.setAttribute('aria-expanded', 'false');
    trigger.removeAttribute('aria-activedescendant');
    activeIndex = -1;
  }

  function openList() {
    var options = getOptions();
    if (!options.length) return;
    list.hidden = false;
    trigger.setAttribute('aria-expanded', 'true');
    var selected = options.findIndex(function (o) {
      return o.getAttribute('aria-selected') === 'true';
    });
    setActive(selected >= 0 ? selected : 0);
  }

  function setActive(index) {
    var options = getOptions();
    if (!options.length) return;
    activeIndex = (index + options.length) % options.length;
    options.forEach(function (o, i) {
      o.classList.toggle('installments-option--active', i === activeIndex);
    });
    trigger.setAttribute('aria-activedescendant', options[activeIndex].id);
    options[activeIndex].scrollIntoView({ block: 'nearest' });
  }

  function selectOption(option) {
    getOptions().forEach(function (o) {
      o.setAttribute('aria-selected', 'false');
    });
    option.setAttribute('aria-selected', 'true');
    triggerLabel.textContent = option.textContent.trim();
    hiddenInput.value = option.dataset.value;
    window.updatePurchaseSummary();
    closeList();
    trigger.focus();
  }

  /* abrir/fechar via clique no trigger */
  trigger.addEventListener('click', function () {
    if (list.hidden) {
      openList();
    } else {
      closeList();
    }
  });

  /* clique em uma opção */
  list.addEventListener('click', function (e) {
    var option = e.target.closest('.installments-option');
    if (option) selectOption(option);
  });

  /* teclado no trigger */
  trigger.addEventListener('keydown', function (e) {
    if (['ArrowDown', 'ArrowUp', 'Enter', ' '].indexOf(e.key) !== -1) {
      e.preventDefault();
      if (list.hidden) {
        openList();
      } else if (e.key === 'Enter' || e.key === ' ') {
        var options = getOptions();
        if (activeIndex >= 0) selectOption(options[activeIndex]);
      } else if (e.key === 'ArrowDown') {
        setActive(activeIndex + 1);
      } else if (e.key === 'ArrowUp') {
        setActive(activeIndex - 1);
      }
    } else if (e.key === 'Escape' && !list.hidden) {
      closeList();
    }
  });

  /* teclado dentro da lista (foco permanece no trigger, navegação por aria-activedescendant) */
  document.addEventListener('keydown', function (e) {
    if (list.hidden || document.activeElement !== trigger) return;
    if (e.key === 'Home') {
      e.preventDefault();
      setActive(0);
    } else if (e.key === 'End') {
      e.preventDefault();
      setActive(getOptions().length - 1);
    }
  });

  /* clique fora fecha a lista */
  document.addEventListener('click', function (e) {
    if (!select.contains(e.target)) closeList();
  });

  /* ── integração com a troca de variante ── */
  /* substitui a antiga manipulação do <select id="js-installments">;
     mesma fonte de dados (data-installments), mesmo ponto de disparo.
     Reconstrói as opções disponíveis; o valor final exibido no trigger
     é recalculado logo em seguida por window.updatePurchaseSummary()
     (disparado pelo módulo de Quantidade ao resetar a quantidade). */
  window.updateInstallmentsFromVariant = function (input) {
    var installments = JSON.parse(input.dataset.installments || '[]');

    list.innerHTML = '';
    installments.forEach(function (item, index) {
      var li = document.createElement('li');
      li.setAttribute('role', 'option');
      li.className = 'installments-option';
      li.id = 'installment-opt-' + index;
      li.dataset.value = item.times;
      li.setAttribute('aria-selected', index === 0 ? 'true' : 'false');
      li.textContent = optionLabel(item);
      list.appendChild(li);
    });

    if (installments.length) {
      triggerLabel.textContent = optionLabel(installments[0]);
      hiddenInput.value = installments[0].times;
    } else {
      triggerLabel.textContent = '';
      hiddenInput.value = '';
    }

    closeList();
  };

  /* liga ao mesmo evento de troca de variante já existente no grid */
  var grid = document.getElementById('js-variant-grid');
  if (grid) {
    grid.addEventListener('change', function (e) {
      if (e.target && e.target.classList.contains('variant-card__input')) {
        window.updateInstallmentsFromVariant(e.target);
      }
    });
  }
}());


/* ── Quantity ── */
(function () {
  var qty     = document.getElementById("js-qty");
  var minus   = document.getElementById("js-qty-minus");
  var plus    = document.getElementById("js-qty-plus");
  var message = document.getElementById("js-qty-message");
  var grid    = document.getElementById("js-variant-grid");

  if (!qty || !minus || !plus) return;

  /* estoque da variante atualmente selecionada */
  function getMaxStock() {
    var selected = document.querySelector(".variant-card__input:checked");
    if (!selected) return 999;
    return parseInt(selected.dataset.stock || "999", 10);
  }

  function showMessage(text) {
    if (message) message.textContent = text;
  }

  function clearMessage() {
    showMessage("");
  }

  /* estado dos botões: apenas o "-" pode ser desabilitado */
  function updateButtons() {
    var value = parseInt(qty.value || 1, 10);
    minus.disabled = value <= 1;
  }

  /* ponto único de entrada para qualquer alteração de quantidade */
  function setQuantity(value) {
    var max = getMaxStock();

    if (isNaN(value) || value < 1) {
      value = 1;
    }

    if (value > max) {
      value = max;
      showMessage(
        "Quantidade máxima disponível: " + max + " unidade" + (max > 1 ? "s." : ".")
      );
    } else {
      clearMessage();
    }

    qty.value = value;
    window.updatePurchaseSummary();
    updateButtons();
  }

  minus.addEventListener("click", function () {
    setQuantity(parseInt(qty.value || 1, 10) - 1);
  });

  plus.addEventListener("click", function () {

    var value = parseInt(qty.value || 1, 10);
    var max = getMaxStock();

    if (value >= max) {
        showMessage(
            "Quantidade máxima disponível: " + max + " unidade" + (max > 1 ? "s." : ".")
        );
        return;
    }

    setQuantity(value + 1);

  });

  qty.addEventListener("change", function () {
    setQuantity(parseInt(qty.value, 10));
  });

  /* troca de variante: recalcula estoque, reseta para 1, limpa mensagem */
  if (grid) {
    grid.addEventListener("change", function () {

        clearMessage();
        setQuantity(1);

    });
  }

  updateButtons();
  window.updatePurchaseSummary();
}());