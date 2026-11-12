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
  document.querySelectorAll('#story h2, #values h2, #approach h2, #caps h2, #tl1 h2, #w1 h2, #w2 h2, #w3 h2, #w4 h2, #w5 .two h2, #x1 h2, #x2 h2, #x3 h2, #x4 h2, #x5 h2, #x6 h2').forEach(function (h) {
    var words = h.textContent.trim().split(/\s+/);
    h.setAttribute('aria-label', h.textContent.trim());
    h.innerHTML = words.map(function (w, i) { return '<span class="w" aria-hidden="true"><span style="--i:' + i + '">' + w + '</span></span>'; }).join(' ');
  });
  document.querySelectorAll('.reveal').forEach(function (el) {
    if (io) io.observe(el); else { el.classList.add('in'); el.querySelectorAll('[data-count]').forEach(function (c) { c.textContent = c.dataset.count + (c.dataset.suffix || ''); }); }
  });

  var yr = document.getElementById('yr'); if (yr) yr.textContent = new Date().getFullYear();

  // Contact form: emails the enquiry to the address below via FormSubmit (https://formsubmit.co).
  // First submission triggers a one-time activation email to that inbox; click the link in it to enable delivery.
  var MAIL_TO = 'hr@ndrinfotech.com';
  var form = document.getElementById('form'), note = document.getElementById('note');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = new FormData(form), btn = form.querySelector('button[type=submit]');
    note.style.color = '';
    if (d.get('_honey')) return;                                   // spam trap
    if (!d.get('name') || !/^\S+@\S+\.\S+$/.test(d.get('email')) || !d.get('msg')) {
      note.textContent = 'Please complete name, a valid email and message.'; return;
    }
    var label = btn.textContent; btn.disabled = true; btn.textContent = 'Sending…'; note.textContent = '';
    function mailtoFallback() {
      var body = 'Name: ' + d.get('name') + '\nEmail: ' + d.get('email') + '\nInterest: ' + d.get('topic') + '\n\n' + d.get('msg');
      window.location.href = 'mailto:' + MAIL_TO + '?subject=' + encodeURIComponent('Website enquiry – ' + d.get('topic')) + '&body=' + encodeURIComponent(body);
    }
    fetch('https://formsubmit.co/ajax/' + MAIL_TO, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({
        name: d.get('name'), email: d.get('email'), interest: d.get('topic'), message: d.get('msg'),
        _subject: 'Website enquiry – ' + d.get('topic') + ' – ' + d.get('name'),
        _template: 'table', _captcha: 'false'
      })
    }).then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok && j.success !== 'false' && j.success !== false, j: j }; }); })
      .then(function (res) {
        if (!res.ok) throw new Error('send failed');
        form.reset();
        note.textContent = 'Thank you. Your message has been sent and we will get back to you soon.';
      })
      .catch(function () {
        note.style.color = '#b45309';
        note.textContent = 'We could not send this automatically, so we are opening your email app instead.';
        setTimeout(mailtoFallback, 900);
      })
      .then(function () { btn.disabled = false; btn.textContent = label; });
  });
})();
