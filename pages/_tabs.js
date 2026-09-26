// Shared behaviour for the converted landing pages: the category tablist
// and the milestone count-up. Injected by pages/_final.py and
// pages/_convert.py so there is one copy, not four.
// Both are progressive enhancement: without them the first panel is the
// only one not marked [hidden], and the figures already read correctly.
// Category tabs. Progressive enhancement: without this the first panel is the
// only one not marked [hidden], so the page still shows a working listing.
(function () {
  // .gp-tabs is the folder strip; .gp-pills (bond-utsav) is a pill filter
  // with no sliding indicator. Both mark their parts up by ARIA role.
  var wrap = document.querySelector('.gp-tabs, .gp-pills');
  if (!wrap) return;
  var track = wrap.querySelector('[role="tablist"]');
  var ink = wrap.querySelector('.gp-tabs__ink');
  var tabs = [].slice.call(wrap.querySelectorAll('[role="tab"]'));
  if (!track || !tabs.length) return;

  var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute('aria-controls')); });

  function moveInk(tab) {
    if (!ink) return;
    ink.style.width = tab.offsetWidth + 'px';
    ink.style.transform = 'translateX(' + tab.offsetLeft + 'px)';
    ink.classList.add('is-ready');
  }

  function select(n, focus) {
    tabs.forEach(function (t, k) {
      var on = k === n;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      panels[k].classList.toggle('is-on', on);
      if (on) { panels[k].removeAttribute('hidden'); } else { panels[k].setAttribute('hidden', ''); }
    });
    moveInk(tabs[n]);
    if (focus) tabs[n].focus();
    tabs[n].scrollIntoView({ block: 'nearest', inline: 'nearest' });
  }

  tabs.forEach(function (t, k) {
    t.addEventListener('click', function () { select(k); });
    t.addEventListener('keydown', function (e) {
      var i = null;
      if (e.key === 'ArrowRight') i = (k + 1) % tabs.length;
      else if (e.key === 'ArrowLeft') i = (k - 1 + tabs.length) % tabs.length;
      else if (e.key === 'Home') i = 0;
      else if (e.key === 'End') i = tabs.length - 1;
      if (i === null) return;
      e.preventDefault();
      select(i, true);
    });
  });

  function sync() {
    var i = tabs.findIndex(function (t) { return t.getAttribute('aria-selected') === 'true'; });
    moveInk(tabs[i < 0 ? 0 : i]);
    wrap.setAttribute('data-overflow',
      String(track.scrollWidth - track.clientWidth - track.scrollLeft > 8));
  }

  // Measure after webfonts settle, or the indicator lands short.
  if (document.fonts && document.fonts.ready) { document.fonts.ready.then(sync); }
  window.addEventListener('resize', sync);
  track.addEventListener('scroll', sync, { passive: true });
  sync();
})();

// Milestone figures count up the first time they are seen. The final value is
// already in the markup, so nothing is lost if this never runs.
(function () {
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      // Count in the text node holding the digits, so markup around it (the
      // smaller "Cr+" suffix) survives the animation.
      var el = e.target, node = null;
      for (var i = 0; i < el.childNodes.length && !node; i++) {
        var c = el.childNodes[i];
        if (c.nodeType === 3 && /\d/.test(c.nodeValue)) node = c;
      }
      if (!node) return;
      var full = node.nodeValue, m = full.match(/([\d,]+)/);
      if (!m) return;
      var target = Number(m[1].replace(/,/g, ''));
      if (!target) return;
      var t0 = null;
      function step(ts) {
        if (!t0) t0 = ts;
        var p = Math.min((ts - t0) / 1000, 1);
        node.nodeValue = full.replace(
          m[1], Math.round(target * (1 - Math.pow(1 - p, 3))).toLocaleString('en-IN'));
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }, { threshold: 0.6 });

  document.querySelectorAll('[data-count]').forEach(function (el) { io.observe(el); });
})();
