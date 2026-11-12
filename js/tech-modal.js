// Technology detail pop-up (technologies.html)
(function () {
  var dataEl = document.getElementById('tech-data');
  if (!dataEl) return;
  var data = JSON.parse(dataEl.textContent), last = null;

  var m = document.createElement('div');
  m.className = 'modal';
  m.setAttribute('role', 'dialog');
  m.setAttribute('aria-modal', 'true');
  m.setAttribute('aria-labelledby', 'm-title');
  m.hidden = true;
  m.innerHTML =
    '<div class="m-back" data-close></div>' +
    '<div class="m-card" tabindex="-1">' +
    '<button class="m-x" data-close aria-label="Close">×</button>' +
    '<div class="m-ic" id="m-ic"></div><p class="eyebrow" id="m-grp"></p><h3 id="m-title"></h3>' +
    '<p class="m-desc" id="m-desc"></p><h4>How we use it</h4><ul class="checks" id="m-pts"></ul>' +
    '<a class="btn" href="contact.html">Discuss your project</a></div>';
  document.body.appendChild(m);

  function esc(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

  function open(name, el) {
    var t = data[name];
    if (!t) return;
    last = el;
    document.getElementById('m-ic').innerHTML = t.icon;
    document.getElementById('m-grp').textContent = t.group;
    document.getElementById('m-title').textContent = name;
    document.getElementById('m-desc').textContent = t.desc;
    document.getElementById('m-pts').innerHTML = t.points.map(function (p) { return '<li>' + esc(p) + '</li>'; }).join('');
    m.hidden = false;
    document.body.classList.add('lock');
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { m.classList.add('show'); m.querySelector('.m-card').focus(); });
    });
  }

  function close() {
    m.classList.remove('show');
    document.body.classList.remove('lock');
    setTimeout(function () { if (!m.classList.contains('show')) m.hidden = true; }, 450);
    if (last) last.focus();
  }

  document.querySelectorAll('.tile[data-tech]').forEach(function (t) {
    t.addEventListener('click', function () { open(t.dataset.tech, t); });
    t.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(t.dataset.tech, t); }
    });
  });

  m.addEventListener('click', function (e) { if (e.target.hasAttribute('data-close')) close(); });

  document.addEventListener('keydown', function (e) {
    if (m.hidden) return;
    if (e.key === 'Escape') close();
    if (e.key === 'Tab') {
      var f = m.querySelectorAll('button,a'), first = f[0], end = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); end.focus(); }
      else if (!e.shiftKey && document.activeElement === end) { e.preventDefault(); first.focus(); }
    }
  });
})();
