/* Amami Italia — English / Italian switch.
   The Italian sits in data-it attributes written at build time, so the swap is
   one pass over the document with no request and no page reload. The choice is
   remembered per visitor. Anything without a data-it stays in English rather
   than showing a gap. */
(function () {
  "use strict";
  var KEY = "amami-lang";
  var root = document.documentElement;
  /* Pages built in one language (html[data-lang]) keep it; the EN | IT
     switch on them is a pair of links to the counterpart page, so there
     is nothing to swap here. This script now only serves any page that
     still carries buttons. data-lang-fixed */
  if (root.hasAttribute("data-lang")) return;

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function remember(lang) {
    try { localStorage.setItem(KEY, lang); } catch (e) {}
  }

  function apply(lang) {
    var it = lang === "it";
    root.setAttribute("data-lang", it ? "it" : "en");
    root.setAttribute("lang", it ? "it-IT" : "en-CA");

    var nodes = document.querySelectorAll("[data-it]");
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (!el.hasAttribute("data-en")) el.setAttribute("data-en", el.textContent);
      var next = it ? el.getAttribute("data-it") : el.getAttribute("data-en");
      if (el.textContent !== next) el.textContent = next;
    }

    var ph = document.querySelectorAll("[data-it-placeholder]");
    for (var j = 0; j < ph.length; j++) {
      var f = ph[j];
      if (!f.hasAttribute("data-en-placeholder"))
        f.setAttribute("data-en-placeholder", f.getAttribute("placeholder") || "");
      f.setAttribute("placeholder", it ? f.getAttribute("data-it-placeholder")
                                       : f.getAttribute("data-en-placeholder"));
    }

    var titleIt = root.getAttribute("data-title-it");
    if (titleIt) {
      if (!root.getAttribute("data-title-en")) root.setAttribute("data-title-en", document.title);
      document.title = it ? titleIt : root.getAttribute("data-title-en");
    }

    var labels = document.querySelectorAll("[data-lang-current]");
    for (var k = 0; k < labels.length; k++) labels[k].textContent = it ? "IT" : "EN";
    try {
      document.dispatchEvent(new CustomEvent("amami:lang", { detail: { lang: lang } }));
    } catch (e) {}

    var opts = document.querySelectorAll("[data-lang-set]");
    for (var m = 0; m < opts.length; m++)
      opts[m].setAttribute("aria-current", opts[m].getAttribute("data-lang-set") === lang ? "true" : "false");
  }

  apply(stored() === "it" ? "it" : "en");

  document.addEventListener("click", function (e) {
    var btn = e.target.closest ? e.target.closest("[data-lang-set]") : null;
    if (!btn) return;
    e.preventDefault();
    var lang = btn.getAttribute("data-lang-set");
    remember(lang);
    apply(lang);
    var panel = btn.closest("details");
    if (panel) panel.open = false;
  });
})();
