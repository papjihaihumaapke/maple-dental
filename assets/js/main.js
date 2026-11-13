/* Maple Dental Vancouver — site behaviour (no dependencies) */
(function () {
  "use strict";
  var doc = document.documentElement;
  var store = {
    get: function (k) { try { return window.sessionStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.sessionStorage.setItem(k, v); } catch (e) { /* ignore */ } }
  };

  /* Announcement bar (dismissible for the session) */
  var bar = document.querySelector("[data-announce]");
  if (bar) {
    if (store.get("md-announce-dismissed") === "1") bar.hidden = true;
    var closeBtn = bar.querySelector("[data-announce-close]");
    if (closeBtn) closeBtn.addEventListener("click", function () {
      bar.hidden = true;
      store.set("md-announce-dismissed", "1");
      setNavTop();
    });
  }

  /* Sticky header shrink */
  var header = document.querySelector(".site-header");
  var onScroll = function () { if (header) header.classList.toggle("is-scrolled", window.scrollY > 12); };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* Mobile menu */
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  function setNavTop() {
    if (!header) return;
    var r = header.getBoundingClientRect();
    doc.style.setProperty("--nav-top", Math.max(0, r.bottom) + "px");
  }
  function setMenu(open) {
    if (!toggle || !nav) return;
    setNavTop();
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    nav.classList.toggle("is-open", open);
    document.body.classList.toggle("menu-open", open);
    if (open) { var first = nav.querySelector("a"); if (first) first.focus(); }
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () { setMenu(toggle.getAttribute("aria-expanded") !== "true"); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") { setMenu(false); toggle.focus(); }
    });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    window.addEventListener("resize", function () { if (window.innerWidth > 900) setMenu(false); });
  }

  /* Accordions */
  document.querySelectorAll(".acc-trigger").forEach(function (btn) {
    var panel = document.getElementById(btn.getAttribute("aria-controls"));
    var item = btn.closest(".acc-item");
    if (!panel || !item) return;
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!open));
      item.classList.toggle("is-open", !open);
      if (open) { panel.setAttribute("inert", ""); } else { panel.removeAttribute("inert"); }
    });
    if (btn.getAttribute("aria-expanded") !== "true") panel.setAttribute("inert", "");
  });

  /* Reveal on scroll (staggered inside [data-stagger]) */
  var reveals = document.querySelectorAll(".reveal");
  document.querySelectorAll("[data-stagger]").forEach(function (group) {
    group.querySelectorAll(":scope > .reveal").forEach(function (el, i) { el.style.setProperty("--d", i * 80 + "ms"); });
  });
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-visible"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* Contact form: validation + endpoint check */
  var form = document.querySelector("[data-contact-form]");
  if (form) {
    var status = form.querySelector(".form-status");
    form.addEventListener("submit", function (e) {
      var firstInvalid = null;
      form.querySelectorAll("[required]").forEach(function (f) {
        var err = document.getElementById(f.id + "-error");
        var ok = f.type === "checkbox" ? f.checked : f.checkValidity() && f.value.trim() !== "";
        f.setAttribute("aria-invalid", ok ? "false" : "true");
        if (err) err.hidden = ok;
        if (!ok && !firstInvalid) firstInvalid = f;
      });
      if (firstInvalid) { e.preventDefault(); firstInvalid.focus(); return; }
      // Until a form endpoint is connected, do not pretend the message was sent.
      if (!form.getAttribute("action") || form.getAttribute("action") === "#") {
        e.preventDefault();
        if (status) {
          status.hidden = false;
          status.textContent = "Online messages are not connected yet. Please call (604) 261-4607 or email welcome@mapledental.info.";
          status.focus();
        }
      }
    });
  }

  /* Footer year */
  var y = document.querySelector("[data-year]");
  if (y) y.textContent = new Date().getFullYear();
})();
