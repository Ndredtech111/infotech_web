// Context-aware hero background animations. Each hero declares data-scene="...".
(function () {
  var hero = document.querySelector('[data-scene]');
  if (!hero) return;
  var scene = hero.dataset.scene;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  var cv = document.createElement('canvas');
  cv.className = 'bg-canvas';
  cv.setAttribute('aria-hidden', 'true');
  hero.insertBefore(cv, hero.firstChild);
  var ctx = cv.getContext('2d'), W = 0, H = 0, dpr = 1, mouse = { x: -999, y: -999 }, visible = true, t0 = performance.now();

  var C1 = '34,211,238', C2 = '139,92,246';
  function rgba(c, a) { return 'rgba(' + c + ',' + a + ')'; }
  function rnd(a, b) { return a + Math.random() * (b - a); }

  function size() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = hero.clientWidth; H = hero.clientHeight;
    cv.width = W * dpr; cv.height = H * dpr;
    cv.style.width = W + 'px'; cv.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    init();
  }

  var S = {}; // scene state
  var scenes = {};

  // ---- network: people / nodes connecting (home, talent, about) ----
  scenes.network = {
    init: function () {
      var n = Math.round(Math.min(70, W * H / 16000));
      S.p = []; for (var i = 0; i < n; i++) S.p.push({ x: rnd(0, W), y: rnd(0, H), vx: rnd(-.25, .25), vy: rnd(-.25, .25), r: rnd(1.5, 3) });
    },
    draw: function () {
      var p = S.p, i, j, d;
      for (i = 0; i < p.length; i++) {
        var a = p[i]; a.x += a.vx; a.y += a.vy;
        if (a.x < 0 || a.x > W) a.vx *= -1; if (a.y < 0 || a.y > H) a.vy *= -1;
        var md = Math.hypot(a.x - mouse.x, a.y - mouse.y);
        if (md < 140) { a.x += (a.x - mouse.x) * .003; a.y += (a.y - mouse.y) * .003; }
        for (j = i + 1; j < p.length; j++) {
          var b = p[j]; d = Math.hypot(a.x - b.x, a.y - b.y);
          if (d < 150) { ctx.strokeStyle = rgba(i % 2 ? C1 : C2, (1 - d / 150) * .35); ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
        }
        ctx.fillStyle = rgba(i % 3 ? C1 : C2, .85); ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, 6.283); ctx.fill();
      }
    }
  };

  // ---- code rain (development, technologies) ----
  scenes.code = {
    init: function () {
      var cols = Math.ceil(W / 26); S.cols = [];
      for (var i = 0; i < cols; i++) S.cols.push({ y: rnd(-H, 0), v: rnd(.6, 1.8), ch: [] });
      S.chars = '{}()<>/;=+*&#01'.split('');
    },
    draw: function () {
      ctx.font = '15px monospace';
      S.cols.forEach(function (c, i) {
        c.y += c.v;
        if (c.y > H + 200) { c.y = rnd(-200, 0); c.v = rnd(.6, 1.8); }
        for (var k = 0; k < 9; k++) {
          var y = c.y - k * 20; if (y < 0 || y > H) continue;
          if (!c.ch[k] || Math.random() < .02) c.ch[k] = S.chars[Math.random() * S.chars.length | 0];
          ctx.fillStyle = rgba(k === 0 ? C1 : (i % 4 ? C1 : C2), k === 0 ? .9 : .45 * (1 - k / 9));
          ctx.fillText(c.ch[k], i * 26, y);
        }
      });
    }
  };

  // ---- bars + line chart (data & BI) ----
  scenes.bars = {
    init: function () { S.n = Math.max(10, Math.round(W / 70)); S.ph = []; for (var i = 0; i < S.n; i++) S.ph.push(rnd(0, 6.28)); },
    draw: function (t) {
      var w = W / S.n, pts = [];
      for (var i = 0; i < S.n; i++) {
        var h = (.25 + .2 * Math.sin(t / 1400 + S.ph[i]) + .1 * Math.sin(t / 700 + i)) * H * .8;
        var g = ctx.createLinearGradient(0, H - h, 0, H); g.addColorStop(0, rgba(i % 2 ? C1 : C2, .35)); g.addColorStop(1, rgba(C1, 0));
        ctx.fillStyle = g; ctx.fillRect(i * w + w * .2, H - h, w * .6, h);
        pts.push([i * w + w / 2, H - h - 20 - 12 * Math.sin(t / 900 + i)]);
      }
      ctx.strokeStyle = rgba(C1, .8); ctx.lineWidth = 2; ctx.beginPath();
      pts.forEach(function (q, i) { i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); }); ctx.stroke();
      pts.forEach(function (q) { ctx.fillStyle = rgba(C2, 1); ctx.beginPath(); ctx.arc(q[0], q[1], 3.5, 0, 6.283); ctx.fill(); });
    }
  };

  // ---- data packets flowing left -> right on lanes (migration) ----
  scenes.flow = {
    init: function () {
      var lanes = Math.max(4, Math.round(H / 55)); S.l = [];
      for (var i = 0; i < lanes; i++) { var pk = []; for (var k = 0; k < 6; k++) pk.push(rnd(0, W)); S.l.push({ y: (i + .5) * H / lanes, v: rnd(.8, 2.4), pk: pk }); }
    },
    draw: function () {
      S.l.forEach(function (l, i) {
        ctx.strokeStyle = rgba(C1, .08); ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(0, l.y); ctx.lineTo(W, l.y); ctx.stroke();
        l.pk = l.pk.map(function (x) {
          x += l.v; if (x > W + 40) x = -40;
          var g = ctx.createLinearGradient(x - 60, 0, x, 0); g.addColorStop(0, rgba(C2, 0)); g.addColorStop(1, rgba(i % 2 ? C1 : C2, .8));
          ctx.strokeStyle = g; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x - 60, l.y); ctx.lineTo(x, l.y); ctx.stroke();
          ctx.fillStyle = rgba(C1, .95); ctx.fillRect(x, l.y - 4, 8, 8); return x;
        });
      });
    }
  };

  // ---- infinity loop with traveling dots (devops) ----
  scenes.loop = {
    init: function () { S.cx = W * .72; S.cy = H * .5; S.a = Math.min(W * .26, 320); S.b = Math.min(H * .32, 130); },
    draw: function (t) {
      function pt(u) { var s = Math.sin(u), c = Math.cos(u), d = 1 + s * s; return [S.cx + S.a * c / d, S.cy + S.b * 1.6 * s * c / d]; }
      ctx.strokeStyle = rgba(C1, .25); ctx.lineWidth = 1.2; ctx.beginPath();
      for (var u = 0; u <= 6.29; u += .04) { var q = pt(u); u ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); } ctx.closePath(); ctx.stroke();
      for (var k = 0; k < 14; k++) {
        var p = pt(t / 1100 + k * .45), a = 1 - k / 14;
        ctx.fillStyle = rgba(k % 2 ? C1 : C2, a); ctx.beginPath(); ctx.arc(p[0], p[1], 4 * a + 1, 0, 6.283); ctx.fill();
      }
    }
  };

  // ---- drifting clouds + rising data points (cloud) ----
  scenes.cloud = {
    init: function () {
      S.c = []; for (var i = 0; i < 6; i++) S.c.push({ x: rnd(0, W), y: rnd(H * .1, H * .8), s: rnd(.6, 1.6), v: rnd(.15, .45) });
      S.d = []; for (i = 0; i < 40; i++) S.d.push({ x: rnd(0, W), y: rnd(0, H), v: rnd(.2, .8) });
    },
    draw: function () {
      S.c.forEach(function (c) {
        c.x += c.v; if (c.x > W + 200) c.x = -200;
        ctx.save(); ctx.translate(c.x, c.y); ctx.scale(c.s, c.s); ctx.strokeStyle = rgba(C1, .35); ctx.lineWidth = 1.4;
        ctx.beginPath(); ctx.arc(-40, 10, 22, Math.PI * .5, Math.PI * 1.5); ctx.arc(-12, -12, 30, Math.PI, Math.PI * 1.95);
        ctx.arc(30, 0, 24, Math.PI * 1.5, Math.PI * .5); ctx.closePath(); ctx.stroke(); ctx.restore();
      });
      S.d.forEach(function (d, i) { d.y -= d.v; if (d.y < 0) { d.y = H; d.x = rnd(0, W); } ctx.fillStyle = rgba(i % 3 ? C1 : C2, .55); ctx.fillRect(d.x, d.y, 2, 2); });
    }
  };

  // ---- radar sweep (consulting) ----
  scenes.radar = {
    init: function () { S.cx = W * .75; S.cy = H * .5; S.r = Math.min(H * .85, W * .35); S.b = []; for (var i = 0; i < 7; i++) S.b.push({ a: rnd(0, 6.28), d: rnd(.2, .95) }); },
    draw: function (t) {
      for (var k = 1; k <= 4; k++) { ctx.strokeStyle = rgba(C1, .16); ctx.beginPath(); ctx.arc(S.cx, S.cy, S.r * k / 4, 0, 6.283); ctx.stroke(); }
      ctx.strokeStyle = rgba(C1, .12); ctx.beginPath(); ctx.moveTo(S.cx - S.r, S.cy); ctx.lineTo(S.cx + S.r, S.cy); ctx.moveTo(S.cx, S.cy - S.r); ctx.lineTo(S.cx, S.cy + S.r); ctx.stroke();
      var a = t / 1500 % 6.283;
      for (var i = 0; i < 40; i++) { ctx.strokeStyle = rgba(C1, .35 * (1 - i / 40)); ctx.beginPath(); ctx.moveTo(S.cx, S.cy); ctx.lineTo(S.cx + Math.cos(a - i * .02) * S.r, S.cy + Math.sin(a - i * .02) * S.r); ctx.stroke(); }
      S.b.forEach(function (b) {
        var diff = ((a - b.a) % 6.283 + 6.283) % 6.283, al = Math.max(0, 1 - diff / 3);
        ctx.fillStyle = rgba(C2, al); ctx.beginPath(); ctx.arc(S.cx + Math.cos(b.a) * S.r * b.d, S.cy + Math.sin(b.a) * S.r * b.d, 4, 0, 6.283); ctx.fill();
      });
    }
  };

  // ---- orbits around a hub (services) ----
  scenes.orbit = {
    init: function () { S.cx = W * .75; S.cy = H * .5; S.R = Math.min(H * .9, W * .3); },
    draw: function (t) {
      ctx.fillStyle = rgba(C1, .9); ctx.beginPath(); ctx.arc(S.cx, S.cy, 7, 0, 6.283); ctx.fill();
      ctx.strokeStyle = rgba(C1, .3); ctx.beginPath(); ctx.arc(S.cx, S.cy, 14 + 3 * Math.sin(t / 400), 0, 6.283); ctx.stroke();
      for (var k = 1; k <= 3; k++) {
        var r = S.R * k / 3; ctx.strokeStyle = rgba(C1, .14); ctx.beginPath(); ctx.arc(S.cx, S.cy, r, 0, 6.283); ctx.stroke();
        for (var j = 0; j < 2; j++) {
          var a = t / (2400 + k * 900) * (k % 2 ? 1 : -1) * 3 + j * 3.14 + k;
          var x = S.cx + Math.cos(a) * r, y = S.cy + Math.sin(a) * r;
          ctx.strokeStyle = rgba(C2, .35); ctx.beginPath(); ctx.moveTo(S.cx, S.cy); ctx.lineTo(x, y); ctx.stroke();
          ctx.fillStyle = rgba(j ? C2 : C1, .95); ctx.beginPath(); ctx.arc(x, y, 5, 0, 6.283); ctx.fill();
        }
      }
    }
  };

  // ---- expanding ripples (contact) ----
  scenes.pulse = {
    init: function () { S.cx = W * .78; S.cy = H * .5; S.max = Math.max(W, H) * .7; },
    draw: function (t) {
      for (var k = 0; k < 5; k++) {
        var p = ((t / 4200) + k / 5) % 1;
        ctx.strokeStyle = rgba(k % 2 ? C2 : C1, (1 - p) * .5); ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(S.cx, S.cy, p * S.max, 0, 6.283); ctx.stroke();
      }
      ctx.fillStyle = rgba(C1, .95); ctx.beginPath(); ctx.arc(S.cx, S.cy, 6, 0, 6.283); ctx.fill();
    }
  };

  var sc = scenes[scene] || scenes.network;
  function init() { S = {}; sc.init(); }

  function frame(now) {
    if (visible) { ctx.clearRect(0, 0, W, H); sc.draw(now - t0); }
    if (!reduce) requestAnimationFrame(frame);
  }

  size();
  window.addEventListener('resize', size);
  hero.addEventListener('mousemove', function (e) { var r = hero.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
  hero.addEventListener('mouseleave', function () { mouse.x = mouse.y = -999; });
  if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }).observe(hero);
  if (reduce) { sc.draw(3000); } else requestAnimationFrame(frame);
})();
