// oi.tax — email obfuscation + Teams link decoder + TP-Schnellcheck form
(function () {

  // Email obfuscation
  document.querySelectorAll('a[data-m]').forEach(function (a) {
    try {
      var email = atob(a.dataset.m);
      a.href = 'mailto:' + email;
      if (a.dataset.show) { a.textContent = email; }
    } catch (e) {}
  });

  // Teams link obfuscation
  document.querySelectorAll('a[data-href-b64]').forEach(function (a) {
    try { a.href = atob(a.dataset.hrefB64); } catch (e) {}
  });

  // TP-Schnellcheck — mailto-based form handler
  var scBtn = document.getElementById('sc-submit');
  if (scBtn) {
    scBtn.addEventListener('click', function () {
      var name  = (document.getElementById('sc-name').value  || '').trim();
      var email = (document.getElementById('sc-email').value || '').trim();
      var sorge = (document.getElementById('sc-sorge') ? document.getElementById('sc-sorge').value : '').trim();
      var to      = atob('emhAc3RldWVyYW53YWx0c2thbnpsZWkuY29t');
      var subject = encodeURIComponent('TP-Schnellcheck DE/CH');
      var body    = encodeURIComponent(
        (name  ? 'Name: '   + name  + '\n' : '') +
        (email ? 'E-Mail: ' + email + '\n' : '') +
        (sorge ? '\nVP-Sorge:\n' + sorge    : '')
      );
      window.location.href = 'mailto:' + to + '?subject=' + subject + '&body=' + body;
    });
  }

}());
