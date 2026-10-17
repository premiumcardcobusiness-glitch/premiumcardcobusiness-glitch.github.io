// J60d (Kenny's build note v3): the banner Kenny sets from the app's /ops page, shown on beltstra.com too. Reads
// https://app.beltstra.com/api/notice (public, CORS for this site); shows nothing when there is none. An info notice can
// be closed and stays closed for that message; warn and down stay. No cookies, nothing sent.
(function () {
  var KEY = 'bs.noticeSeen';
  function show(n) {
    var seen = null;
    try { seen = localStorage.getItem(KEY); } catch (e) {}
    if (!n || (n.severity === 'info' && String(n.id) === seen)) return;
    var bar = document.createElement('div');
    bar.setAttribute('role', 'status');
    var bg = n.severity === 'down' ? '#7f1d1d' : n.severity === 'warn' ? '#7a4a00' : '#262626';
    bar.style.cssText = 'background:' + bg + ';color:#fff;font:600 14px/20px system-ui,sans-serif;padding:10px 16px;display:flex;gap:12px;align-items:center;justify-content:center;flex-wrap:wrap';
    var msg = document.createElement('span');
    msg.textContent = n.message;
    bar.appendChild(msg);
    var link = document.createElement('a');
    link.href = 'status.html'; link.textContent = 'Status'; link.style.cssText = 'color:#fff;text-decoration:underline';
    bar.appendChild(link);
    if (n.severity === 'info') {
      var ok = document.createElement('button');
      ok.type = 'button'; ok.textContent = 'OK';
      ok.style.cssText = 'border:1px solid #fff;background:transparent;color:#fff;border-radius:999px;padding:4px 12px;font:inherit;min-height:32px';
      ok.onclick = function () { try { localStorage.setItem(KEY, String(n.id)); } catch (e) {} bar.remove(); };
      bar.appendChild(ok);
    }
    document.body.insertBefore(bar, document.body.firstChild);
  }
  try {
    fetch('https://app.beltstra.com/api/notice', {cache: 'no-store'}).then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) { if (d) show(d.notice); }).catch(function () {});
  } catch (e) {}
})();
