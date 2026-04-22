// oi.tax — nav dropdown toggle (only JS on the site)
(function () {
  var dd = document.querySelector('.oitax-nav-dropdown');
  if (!dd) return;
  var toggle = dd.querySelector('.oitax-nav-dropdown-toggle');
  toggle.addEventListener('click', function (e) {
    e.stopPropagation();
    dd.classList.toggle('open');
  });
  document.addEventListener('click', function () { dd.classList.remove('open'); });
})();
