// Profile pages: the sidebar swaps panels, addressed by hash so each section
// can be linked (profile.html#orders). Inlined by pages/_profile.py after
// _portfolio.js, which drives the order tabs and the nominee sheet.
// Progressive enhancement: without it every panel is on the page in order and
// the sidebar links jump to them.
(function () {
  var root = document.querySelector('[data-profile]');
  if (!root) return;
  var links = [].slice.call(root.querySelectorAll('.pr-nav a[href^="#"]'));
  var panels = [].slice.call(root.querySelectorAll('[data-panel]'));
  root.classList.add('is-js');

  function show() {
    var id = location.hash.slice(1);
    var panel = panels.filter(function (p) { return p.id === id; })[0];
    // Phones open on the menu and step into a section, as the mobile frames
    // do; from 1024px the menu and a panel sit side by side.
    root.setAttribute('data-view', panel ? 'panel' : 'menu');
    panel = panel || panels[0];
    panels.forEach(function (p) { p.hidden = p !== panel; });
    links.forEach(function (a) {
      if (a.hash === '#' + panel.id) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
  }

  function go(hash) {
    history.pushState(null, '', hash || location.pathname + location.search);
    show();
    if (window.matchMedia('(max-width: 1023px)').matches) window.scrollTo(0, 0);
  }

  root.addEventListener('click', function (e) {
    var link = e.target.closest('.pr-nav a[href^="#"]');
    if (link) { e.preventDefault(); go(link.hash); return; }
    if (e.target.closest('.pr-back')) { e.preventDefault(); go(''); return; }

    var copy = e.target.closest('[data-copy]');
    if (copy && navigator.clipboard) {
      navigator.clipboard.writeText(copy.getAttribute('data-copy')).then(function () {
        var label = copy.getAttribute('aria-label');
        copy.classList.add('is-copied');
        copy.setAttribute('aria-label', 'Copied');
        setTimeout(function () { copy.classList.remove('is-copied'); copy.setAttribute('aria-label', label); }, 1600);
      });
    }
  });

  window.addEventListener('popstate', show);
  window.addEventListener('hashchange', show);
  show();
})();
