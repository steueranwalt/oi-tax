/* oi.tax — GA4 event tracking
   Events: generate_lead | nav_click | scroll_depth | time_on_page | internal_nav | quick_exit
   Reference: /docs/ga4-events.html
*/
(function () {
  /* --- Consent banner --- */
  window.oiGrantConsent = function () {
    localStorage.setItem('oi_consent', 'granted');
    gtag('consent', 'update', { analytics_storage: 'granted' });
    document.getElementById('oi-consent').style.display = 'none';
  };
  window.oiDenyConsent = function () {
    localStorage.setItem('oi_consent', 'denied');
    document.getElementById('oi-consent').style.display = 'none';
  };
  if (!localStorage.getItem('oi_consent')) {
    var banner = document.getElementById('oi-consent');
    if (banner) banner.style.display = 'flex';
  }

  /* --- generate_lead: IncaMail / phone clicks --- */
  document.querySelectorAll('a[data-lead]').forEach(function (a) {
    a.addEventListener('click', function () {
      gtag('event', 'generate_lead', { method: a.dataset.lead });
    });
  });

  /* --- nav_click: header + footer navigation --- */
  document.querySelectorAll('nav a').forEach(function (a) {
    a.addEventListener('click', function () {
      var inFooter = !!a.closest('footer') ||
        (a.closest('nav') && a.closest('nav').classList.contains('oitax-footer-nav'));
      gtag('event', 'nav_click', {
        link_text: a.textContent.trim().slice(0, 60),
        link_destination: a.getAttribute('href'),
        nav_location: inFooter ? 'footer' : 'header',
      });
    });
  });

  var path = location.pathname;

  /* --- scroll_depth: 25 / 50 / 75 / 100 % --- */
  var marks = { 25: false, 50: false, 75: false, 100: false };
  window.addEventListener('scroll', function () {
    var pct = (window.scrollY + window.innerHeight) / document.documentElement.scrollHeight * 100;
    [25, 50, 75, 100].forEach(function (m) {
      if (!marks[m] && pct >= m) {
        marks[m] = true;
        gtag('event', 'scroll_depth', { depth: m, page: path });
      }
    });
  }, { passive: true });

  /* --- time_on_page: 30 / 60 / 120 seconds active --- */
  [30, 60, 120].forEach(function (s) {
    setTimeout(function () {
      gtag('event', 'time_on_page', { seconds: s, page: path });
    }, s * 1000);
  });

  /* --- internal_nav: body links (excluding nav and lead links) --- */
  document.querySelectorAll('a[href^="/"], a[href^="./"], a[href$=".html"]').forEach(function (a) {
    if (!a.dataset.lead && !a.closest('nav')) {
      a.addEventListener('click', function () {
        gtag('event', 'internal_nav', { destination: a.getAttribute('href') });
      });
    }
  });

  /* --- quick_exit: organic visitor, no interaction within 15 s --- */
  if (/google\.|bing\./.test(document.referrer)) {
    var engaged = false;
    ['scroll', 'click', 'keydown'].forEach(function (ev) {
      document.addEventListener(ev, function () { engaged = true; }, { once: true, passive: true });
    });
    setTimeout(function () {
      if (!engaged) gtag('event', 'quick_exit', { page: path });
    }, 15000);
  }
}());
