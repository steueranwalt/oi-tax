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
  btn.setAttribute('aria-label', 'Zum vorherigen Abschnitt');
  btn.className = 'oitax-scroll-top';
  btn.innerHTML = '↑';
  document.body.appendChild(btn);

  var sections = Array.from(document.querySelectorAll('.oitax-hero, .oitax-section'));

  function update() {
    btn.classList.toggle('oitax-scroll-top--visible', window.scrollY > 200);
  }
  window.addEventListener('scroll', update, { passive: true });
  update();

  btn.addEventListener('click', function () {
    var current = window.scrollY;
    // find the section whose top is above current scroll position
    var target = null;
    for (var i = sections.length - 1; i >= 0; i--) {
      var top = sections[i].getBoundingClientRect().top + current;
      if (top < current - 10) { target = top; break; }
    }
    window.scrollTo({ top: target !== null ? target : 0, behavior: 'smooth' });
  });
})();
