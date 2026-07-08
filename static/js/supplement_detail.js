
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

  /* ── Variant Selector ── */
  (function () {
    var sel = document.getElementById('js-variant-select');
    if (!sel) return;

      /* price */
    function toNumber(value) {
        return parseFloat(value.replace(",", "."));
    }

    sel.addEventListener('change', function () {

        var opt = this.options[this.selectedIndex];

        var finalPrice = toNumber(opt.dataset.discountPrice);
        var originalPrice = toNumber(opt.dataset.originalPrice);
        var percentage = opt.dataset.percent;

        document.getElementById("js-price").textContent =
            finalPrice.toLocaleString("pt-BR", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });

        var priceOld = document.getElementById("js-price-old");
        var discount = document.getElementById("js-discount");

        if (priceOld) {
            priceOld.textContent = originalPrice.toLocaleString("pt-BR", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        }

        if (discount) {
            discount.textContent = percentage + "% OFF";
        }


      /* hidden variant id */
      var hidden = document.getElementById('js-variant-hidden');
      if (hidden) hidden.value = this.value;

      /* chips */
      document.getElementById('js-brand').textContent = opt.dataset.brand || '—';
      document.getElementById('js-stock').textContent = opt.dataset.stock;

      var flavorChip = document.getElementById('js-flavor-chip');
      var sizeChip   = document.getElementById('js-size-chip');
      if (opt.dataset.flavor) {
        document.getElementById('js-flavor').textContent = opt.dataset.flavor;
        flavorChip.classList.remove('hidden-chip');
      } else {
        flavorChip.classList.add('hidden-chip');
      }
      if (opt.dataset.size) {
        document.getElementById('js-size').textContent = opt.dataset.size;
        sizeChip.classList.remove('hidden-chip');
      } else {
        sizeChip.classList.add('hidden-chip');
      }

      /* stock alert */
      var stock = parseInt(opt.dataset.stock, 10);
      var box   = document.getElementById('js-stock-alert');
      if (box) {
        if (stock <= 0) {
          box.innerHTML = '<div class="stock-alert stock-alert--out"><span class="stock-alert__icon">✕</span><span>Produto <strong>esgotado</strong>.</span></div>';
        } else if (stock <= 5) {
          box.innerHTML = '<div class="stock-alert stock-alert--low"><span class="stock-alert__icon">⚠</span><div><strong>Últimas '+stock+' unidades!</strong><div class="stock-bar"><div class="stock-bar__fill stock-bar__fill--low" style="width:20%"></div></div></div></div>';
        } else if (stock <= 10) {
          box.innerHTML = '<div class="stock-alert stock-alert--low"><span class="stock-alert__icon">🔥</span><div>Alta procura — apenas <strong>'+stock+'</strong> restantes.<div class="stock-bar"><div class="stock-bar__fill stock-bar__fill--hot" style="width:40%"></div></div></div></div>';
        } else {
          box.innerHTML = '';
        }
      }

      /* installments */
      var installments = JSON.parse(opt.dataset.installments || '[]');
      var picker = document.getElementById('js-installments');
      if (picker) {
        picker.innerHTML = '';
        installments.forEach(function (item) {
          var o = document.createElement('option');
          o.value = item.times;
          o.textContent =
              item.times +
              'x de R$ ' +
              item.value.toLocaleString("pt-BR", {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2
              });
          
          picker.appendChild(o);
        });
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
