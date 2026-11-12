// Home page: challenge explorer tabs + bento spotlight
(function () {
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.ch-tab'));
  var pans = Array.prototype.slice.call(document.querySelectorAll('.ch-pan'));

  var icons = Array.prototype.slice.call(document.querySelectorAll('.ch-ic'));
  var hint = document.getElementById('ch-hint');
  function select(i, focus) {
    if (hint) hint.hidden = true;
    tabs.forEach(function (t, k) {
      var on = k === i;
      t.classList.toggle('on', on);
      t.setAttribute('aria-selected', on);
      t.tabIndex = on ? 0 : -1;
    });
    icons.forEach(function (c, k) { c.classList.toggle('on', k === i); });
    pans.forEach(function (p, k) {
      if (k === i) { p.hidden = false; void p.offsetWidth; requestAnimationFrame(function () { p.classList.add('on'); }); }
      else { p.classList.remove('on'); p.hidden = true; }
    });
    if (focus) tabs[i].focus();
  }
  icons.forEach(function (c, i) { c.addEventListener('click', function () { select(i); }); });
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(i); });
    t.addEventListener('keydown', function (e) {
      var n = tabs.length;
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { e.preventDefault(); select((i + 1) % n, true); }
      if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { e.preventDefault(); select((i - 1 + n) % n, true); }
    });
  });

  // bento: tiles emerge from the centre of the grid
  var bento = document.querySelector('.bento');
  if (bento) {
    var tiles = Array.prototype.slice.call(bento.querySelectorAll('.bt'));
    var measure = function () {
      // measure the resting layout: neutralise the hidden-state transforms first
      tiles.forEach(function (b) { b.style.transition = 'none'; b.style.translate = '0 0'; b.style.scale = '1'; });
      var g = bento.getBoundingClientRect(), cx = g.left + g.width / 2, cy = g.top + g.height / 2, out = [];
      tiles.forEach(function (b) {
        var r = b.getBoundingClientRect();
        out.push([cx - (r.left + r.width / 2), cy - (r.top + r.height / 2)]);
      });
      tiles.forEach(function (b, i) {
        b.style.setProperty('--dx', out[i][0] + 'px');
        b.style.setProperty('--dy', out[i][1] + 'px');
        b.style.translate = ''; b.style.scale = ''; void b.offsetWidth; b.style.transition = '';
      });
    };
    measure();
    window.addEventListener('resize', function () { if (!bento.classList.contains('in')) measure(); });
    if ('IntersectionObserver' in window) {
      var io2 = new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { measure(); bento.classList.add('in'); io2.disconnect(); }
      }, { threshold: .25 });
      io2.observe(bento);
    } else bento.classList.add('in');
  }

  // cursor spotlight on bento tiles
  document.querySelectorAll('.bt').forEach(function (b) {
    b.addEventListener('mousemove', function (e) {
      var r = b.getBoundingClientRect();
      b.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      b.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });
})();
