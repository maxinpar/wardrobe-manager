/* Folding sections in the fit sheet, and the scroll lock behind any overlay.
 *
 * Phone only, both of them. On a desktop the sections render flat and open in
 * CSS and this file leaves them alone — the fold is a way of making 1,800px of
 * detail navigable on a 412px screen, not a way of hiding things.
 *
 * Same ES5 idiom as the other scripts here: no framework, no build step.
 */
(function () {
  "use strict";

  var PHONE = "(max-width: 760px)";
  var STORE = "wardrobe.secOpen";

  /* Which sections Max opened, kept for the session. Not localStorage: a fold
     he opened to read one thing should not still be open next week, and the
     folded state is the one worth returning to. */
  function read() {
    try {
      return JSON.parse(window.sessionStorage.getItem(STORE) || "{}") || {};
    } catch (e) {
      return {};
    }
  }

  function write(state) {
    try {
      window.sessionStorage.setItem(STORE, JSON.stringify(state));
    } catch (e) {
      /* Private mode, or storage off. The folds still work for this page —
         they just do not travel to the next one. */
    }
  }

  var open = read();

  function phone() {
    return window.matchMedia && window.matchMedia(PHONE).matches;
  }

  function apply(section, on) {
    var body = section.querySelector(".sheet-sec-body");
    var head = section.querySelector(".sheet-sec-head");
    var mark = section.querySelector(".sheet-sec-mark");
    if (!body || !head) return;
    section.classList.toggle("open", on);
    head.setAttribute("aria-expanded", on ? "true" : "false");
    if (mark) mark.textContent = on ? "−" : "+";
  }

  var sections = [].slice.call(document.querySelectorAll(".sheet-sec"));
  if (!sections.length) return;

  sections.forEach(function (section) {
    var key = section.getAttribute("data-sec");
    var head = section.querySelector(".sheet-sec-head");
    if (!head) return;

    apply(section, !!open[key]);

    head.addEventListener("click", function (event) {
      /* Desktop headers are headings, not controls: the CSS renders every
         section open and unmarked, so a click there must do nothing rather
         than fold something that has no affordance saying it folds. */
      if (!phone()) return;
      event.preventDefault();
      var on = !section.classList.contains("open");
      if (on) open[key] = 1;
      else delete open[key];
      write(open);
      apply(section, on);
    });
  });

  /* Crossing the breakpoint with a fold closed would leave a desktop section
     collapsed with nothing to say so. CSS already forces them open; this keeps
     the marks and aria in step with it. */
  if (window.matchMedia) {
    var mq = window.matchMedia(PHONE);
    var onChange = function () {
      sections.forEach(function (section) {
        var key = section.getAttribute("data-sec");
        apply(section, phone() ? !!open[key] : true);
      });
    };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }
})();

/* ------------------------------------------------------ the scroll lock -- */
(function () {
  "use strict";

  /* With a full-screen sheet open, the page behind it keeps its own scrollbar.
     Dragging anywhere outside the sheet then scrolls 3,600px of fits grid and
     moves nothing you can see — and on a phone that is most of the screen. The
     lock goes on while any overlay is open and comes off with it. */
  var OVERLAYS = ".modal, .builder-overlay, .drawer";

  function anyOpen() {
    return !!document.querySelector(OVERLAYS);
  }

  function lock(on) {
    var html = document.documentElement;
    var body = document.body;
    if (on) {
      html.style.overflow = "hidden";
      body.style.overflow = "hidden";
    } else {
      html.style.overflow = "";
      body.style.overflow = "";
    }
  }

  lock(anyOpen());

  /* The overlays are server-rendered, so they arrive and leave with a
     navigation — except the AI builder's results, which swap in place. A
     disconnected observer on unload keeps this from outliving the page. */
  if (window.MutationObserver) {
    var observer = new MutationObserver(function () { lock(anyOpen()); });
    observer.observe(document.body, { childList: true, subtree: true });
    window.addEventListener("pagehide", function () { observer.disconnect(); });
  }
})();
