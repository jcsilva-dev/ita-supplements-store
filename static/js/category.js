(function () {
  'use strict';

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  }, { threshold: 0.07, rootMargin: '0px 0px -24px 0px' });

  document.querySelectorAll('.reveal').forEach(function (el, i) {
    if (!el.style.transitionDelay) {
      el.style.transitionDelay = (Math.min(i, 8) * 0.055) + 's';
    }
    io.observe(el);
  });

}());
