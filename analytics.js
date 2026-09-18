// Beltstra Co, the five funnel numbers (9/18).
//
// Paste the PostHog project key between the quotes below and this page starts sending hero_cta_click to
// PostHog. Leave it empty and nothing is loaded and nothing is sent from here. Either way the app records
// all five events on its own side (hero_cta_click when the button lands on /try/page, then
// anon_scan_started, anon_scan_result_shown, save_prompt_shown and signup_completed), so the numbers exist
// without PostHog. The app reads its own key from the POSTHOG_KEY environment variable on the server.
var POSTHOG_KEY = "";

(function () {
  if (POSTHOG_KEY) {
    var s = document.createElement("script");
    s.src = "https://us-assets.i.posthog.com/static/array.js";
    s.onload = function () {
      try { posthog.init(POSTHOG_KEY, {api_host: "https://us.i.posthog.com"}); } catch (e) {}
    };
    document.head.appendChild(s);
  }
  // Both green buttons carry the same event; the link itself tells the app which one was tapped (?src=).
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest("a[data-ev]") : null;
    if (!a) return;
    try {
      if (window.posthog && posthog.capture) posthog.capture("hero_cta_click", {source: a.getAttribute("data-ev")});
    } catch (err) {}
  });
})();
