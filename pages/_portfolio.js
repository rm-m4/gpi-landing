// Portfolio pages: tabs, carousels, info sheets, period chips and the TDS
// switch. Inlined by pages/_portfolio.py. Progressive enhancement throughout:
// without it the first panel of each tablist is the only one not [hidden],
// every carousel slide is reachable by scrolling, and the info buttons simply
// do nothing.
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ------------------------------------------------------------- tablists
  document.querySelectorAll('[data-pf-tabs]').forEach(function (list) {
    var tabs = [].slice.call(list.querySelectorAll('[role="tab"]'));
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute('aria-controls')); });
    var ink = list.querySelector('.pf-seg__ink');

    function moveInk(tab) {
      if (!ink) return;
      ink.style.width = tab.offsetWidth + 'px';
      ink.style.transform = 'translateX(' + tab.offsetLeft + 'px)';
      list.classList.add('is-ready');
    }
    function select(n, focus) {
      tabs.forEach(function (t, k) {
        var on = k === n;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        panels[k].hidden = !on;
        panels[k].classList.toggle('is-on', on);
      });
      moveInk(tabs[n]);
      if (focus) tabs[n].focus();
    }
    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { select(k); });
      t.addEventListener('keydown', function (e) {
        var i = { ArrowRight: (k + 1) % tabs.length, ArrowLeft: (k - 1 + tabs.length) % tabs.length,
                  Home: 0, End: tabs.length - 1 }[e.key];
        if (i === undefined) return;
        e.preventDefault();
        select(i, true);
      });
    });
    var sync = function () {
      var i = tabs.findIndex(function (t) { return t.getAttribute('aria-selected') === 'true'; });
      moveInk(tabs[Math.max(i, 0)]);
    };
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(sync);
    window.addEventListener('resize', sync);
    sync();
  });

  // ------------------------------------------------------------ carousels
  document.querySelectorAll('[data-pf-carousel]').forEach(function (box) {
    var track = box.querySelector('.pf-track');
    var slides = [].slice.call(track.children);
    var dots = [].slice.call(box.querySelectorAll('.pf-dots button'));
    var current = 0, timer = null;

    function mark(n) {
      current = n;
      dots.forEach(function (d, k) { d.setAttribute('aria-current', String(k === n)); });
      slides.forEach(function (s, k) { s.classList.toggle('is-on', k === n); });
    }
    function go(n) {
      track.scrollTo({ left: slides[n].offsetLeft - track.offsetLeft, behavior: reduce ? 'auto' : 'smooth' });
      mark(n);
    }
    dots.forEach(function (d, k) { d.addEventListener('click', function () { go(k); restart(); }); });
    var raf = 0;
    track.addEventListener('scroll', function () {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(function () {
        var n = Math.round(track.scrollLeft / Math.max(track.clientWidth, 1));
        if (n !== current && slides[n]) mark(n);
      });
    }, { passive: true });

    // The achievement strip turns on its own; hover, focus or a hidden tab pause it.
    function restart() {
      if (!box.hasAttribute('data-auto') || reduce) return;
      clearInterval(timer);
      timer = setInterval(function () {
        if (document.hidden || box.matches(':hover, :focus-within')) return;
        go((current + 1) % slides.length);
      }, 4500);
    }
    mark(0);
    restart();
  });

  // Each gold card catches the light once, the first time it is seen.
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-lit'); io.unobserve(e.target); }
      });
    }, { threshold: 0.6 });
    document.querySelectorAll('.pf-gcard').forEach(function (c) { io.observe(c); });
  }

  // ---------------------------------------------------------------- sheets
  document.addEventListener('click', function (e) {
    var open = e.target.closest('[data-sheet]');
    if (open) {
      var d = document.getElementById(open.getAttribute('data-sheet'));
      if (d && d.showModal) { d.showModal(); }
      return;
    }
    if (e.target.closest('[data-close]')) { e.target.closest('dialog').close(); return; }
    // A click on the backdrop lands on the dialog element itself.
    if (e.target.tagName === 'DIALOG') e.target.close();
  });

  // ------------------------------------------------------- chips, switch
  document.querySelectorAll('.pf-chips').forEach(function (group) {
    group.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      group.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
    });
  });
  document.querySelectorAll('.pf-switch').forEach(function (s) {
    s.addEventListener('click', function () {
      var on = s.getAttribute('aria-checked') !== 'true';
      s.setAttribute('aria-checked', String(on));
      var scope = s.closest('[data-tds]');
      if (scope) scope.setAttribute('data-tds', on ? 'on' : 'off');
    });
  });
})();
