(function () {
  var nav = document.getElementById('nav'), menu = document.getElementById('menu'), burger = document.getElementById('burger');
  function onScroll() { nav.classList.toggle('solid', window.scrollY > 20); }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  burger.addEventListener('click', function () {
    var open = menu.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });
  menu.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') { menu.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }
  });

  function count(el) {
    var end = +el.dataset.count, suf = el.dataset.suffix || '', t0 = null;
    (function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / 1200, 1);
      el.textContent = Math.round(end * p) + suf;
      if (p < 1) requestAnimationFrame(step);
    })(performance.now());
  }
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      e.target.querySelectorAll('[data-count]').forEach(count);
      io.unobserve(e.target);
    });
  }, { threshold: .15 }) : null;
  // split headings marked for word-by-word reveal
  document.querySelectorAll('#story h2, #values h2, #approach h2, #caps h2, #tl1 h2').forEach(function (h) {
    var words = h.textContent.trim().split(/\s+/);
    h.setAttribute('aria-label', h.textContent.trim());
    h.innerHTML = words.map(function (w, i) { return '<span class="w" aria-hidden="true"><span style="--i:' + i + '">' + w + '</span></span>'; }).join(' ');
  });
  document.querySelectorAll('.reveal').forEach(function (el) {
    if (io) io.observe(el); else { el.classList.add('in'); el.querySelectorAll('[data-count]').forEach(function (c) { c.textContent = c.dataset.count + (c.dataset.suffix || ''); }); }
  });

  var yr = document.getElementById('yr'); if (yr) yr.textContent = new Date().getFullYear();

  // Placeholder submit: opens a mailto draft. Replace with a real endpoint (Formspree/Netlify/API).
  var form = document.getElementById('form'), note = document.getElementById('note');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = new FormData(form);
    if (!d.get('name') || !/^\S+@\S+\.\S+$/.test(d.get('email')) || !d.get('msg')) {
      note.textContent = 'Please complete name, a valid email and message.'; return;
    }
    var body = 'Name: ' + d.get('name') + '\nEmail: ' + d.get('email') + '\nInterest: ' + d.get('topic') + '\n\n' + d.get('msg');
    window.location.href = 'mailto:hr@ndrinfotech.com?subject=' + encodeURIComponent('Website enquiry – ' + d.get('topic')) + '&body=' + encodeURIComponent(body);
    note.textContent = 'Opening your email app…';
  });
})();
