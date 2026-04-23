// oi.tax — nav dropdown + hamburger menu + scroll-to-section
(function () {

  /* ── Dropdown ── */
  var dd = document.querySelector('.oitax-nav-dropdown');
  if (dd) {
    var toggle = dd.querySelector('.oitax-nav-dropdown-toggle');
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      dd.classList.toggle('open');
    });
    document.addEventListener('click', function () { dd.classList.remove('open'); });
  }

  /* ── Hamburger menu (mobile) ── */
  var headerContainer = document.querySelector('.site-header .oitax-container');
  var nav = headerContainer && headerContainer.querySelector('nav');
  if (headerContainer && nav) {
    var hbtn = document.createElement('button');
    hbtn.className = 'oitax-hamburger';
    hbtn.setAttribute('type', 'button');
    hbtn.setAttribute('aria-label', 'Menü öffnen');
    hbtn.innerHTML = '<span></span><span></span><span></span>';
    headerContainer.appendChild(hbtn);

    hbtn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = nav.classList.toggle('oitax-nav-open');
      hbtn.classList.toggle('oitax-hamburger--open', open);
      hbtn.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü öffnen');
    });

    document.addEventListener('click', function (e) {
      if (!headerContainer.contains(e.target)) {
        nav.classList.remove('oitax-nav-open');
        hbtn.classList.remove('oitax-hamburger--open');
      }
    });
  }

  /* ── Scroll to previous section ── */
  var scrollBtn = document.createElement('button');
  scrollBtn.setAttribute('aria-label', 'Zum vorherigen Abschnitt');
  scrollBtn.className = 'oitax-scroll-top';
  scrollBtn.innerHTML = '↑';
  document.body.appendChild(scrollBtn);

  var sections = Array.from(document.querySelectorAll('.oitax-hero, .oitax-section'));

  function updateScrollBtn() {
    scrollBtn.classList.toggle('oitax-scroll-top--visible', window.scrollY > 200);
  }
  window.addEventListener('scroll', updateScrollBtn, { passive: true });
  updateScrollBtn();

  scrollBtn.addEventListener('click', function () {
    var current = window.scrollY;
    var target = null;
    for (var i = sections.length - 1; i >= 0; i--) {
      var top = sections[i].getBoundingClientRect().top + current;
      if (top < current - 10) { target = top; break; }
    }
    window.scrollTo({ top: target !== null ? target : 0, behavior: 'smooth' });
  });

})();
