// oi.tax — email obfuscation + Teams link decoder
(function () {
  // Decode mailto links: <a data-m="base64email" ...>
  document.querySelectorAll('a[data-m]').forEach(function (a) {
    try {
      var email = atob(a.dataset.m);
      a.href = 'mailto:' + email;
      // data-show: render email as visible link text (Impressum / Datenschutz)
      if (a.dataset.show) {
        a.textContent = email;
      }
    } catch (e) {}
  });

  // Decode Teams chat links: <a data-href-b64="base64url" ...>
  document.querySelectorAll('a[data-href-b64]').forEach(function (a) {
    try {
      a.href = atob(a.dataset.hrefB64);
    } catch (e) {}
  });
}());
