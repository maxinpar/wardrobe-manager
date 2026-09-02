/* Coming back from a modal should land you where you left.

   Opening a garment or a fit is a navigation, not a script — that is what
   makes the back button, the backdrop and a middle-click all work with no JS
   in the path. The cost is that closing one loads the grid again, and a fresh
   load starts at the top: a garment picked from halfway down the closet threw
   the page back to the first row every time you shut it.

   So: when a click is about to open a modal, remember where the grid was, and
   put it back on the way through and on the way out. Keyed by the page and its
   filters, because a different filter set is a different grid and a position
   from another one means nothing. Kept in sessionStorage, like the folded
   sections and the layer switch — view state for one trip, not a preference —
   and spent on arrival, so it can only ever apply to the return journey it was
   saved for. Clicking "Closet" in the topbar still lands at the top, which is
   what pressing a nav tab is asking for.

   Without this file every load starts at the top, which is where the app was
   before it: nothing here is load-bearing. */

(function () {
  "use strict";

  var KEY = "wardrobe.gridScroll";

  /* The params that draw something over a grid. The grid underneath is the
     same page, so they are left out of its key. */
  var OVERLAY = ["item", "fit", "build"];

  function url(href) {
    try {
      return new URL(href, window.location.href);
    } catch (e) {
      return null;
    }
  }

  function overlays(u) {
    for (var i = 0; i < OVERLAY.length; i++) {
      if (u.searchParams.has(OVERLAY[i])) return true;
    }
    return false;
  }

  /* The endpoint rather than the path: /closet and /catalogue are one page,
     and a key that cannot tell them apart is one less way to lose the
     position. Falls back to the path if the attribute ever goes missing. */
  function pageKey(u) {
    var params = u.searchParams;
    for (var i = 0; i < OVERLAY.length; i++) params.delete(OVERLAY[i]);
    if (params.sort) params.sort();
    var page = document.body.getAttribute("data-page") || u.pathname;
    return page + "?" + params.toString();
  }

  function read() {
    try {
      return JSON.parse(window.sessionStorage.getItem(KEY) || "null");
    } catch (e) {
      return null;
    }
  }

  function write(rec) {
    try {
      if (rec) window.sessionStorage.setItem(KEY, JSON.stringify(rec));
      else window.sessionStorage.removeItem(KEY);
    } catch (e) {
      /* Land at the top, then. */
    }
  }

  function scrolled() {
    return window.scrollY || document.documentElement.scrollTop || 0;
  }

  var here = url(window.location.href);
  if (!here) return;
  var openHere = overlays(here);
  var key = pageKey(here);

  /* Save on the way out, not on unload: only a click that opens a modal is
     worth remembering, and at that moment we can still see where it points. */
  document.addEventListener("click", function (e) {
    if (e.defaultPrevented || e.button !== 0) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest ? e.target.closest("a[href]") : null;
    if (!a || a.target) return;
    var to = url(a.getAttribute("href"));
    if (!to || to.origin !== window.location.origin || !overlays(to)) return;
    var y = scrolled();
    write(y > 0 ? { key: key, y: y } : null);
  });

  var rec = read();
  if (!rec || rec.key !== key) return;

  /* On a grid, only when you have just come back off one of its modals. A
     fresh visit through the nav is not a return trip. */
  if (!openHere) {
    var from = document.referrer ? url(document.referrer) : null;
    if (!from || from.origin !== window.location.origin || !overlays(from)) return;
    write(null);   /* spent: this was the journey it was saved for */
  }

  window.scrollTo(0, rec.y);
  /* Every tile has a fixed aspect ratio, so the page is already its full
     height with the images still loading. If the position was out of reach
     anyway, something below is still growing — try again once it has. */
  if (scrolled() < rec.y - 2) {
    window.addEventListener("load", function () {
      window.scrollTo(0, rec.y);
    });
  }
})();
