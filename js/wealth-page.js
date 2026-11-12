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

// FAQ accordion with smooth open/close: opening one question closes the others
(function () {
  var items = Array.prototype.slice.call(document.querySelectorAll('.faq details'));
  if (!items.length) return;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var EASE = 'cubic-bezier(.2,.85,.25,1)', DUR = 420;

  function collapsedHeight(d) {
    var cs = getComputedStyle(d), s = d.querySelector('summary');
    return s.offsetHeight + parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom) + parseFloat(cs.borderTopWidth) + parseFloat(cs.borderBottomWidth);
  }
  function run(d, from, to, done) {
    if (d._anim) d._anim.cancel();
    d.style.overflow = 'hidden';
    var a = d._anim = d.animate({ height: [from + 'px', to + 'px'] }, { duration: DUR, easing: EASE });
    var end = function () {
      if (d._anim !== a) return;
      d._anim = null; d.style.overflow = ''; d.style.height = ''; if (done) done();
    };
    a.onfinish = a.oncancel = end;
    setTimeout(end, DUR + 150);   // safety net if the finish event is missed
  }
  function open(d) {
    if (d.open && !d.classList.contains('closing')) return;
    var from = d.offsetHeight;
    d.classList.remove('closing'); d.open = true; d.classList.add('is-open');
    if (reduce) return;
    run(d, from, d.scrollHeight);
  }
  function close(d) {
    if (!d.open || d.classList.contains('closing')) return;
    var from = d.offsetHeight, to = collapsedHeight(d);
    d.classList.remove('is-open');
    if (reduce) { d.open = false; return; }
    d.classList.add('closing');
    run(d, from, to, function () { d.open = false; d.classList.remove('closing'); });
  }
  items.forEach(function (d) {
    if (d.open) d.classList.add('is-open');
    d.querySelector('summary').addEventListener('click', function (e) {
      e.preventDefault();
      if (d.open && !d.classList.contains('closing')) close(d);
      else { items.forEach(function (o) { if (o !== d) close(o); }); open(d); }
    });
  });
})();
