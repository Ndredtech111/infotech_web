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

  // copyright year is fixed (2022) in the footer markup

  // Contact form: posts to our own API on the GoDaddy hosting (server/contact-api/contact.php),
  // which saves the enquiry to MySQL and emails the company inboxes.
  var API_URL = 'https://api.ndrinfotech.com/contact.php';
  var MAIL_TO = 'hr@ndrinfotech.com';
  var MAIL_CC = 'dineshreddyvari@ndrinfotech.com';   // used only by the email-app fallback
  var form = document.getElementById('form'), note = document.getElementById('note');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = new FormData(form), btn = form.querySelector('button[type=submit]');
    note.style.color = '';
    if (d.get('_honey')) return;                                   // spam trap
    var phoneDigits = String(d.get('phone') || '').replace(/\D/g, '');
    if (!d.get('name') || !/^\S+@\S+\.\S+$/.test(d.get('email')) || !d.get('msg')) {
      note.textContent = 'Please complete name, a valid email and message.'; return;
    }
    if (!/^[+()\d\s-]+$/.test(String(d.get('phone') || '')) || phoneDigits.length < 7 || phoneDigits.length > 15) {
      note.textContent = 'Please enter a valid mobile number (digits only, with an optional country code).'; return;
    }
    // no hyperlinks allowed in the name or message
    var LINK = /(https?:\/\/|ftp:\/\/|www\.|<\s*a\b|href\s*=|\[url|\b[a-z0-9-]+\.(?:com|org|io|info|biz|xyz|ru|cn|top|site|online|link|click|shop|app|ly|tk|ml|ga|cf)\b|\b[a-z0-9-]+\.[a-z]{2,}\/\S*)/i;
    function hasLink(v) { return LINK.test(String(v || '').replace(/[^\s@]+@[^\s@]+\.[^\s@]+/g, ' ')); }   // email addresses are fine
    if (hasLink(d.get('name')) || hasLink(d.get('msg'))) {
      note.style.color = '#b45309';
      note.textContent = 'Links are not allowed in the name or message. Please remove any web addresses and try again.'; return;
    }
    var label = btn.textContent; btn.disabled = true; btn.textContent = 'Sending…'; note.textContent = '';
    function mailtoFallback() {
      var body = 'Name: ' + d.get('name') + '\nEmail: ' + d.get('email') + '\nMobile: ' + d.get('phone') + '\nInterest: ' + d.get('topic') + '\n\n' + d.get('msg');
      window.location.href = 'mailto:' + MAIL_TO + '?cc=' + encodeURIComponent(MAIL_CC) + '&subject=' + encodeURIComponent('Website enquiry – ' + d.get('topic')) + '&body=' + encodeURIComponent(body);
    }
    var ctrl = ('AbortController' in window) ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 15000);   // never hang on "Sending…"
    fetch(API_URL, {
      method: 'POST',
      signal: ctrl ? ctrl.signal : undefined,
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({
        name: d.get('name'), email: d.get('email'), phone: d.get('phone'), topic: d.get('topic'), msg: d.get('msg'),
        _honey: d.get('_honey') || ''
      })
    }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (j) { return { status: r.status, ok: !!(r.ok && j.ok), j: j }; });
      })
      .then(function (res) {
        if (res.status === 429) {
          note.style.color = '#b45309';
          note.textContent = 'Too many messages from this device. Please try again later or call us.';
          return;
        }
        if (res.status === 422) {
          note.style.color = '#b45309';
          note.textContent = 'Please check your details. Links are not allowed, and the email and mobile number must be valid.';
          return;
        }
        if (!res.ok) throw new Error('send failed');
        form.reset();
        note.style.color = '';
        note.textContent = 'Thank you. Your message has been sent and we will get back to you soon.';
      })
      .catch(function () {
        note.style.color = '#b45309';
        note.textContent = 'We could not send this automatically, so we are opening your email app instead.';
        setTimeout(mailtoFallback, 900);
      })
      .then(function () { clearTimeout(timer); btn.disabled = false; btn.textContent = label; });
  });
})();

// Fixed date & time widget (bottom-right corner, every page)
(function () {
  var w = document.createElement('div');
  w.className = 'dt-widget';
  w.setAttribute('role', 'timer');
  w.setAttribute('aria-label', 'Current date and time');
  w.innerHTML = '<svg class="dt-ic" viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/><circle class="dt-dot" cx="12" cy="15" r="1.6"/></svg>' +
    '<div class="dt-txt"><span class="dt-date"></span><span class="dt-time"></span></div>';
  document.body.appendChild(w);
  var dEl = w.querySelector('.dt-date'), tEl = w.querySelector('.dt-time');
  var dfmt, tfmt;
  try {
    dfmt = new Intl.DateTimeFormat(undefined, { weekday: 'short', day: '2-digit', month: 'short', year: 'numeric' });
    tfmt = new Intl.DateTimeFormat(undefined, { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  } catch (e) { dfmt = tfmt = null; }
  function tick() {
    var n = new Date();
    dEl.textContent = dfmt ? dfmt.format(n) : n.toDateString();
    tEl.textContent = tfmt ? tfmt.format(n) : n.toLocaleTimeString();
  }
  tick(); setInterval(tick, 1000);
})();
