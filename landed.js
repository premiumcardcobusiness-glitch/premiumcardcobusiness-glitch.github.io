// linknames1112 (Kenny's 30 Day Exit Plan, build 6): a visitor who lands on this site by a link that says where she came
// from (the Facebook page's own button is beltstra.com/?utm_source=facebook&utm_medium=page; a post's ?src=fb) tells the
// app so with a picture of nothing, the way try.html does, so "Where people come from" counts her under that link and
// her sign-up after says it too. Only the link's own tag, the site's name and its medium go along, cleaned; nothing else
// of the address, and nothing is stored here. A visit with no tag asks for nothing.
(function () {
  var APP = "https://app.beltstra.com";
  function arg(name, bad, max) {
    var m = new RegExp("[?&]" + name + "=([^&#]*)", "i").exec(location.search), v;
    if (!m) return "";
    try { v = decodeURIComponent(m[1].replace(/\+/g, " ")); } catch (e) { v = m[1]; }
    return v.toLowerCase().replace(bad, "").slice(0, max);
  }
  var src = arg("src", /[^a-z0-9_-]/g, 24), utm = arg("utm_source", /[^a-z0-9._-]/g, 32),
      med = arg("utm_medium", /[^a-z0-9._-]/g, 16), tail = [];
  if (!src && !utm) return;
  if (src) tail.push("src=" + encodeURIComponent(src));
  if (utm) tail.push("utm_source=" + encodeURIComponent(utm));
  if (utm && med) tail.push("utm_medium=" + encodeURIComponent(med));
  try { new Image().src = APP + "/api/landed?" + tail.join("&") + "&cb=" + Date.now(); } catch (e) {}
})();
