(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Header border once scrolled
  var header = document.querySelector('.site-header');
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Mobile menu
  var btn = document.querySelector('.menu-btn');
  if (btn) {
    btn.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.querySelector('.label').textContent = open ? 'Close' : 'Menu';
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('menu-open')) btn.click();
    });
  }

  // Year
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // ---------- The mane: the one living element ----------
  var panel = document.querySelector('.mane-panel');
  if (panel) {
    var cv = panel.querySelector('canvas');
    var ctx = cv.getContext('2d');
    var W = 0, H = 0, dpr = 1, N = 132;
    var px = -1, py = -1, pTarget = 0, pAmt = 0, burst = 0, t0 = performance.now();
    var css = getComputedStyle(document.documentElement);
    var ink = (css.getPropertyValue('--ivory') || '#F0ECE4').trim();
    var moss = (css.getPropertyValue('--marigold') || '#F4A51C').trim();
    var night = (css.getPropertyValue('--night') || '#17140F').trim();

    function size() {
      var r = panel.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = r.width; H = r.height;
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function draw(now) {
      var t = (now - t0) / 1000;
      pAmt += (pTarget - pAmt) * 0.08;
      burst *= 0.94;
      ctx.clearRect(0, 0, W, H);
      var cx = W * 0.5, cy = H * 0.46;
      var R = Math.min(W, H) * 0.42;
      var r0 = R * 0.3;
      var pa = Math.atan2(py - cy, px - cx);
      ctx.lineCap = 'round';
      for (var i = 0; i < N; i++) {
        var a = (i / N) * Math.PI * 2 - Math.PI / 2;
        var wave = Math.sin(a * 5 + t * 0.9) * 0.08 + Math.sin(a * 11 - t * 1.3) * 0.05 + Math.sin(a * 3 + t * 0.4) * 0.06;
        var d = Math.atan2(Math.sin(a - pa), Math.cos(a - pa));
        var face = Math.max(0, Math.cos(d)) ;
        var lean = pAmt * face * face * 0.35;
        var len = R * (0.62 + wave + lean + burst * (0.25 + 0.2 * Math.sin(i * 1.7)));
        var bend = Math.sin(t * 0.7 + i * 0.35) * 0.06 + pAmt * Math.sin(d) * -0.12;
        var x1 = cx + Math.cos(a) * r0, y1 = cy + Math.sin(a) * r0;
        var x2 = cx + Math.cos(a + bend) * (r0 + len), y2 = cy + Math.sin(a + bend) * (r0 + len);
        var mx = cx + Math.cos(a + bend * 0.4) * (r0 + len * 0.55), my = cy + Math.sin(a + bend * 0.4) * (r0 + len * 0.55);
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.quadraticCurveTo(mx, my, x2, y2);
        ctx.strokeStyle = i % 4 === 0 ? moss : ink;
        ctx.globalAlpha = i % 4 === 0 ? 1 : 0.55;
        ctx.lineWidth = i % 4 === 0 ? 2.2 : 1.3;
        ctx.stroke();
      }
      ctx.globalAlpha = 1;
      ctx.beginPath(); ctx.arc(cx, cy, r0 * 0.78, 0, Math.PI * 2); ctx.fillStyle = moss; ctx.fill();
      // eyes: two small calm marks that follow the pointer slightly
      var ex = pAmt * Math.cos(pa) * r0 * 0.08, ey = pAmt * Math.sin(pa) * r0 * 0.08;
      ctx.fillStyle = night;
      ctx.beginPath(); ctx.ellipse(cx - r0 * 0.26 + ex, cy - r0 * 0.04 + ey, r0 * 0.07, r0 * 0.035, 0, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.ellipse(cx + r0 * 0.26 + ex, cy - r0 * 0.04 + ey, r0 * 0.07, r0 * 0.035, 0, 0, Math.PI * 2); ctx.fill();
      if (!reduce) raf = requestAnimationFrame(draw);
    }
    var raf = 0, visible = true;
    size();
    if (reduce) { draw(t0 + 2000); }
    else {
      raf = requestAnimationFrame(draw);
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (es) {
          es.forEach(function (e) {
            if (e.isIntersecting && !visible) { visible = true; raf = requestAnimationFrame(draw); }
            else if (!e.isIntersecting && visible) { visible = false; cancelAnimationFrame(raf); }
          });
        }).observe(panel);
      }
    }
    window.addEventListener('resize', function () { size(); if (reduce) draw(t0 + 2000); });
    panel.addEventListener('pointermove', function (e) {
      var r = panel.getBoundingClientRect(); px = e.clientX - r.left; py = e.clientY - r.top; pTarget = 1;
    });
    panel.addEventListener('pointerleave', function () { pTarget = 0; });
    panel.addEventListener('click', function () { burst = 1; });
  }

  // ---------- Perspectives filter ----------
  var filters = document.querySelector('.filters');
  if (filters) {
    filters.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      filters.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      var cat = b.getAttribute('data-cat');
      document.querySelectorAll('[data-post]').forEach(function (p) {
        p.hidden = !(cat === 'all' || p.getAttribute('data-post') === cat);
      });
    });
  }

  // ---------- Contact form ----------
  var form = document.querySelector('#enquiry');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var err = form.querySelector('.form-error');
      var name = form.querySelector('#f-name').value.trim();
      var email = form.querySelector('#f-email').value.trim();
      var msg = form.querySelector('#f-msg').value.trim();
      var problems = [];
      if (!name) problems.push('your name');
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) problems.push('a valid work email');
      if (!msg) problems.push('a line about the challenge');
      if (problems.length) {
        err.hidden = false;
        err.textContent = 'Add ' + problems.join(', ') + ' so we can get back to you.';
        return;
      }
      err.hidden = true;
      // Wire this to your form backend (Formspree, Netlify Forms, HubSpot) before launch.
      form.hidden = true;
      var done = document.querySelector('.form-done');
      done.querySelector('[data-first]').textContent = name.split(' ')[0];
      done.hidden = false;
      done.setAttribute('tabindex', '-1'); done.focus();
    });
  }
})();
