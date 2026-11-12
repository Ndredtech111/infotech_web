// Wealth page: scroll progress bar + gentle hero parallax
(function () {
  var bar = document.createElement('div'); bar.className = 'scroll-prog'; bar.setAttribute('aria-hidden', 'true'); document.body.appendChild(bar);
  var hero = document.querySelector('.page-hero .wrap'), tick = false;
  function upd() {
    var h = document.documentElement, max = h.scrollHeight - h.clientHeight, y = window.scrollY || h.scrollTop;
    bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(y / max, 1) : 0) + ')';
    if (hero && y < 700 && !matchMedia('(prefers-reduced-motion: reduce)').matches) { hero.style.transform = 'translateY(' + (y * .18) + 'px)'; hero.style.opacity = Math.max(0, 1 - y / 650); }
    tick = false;
  }
  window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(upd); } }, { passive: true });
  upd();
})();
