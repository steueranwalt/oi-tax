// oi.tax — nav dropdown + hamburger menu + scroll-to-top
(function () {

  /* ── Dropdown ── */
  var dd = document.querySelector('.oitax-nav-dropdown');
  if (dd) {
    var toggle = dd.querySelector('.oitax-nav-dropdown-toggle');
    var menu = dd.querySelector('.oitax-nav-dropdown-menu');

    toggle.setAttribute('aria-haspopup', 'true');
    toggle.setAttribute('aria-expanded', 'false');
    if (menu) menu.setAttribute('aria-hidden', 'true');

    function openDropdown() {
      dd.classList.add('open');
      toggle.setAttribute('aria-expanded', 'true');
      if (menu) menu.setAttribute('aria-hidden', 'false');
    }
    function closeDropdown() {
      dd.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      if (menu) menu.setAttribute('aria-hidden', 'true');
    }

    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      dd.classList.contains('open') ? closeDropdown() : openDropdown();
    });

    document.addEventListener('click', function () { closeDropdown(); });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && dd.classList.contains('open')) {
        closeDropdown();
        toggle.focus();
      }
    });
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

  /* ── Active page state ── */
  var currentPath = window.location.pathname.replace(/\/+$/, '') || '/';
  var navLinks = document.querySelectorAll('.site-header nav a, .oitax-nav-dropdown-menu a');
  navLinks.forEach(function (link) {
    var href = link.getAttribute('href');
    if (!href) return;
    try {
      var linkPath = new URL(href, window.location.href).pathname.replace(/\/+$/, '') || '/';
      if (linkPath === currentPath) link.setAttribute('aria-current', 'page');
    } catch (e) {}
  });

  /* ── Language switch labels ── */
  var langLinks = document.querySelectorAll('.site-header nav a[href="index.html"], .site-header nav a[href="/"], .site-header nav a[href="en.html"], .site-header nav a[href="/en.html"]');
  langLinks.forEach(function (link) {
    var text = link.textContent.trim();
    if (text === 'DE') link.setAttribute('title', 'Zur deutschen Version wechseln');
    if (text === 'EN') link.setAttribute('title', 'Switch to English version');
  });

  /* ── Compact header on scroll ── */
  var header = document.querySelector('.site-header');
  if (header) {
    function updateHeader() {
      header.classList.toggle('site-header--compact', window.scrollY > 80);
    }
    window.addEventListener('scroll', updateHeader, { passive: true });
    updateHeader();
  }

  /* ── Scroll-to-top button ── */
  var scrollBtn = document.createElement('button');
  scrollBtn.setAttribute('aria-label', 'Zurück nach oben');
  scrollBtn.className = 'oitax-scroll-top';
  scrollBtn.innerHTML = '↑';
  document.body.appendChild(scrollBtn);

  function updateScrollBtn() {
    scrollBtn.classList.toggle('oitax-scroll-top--visible', window.scrollY > 200);
  }
  window.addEventListener('scroll', updateScrollBtn, { passive: true });
  updateScrollBtn();

  scrollBtn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

})();
