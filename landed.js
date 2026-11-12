// linknames1112 (Kenny's 30 Day Exit Plan, build 6): a visitor who lands on this site by a link that says where she came
// from (the Facebook page's own button is beltstra.com/?utm_source=facebook&utm_medium=page; a post's ?src=fb) tells the
// app so with a picture of nothing, the way try.html does, so "Where people come from" counts her under that link and
// her sign-up after says it too. Only the link's own tag, the site's name and its medium go along, cleaned; nothing else
// of the address, and nothing is stored here.
// refnames1112: a link with no tag sends only the HOST of the page that sent her (l.facebook.com, www.google.com; never
// its path), or just "-" from inside a social app's own browser, so she is named by where she came from. A typed
// address, and a move between our own pages, ask for nothing.
(function () {
  var APP = "https://app.beltstra.com";
  function arg(name, bad, max) {
    var m = new RegExp("[?&]" + name + "=([^&#]*)", "i").exec(location.search), v;
    if (!m) return "";
    try { v = decodeURIComponent(m[1].replace(/\+/g, " ")); } catch (e) { v = m[1]; }
    return v.toLowerCase().replace(bad, "").slice(0, max);
  }
  var src = arg("src", /[^a-z0-9_-]/g, 24), utm = arg("utm_source", /[^a-z0-9._-]/g, 32),
      med = arg("utm_medium", /[^a-z0-9._-]/g, 16), tail = [], ref = "";
  if (!src && !utm) {
    try { ref = new URL(document.referrer).hostname.toLowerCase().replace(/[^a-z0-9.-]/g, "").slice(0, 64); } catch (e) { ref = ""; }
    if (/(^|\.)beltstra\.com$/.test(ref)) ref = "";
    if (!ref && !/FBAN\/|FBAV\/|FB_IAB\/|Instagram|Barcelona|musical_ly|TikTok|BytedanceWebview|Snapchat|Pinterest|Twitter/
        .test(navigator.userAgent || "")) return;
    tail.push("ref=" + encodeURIComponent(ref || "-"));
  }
  if (src) tail.push("src=" + encodeURIComponent(src));
  if (utm) tail.push("utm_source=" + encodeURIComponent(utm));
  if (utm && med) tail.push("utm_medium=" + encodeURIComponent(med));
  try { new Image().src = APP + "/api/landed?" + tail.join("&") + "&cb=" + Date.now(); } catch (e) {}
})();
