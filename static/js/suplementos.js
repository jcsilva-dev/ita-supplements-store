 /*<!-- ================================================================
     § SCRIPTS — mínimo, performático, sem vazamento de memória
     ================================================================ -->*/


(function () {
  'use strict';

  /* ── Util: one IntersectionObserver for all .reveal elements ── */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  }, { threshold: 0.07, rootMargin: '0px 0px -28px 0px' });

  document.querySelectorAll('.reveal').forEach(function (el, i) {
    /* stagger delay capped at 0.4s so late items don't feel broken */
    if (!el.style.transitionDelay) {
      el.style.transitionDelay = (Math.min(i, 8) * 0.06) + 's';
    }
    io.observe(el);
  });

  /* ── Banner auto-play ── */
  (function () {
    var slides = document.querySelectorAll('.banner__slide');
    var dots   = document.querySelectorAll('.banner__dot');
    if (!slides.length) return;

    var cur = 0;
    var tid;

    function show(n) {
      slides[cur].classList.remove('is-active');
      dots[cur] && dots[cur].classList.remove('is-active');
      dots[cur] && dots[cur].setAttribute('aria-selected', 'false');
      cur = (n + slides.length) % slides.length;
      slides[cur].classList.add('is-active');
      dots[cur] && dots[cur].classList.add('is-active');
      dots[cur] && dots[cur].setAttribute('aria-selected', 'true');
    }

    function play()  { tid = setInterval(function () { show(cur + 1); }, 5000); }
    function pause() { clearInterval(tid); }

    play();

    dots.forEach(function (d) {
      d.addEventListener('click', function () {
        pause(); show(+this.dataset.slide); play();
      });
    });

    var banner = document.querySelector('.banner');
    if (banner) {
      banner.addEventListener('mouseenter', pause);
      banner.addEventListener('mouseleave', play);
    }
  }());

  /* ── Card carousel nav (arrows — manual multi-image) ── */
  window.navCard = function (btn, dir) {
    var box  = btn.closest('[data-carousel-box]');
    var imgs = Array.from(box.querySelectorAll('.card__img--a, .card__img--b'));
    if (imgs.length < 2) return;

    var cur = imgs.findIndex(function (img) { return img.style.zIndex === '3'; });
    if (cur === -1) cur = 0;

    imgs[cur].style.opacity = '0';
    imgs[cur].style.zIndex  = '1';

    var next = (cur + dir + imgs.length) % imgs.length;
    imgs[next].style.opacity = '1';
    imgs[next].style.zIndex  = '3';
  };

}());


