(function () {
  'use strict';

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  }, { threshold: 0.06, rootMargin: '0px 0px -20px 0px' });

  document.querySelectorAll('.reveal').forEach(function (el, i) {
    if (!el.style.transitionDelay) {
      el.style.transitionDelay = (Math.min(i, 6) * 0.06) + 's';
    }
    io.observe(el);
  });

}());
