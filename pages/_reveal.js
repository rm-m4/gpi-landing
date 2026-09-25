// Scroll reveal, shared by the converted landing pages. Injected by
// pages/_convert.py and present inline in _final_shell.html.
// The .reveal-ready class is added here, so if this never runs the content
// simply stays visible rather than staying hidden.
// Scroll reveal. The .reveal-ready class is added by script, so if this never
// runs the content simply stays visible rather than staying hidden.
(function () {
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  document.documentElement.classList.add('reveal-ready');

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('is-in');
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.04 });

  document.querySelectorAll('[data-reveal]').forEach(function (el) { io.observe(el); });
})();
