// oi.tax — nav dropdown toggle + scroll-to-top
(function () {
  var dd = document.querySelector('.oitax-nav-dropdown');
  if (dd) {
    var toggle = dd.querySelector('.oitax-nav-dropdown-toggle');
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      dd.classList.toggle('open');
    });
    document.addEventListener('click', function () { dd.classList.remove('open'); });
  }

  var btn = document.createElement('button');
  btn.setAttribute('aria-label', 'Nach oben');
  btn.className = 'oitax-scroll-top';
  btn.innerHTML = '↑';
  document.body.appendChild(btn);

  window.addEventListener('scroll', function () {
    btn.classList.toggle('oitax-scroll-top--visible', window.scrollY > 400);
  }, { passive: true });

  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();
