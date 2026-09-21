/* Amami Italia — shared behaviour for the new templates.
   Deliberately small and dependency-free: the pages are static HTML and the
   old WordPress capture already loads more JavaScript than this site needs. */
(function () {
  "use strict";

  /* ---- full-screen navigation overlay ---- */
  var overlay = document.querySelector("[data-nav-overlay]");
  var openers = document.querySelectorAll("[data-nav-open]");
  var closers = document.querySelectorAll("[data-nav-close]");
  var lastFocus = null;

  function setNav(open) {
    if (!overlay) return;
    overlay.setAttribute("data-open", open ? "true" : "false");
    overlay.setAttribute("aria-hidden", open ? "false" : "true");
    document.documentElement.style.overflow = open ? "hidden" : "";
    if (open) {
      lastFocus = document.activeElement;
      var first = overlay.querySelector("a, button");
      if (first) first.focus();
    } else if (lastFocus) {
      lastFocus.focus();
    }
  }
  openers.forEach(function (b) { b.addEventListener("click", function () { setNav(true); }); });
  closers.forEach(function (b) { b.addEventListener("click", function () { setNav(false); }); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && overlay && overlay.getAttribute("data-open") === "true") setNav(false);
  });

  /* ---- today's hours status (spec 5.1) ----
     ONE SOURCE. The hours live in data-hours on <body> as a JSON map of
     weekday -> [openHour, closeHour] in 24h local time, so the header, the
     footer and the Visit page cannot drift apart. Closed days are null. A day
     with a break is a list of ranges, [[12,15],[17,22]]; a close of null
     means "open from 12, close not stated" (Friday and Saturday run late and
     no closing hour has been confirmed — TODO(hours)). */
  var body = document.body;
  var statusEls = document.querySelectorAll("[data-hours-status]");

  /* The status line is written at runtime, so it cannot be annotated at build
     time like the rest of the copy. It renders in whichever language is
     current, and re-renders when the switch fires. */
  var WORDS = {
    en: { closedNext: "Closed today — open %s from %s", closed: "Closed today",
          openUntil: "Open today until %s", opensAt: "Opens today at %s",
          openFrom: "Open today from %s", shut: "Closed for tonight",
          days: { sun: "Sunday", mon: "Monday", tue: "Tuesday", wed: "Wednesday",
                  thu: "Thursday", fri: "Friday", sat: "Saturday" } },
    it: { closedNext: "Oggi chiuso — apre %s dalle %s", closed: "Oggi chiuso",
          openUntil: "Oggi aperto fino alle %s", opensAt: "Oggi apre alle %s",
          openFrom: "Oggi aperto dalle %s", shut: "Chiuso per stasera",
          days: { sun: "domenica", mon: "lunedì", tue: "martedì", wed: "mercoledì",
                  thu: "giovedì", fri: "venerdì", sat: "sabato" } }
  };

  function renderHours() {
    if (!statusEls.length || !body.getAttribute("data-hours")) return;
    var hours;
    try { hours = JSON.parse(body.getAttribute("data-hours")); } catch (err) { return; }
    if (!hours) return;
    var lang = document.documentElement.getAttribute("data-lang") === "it" ? "it" : "en";
    var w = WORDS[lang];
    var names = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
    var now = new Date();
    var today = hours[names[now.getDay()]];
    var text;
    if (!today) {
      var nextName = null;
      for (var i = 1; i <= 7; i++) {
        var cand = names[(now.getDay() + i) % 7];
        if (hours[cand]) { nextName = cand; break; }
      }
      text = nextName
        ? w.closedNext.replace("%s", w.days[nextName]).replace("%s", fmt(ranges(hours[nextName])[0][0], lang))
        : w.closed;
    } else {
      var h = now.getHours() + now.getMinutes() / 60, rs = ranges(today), cur = null, next = null;
      rs.forEach(function (r) {
        if (h >= r[0] && (r[1] === null || h < r[1])) cur = r;
        else if (h < r[0] && !next) next = r;
      });
      text = cur
        ? (cur[1] === null ? w.openFrom.replace("%s", fmt(cur[0], lang)) : w.openUntil.replace("%s", fmt(cur[1], lang)))
        : (next ? w.opensAt.replace("%s", fmt(next[0], lang)) : w.shut);
    }
    statusEls.forEach(function (el) { el.textContent = text; });
  }
  renderHours();
  document.addEventListener("amami:lang", renderHours);

  function ranges(day) { return Array.isArray(day[0]) ? day : [day]; }
  function fmt(h, lang) {
    var hr = Math.floor(h), m = Math.round((h - hr) * 60);
    var mins = m ? ":" + String(m).padStart(2, "0") : "";
    /* Italy states the hour on a 24-hour clock and does not say am/pm. */
    if (lang === "it") return hr + mins;
    var ap = hr >= 12 ? "pm" : "am";
    return (hr % 12 === 0 ? 12 : hr % 12) + mins + ap;
  }

  /* ---- menu-hub anchor nav (spec 2.3: anchors within all menu pages) ---- */
  document.querySelectorAll("[data-anchor-nav] a").forEach(function (a) {
    a.addEventListener("click", function () {
      document.querySelectorAll("[data-anchor-nav] a").forEach(function (x) {
        x.removeAttribute("aria-current");
      });
      a.setAttribute("aria-current", "true");
    });
  });
})();

/* ------------------------------------------------------------------------
   Forms. Every form on the site posts to one Apps Script handler
   (apps-script/forms.gs). While the endpoint is empty the submit falls back
   to opening a pre-filled email, so an enquiry still reaches somebody rather
   than disappearing into action="#".
   ------------------------------------------------------------------------ */
(function () {
  var MSG = {
    en: { sending: "Sending…",
          ok: "Thanks — we’ll be in touch.",
          fail: "That didn’t send. Call 905-794-3366 and we’ll sort it.",
          mail: "Opening your email…" },
    it: { sending: "Invio…",
          ok: "Grazie — ci sentiamo presto.",
          fail: "Non è partito. Chiama il 905-794-3366 e sistemiamo.",
          mail: "Apro la tua email…" }
  };
  function t(k) {
    // the language switch sets lang="it-IT", so match the language, not the tag
    var l = /^it/i.test(document.documentElement.lang) ? "it" : "en";
    return MSG[l][k];
  }
  function say(el, text, state) {
    if (!el) return;
    el.textContent = text;
    if (state) el.setAttribute("data-state", state);
    else el.removeAttribute("data-state");
  }
  function labelFor(form, name) {
    var field = form.querySelector('[name="' + name + '"]');
    if (!field) return name;
    var lab = field.id && form.querySelector('label[for="' + field.id + '"]');
    return lab ? lab.textContent.trim() : name;
  }
  function mailtoFallback(form, fd, status) {
    var to = form.getAttribute("data-mailto") || "";
    var kind = form.getAttribute("data-amami-form") || "enquiry";
    var lines = [];
    fd.forEach(function (v, k) {
      if (!v || k === "form" || k === "page" || k === "company_website") return;
      lines.push(labelFor(form, k) + ": " + v);
    });
    say(status, t("mail"));
    window.location.href = "mailto:" + to +
      "?subject=" + encodeURIComponent("Website " + kind + " enquiry") +
      "&body=" + encodeURIComponent(lines.join("\n"));
  }

  document.querySelectorAll("form[data-amami-form]").forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var status = form.querySelector(".form-status");
      var btn = form.querySelector('button[type="submit"], button:not([type])');
      var fd = new FormData(form);
      fd.append("form", form.getAttribute("data-amami-form"));
      fd.append("page", location.pathname);

      var url = form.getAttribute("data-endpoint");
      if (!url) { mailtoFallback(form, fd, status); return; }

      if (btn) btn.disabled = true;
      say(status, t("sending"));
      fetch(url, { method: "POST", body: new URLSearchParams(fd) })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); say(status, t("ok"), "ok"); }
          else { say(status, (d && d.error) || t("fail"), "err"); }
        })
        .catch(function () { say(status, t("fail"), "err"); })
        .then(function () { if (btn) btn.disabled = false; });
    });
  });
})();

/* §4 Motion. Sections arrive once at ~20% visibility and stay; the header
   settles once the page has scrolled past the top. Nothing here changes
   layout — only classes that CSS turns into transform and opacity. The
   .motion class is added only when the browser can observe intersections
   and the visitor has not asked for reduced motion, so without either the
   page simply renders as it is. */
(function () {
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !("IntersectionObserver" in window)) return;
  var root = document.documentElement, body = document.body;
  body.classList.add("motion");
  var hero = document.querySelector(".pg-hero");
  if (hero) requestAnimationFrame(function () { hero.classList.add("is-ready"); });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
    });
  }, { threshold: 0.2, rootMargin: "0px 0px -5% 0px" });
  document.querySelectorAll("main > section").forEach(function (s) {
    // anything already on screen at load is shown at once, not animated in
    var r = s.getBoundingClientRect();
    if (r.top < innerHeight * 0.8) s.classList.add("is-in"); else io.observe(s);
  });
  var scroller = document.scrollingElement || root;
  function onScroll() { body.classList.toggle("is-scrolled", scroller.scrollTop > 24); }
  addEventListener("scroll", onScroll, { passive: true }); onScroll();
})();
