// Discover Bonds: filter and sort the snapshot, as the live page does against
// its API. Each row lists the filter options it matches in data-f; within a
// group any ticked option may match, across groups all must. Options marked
// data-wired="false" need data the snapshot lacks, so they count and chip but
// do not narrow the list. Without this script every row still shows.
(function () {
  var form = document.querySelector('[data-filters]');
  var list = document.querySelector('[data-rows]');
  if (!form || !list) return;
  var rows = [].slice.call(list.children);
  var sorts = [].slice.call(document.querySelectorAll('[data-sort]'));
  var chips = document.querySelector('[data-chips]');
  var clear = document.querySelector('[data-clear]');
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Sort value -> [row attribute, direction]. Ties keep the captured order.
  var KEYS = {
    'investment-high-to-low': ['min', -1], 'investment-low-to-high': ['min', 1],
    'safety-high-to-low': ['safety', -1], 'safety-low-to-high': ['safety', 1],
    'yield-high-to-low': ['yield', -1], 'yield-low-to-high': ['yield', 1],
    'tenure-high-to-low': ['tenure', -1], 'tenure-low-to-high': ['tenure', 1]
  };

  function ticked() { return [].slice.call(form.querySelectorAll('input:checked')); }

  function apply() {
    var on = ticked();
    var groups = {};
    on.forEach(function (i) {
      if (i.dataset.wired === 'false') return;
      (groups[i.name] = groups[i.name] || []).push(i.value);
    });
    var names = Object.keys(groups);
    var k = sorts[0].value in KEYS ? KEYS[sorts[0].value] : KEYS['yield-high-to-low'];
    var shown = rows.filter(function (r) {
      var f = ' ' + r.dataset.f + ' ';
      var ok = names.every(function (n) {
        return groups[n].some(function (v) { return f.indexOf(' ' + v + ' ') > -1; });
      });
      r.hidden = !ok;
      return ok;
    });
    rows.slice().sort(function (a, b) {
      return (a.dataset[k[0]] - b.dataset[k[0]]) * k[1] || a.dataset.i - b.dataset.i;
    }).forEach(function (r) { list.appendChild(r); });
    // Restagger the rows that are showing, so a change reads as a new list.
    shown.forEach(function (r, n) { r.style.setProperty('--r', Math.min(n, 11)); });
    if (!still) {
      list.classList.remove('is-fresh');
      void list.offsetWidth;
      list.classList.add('is-fresh');
    }

    document.querySelector('[data-count]').textContent = shown.length;
    document.querySelector('[data-empty]').hidden = shown.length > 0;
    list.hidden = shown.length === 0;
    document.querySelector('[data-applied]').textContent = on.length;
    var badge = document.querySelector('[data-applied-badge]');
    badge.textContent = on.length;
    badge.hidden = !on.length;
    clear.hidden = !on.length;
    chips.innerHTML = '';
    on.forEach(function (i) {
      var li = document.createElement('li');
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', 'Remove filter: ' + i.dataset.chip);
      b.innerHTML = '<span></span><span aria-hidden="true">&times;</span>';
      b.firstChild.textContent = i.dataset.chip;
      b.addEventListener('click', function () { i.checked = false; apply(); });
      li.appendChild(b);
      chips.appendChild(li);
    });
  }

  form.addEventListener('change', apply);
  sorts.forEach(function (s) {
    s.addEventListener('change', function () {
      sorts.forEach(function (o) { o.value = s.value; });
      apply();
    });
  });
  function reset() { form.reset(); apply(); }
  clear.addEventListener('click', reset);
  document.querySelector('[data-clear-sheet]').addEventListener('click', reset);

  // More Filters: the last eleven groups.
  var more = document.querySelector('[data-more]');
  more.addEventListener('click', function () {
    var open = more.getAttribute('aria-expanded') !== 'true';
    more.setAttribute('aria-expanded', String(open));
    document.getElementById('lv-more').hidden = !open;
    more.firstElementChild.textContent = open ? '−' : '+';
    more.lastElementChild.textContent = open ? more.dataset.lessText : more.dataset.moreText;
  });

  // Phones: the sidebar is a sheet opened from the bar.
  var sheet = document.getElementById('lv-filters');
  var opener = document.querySelector('[data-open-filters]');
  var scrim = document.querySelector('.gp-lv__scrim');
  function setSheet(open) {
    sheet.classList.toggle('is-open', open);
    scrim.hidden = !open;
    opener.setAttribute('aria-expanded', String(open));
    document.documentElement.classList.toggle('gp-lv-locked', open);
    if (open) sheet.querySelector('summary').focus();
    else opener.focus();
  }
  opener.addEventListener('click', function () { setSheet(true); });
  [].forEach.call(document.querySelectorAll('[data-close-filters]'), function (b) {
    b.addEventListener('click', function () { setSheet(false); });
  });
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape' && sheet.classList.contains('is-open')) setSheet(false);
  });
})();
