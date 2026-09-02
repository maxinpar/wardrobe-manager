/* Collapsing a category section in the fits grid.

   The sections themselves are built on the server, in the authored order, so
   the page arrives correct and complete. This adds one thing: a header you can
   press to fold its cards away, and the memory of which ones you folded.

   Keyed by LABEL rather than by category code, because that is what the user
   sees and because the trailing "Not in a category yet" section has no code.
   Kept in sessionStorage for the same reason the layer switch is: which
   sections you have folded is view state, and it does not deserve to outlive
   the tab.

   Without this file every section renders open, which is the honest default —
   nothing in the grid is hidden by a script that failed to load. */

(function () {
  "use strict";

  var KEY = "wardrobe.sectionsClosed";

  function read() {
    try {
      return JSON.parse(window.sessionStorage.getItem(KEY) || "{}");
    } catch (e) {
      return {};
    }
  }

  function write(state) {
    try {
      window.sessionStorage.setItem(KEY, JSON.stringify(state));
    } catch (e) {
      /* Fold away, just not durably. */
    }
  }

  var headers = document.querySelectorAll("[data-section]");
  if (!headers.length) return;

  var closed = read();

  function cardsIn(label) {
    var out = [];
    var all = document.querySelectorAll("[data-in-section]");
    for (var i = 0; i < all.length; i++) {
      if (all[i].getAttribute("data-in-section") === label) out.push(all[i]);
    }
    return out;
  }

  function apply(header, isClosed) {
    var label = header.getAttribute("data-section");
    header.setAttribute("aria-expanded", isClosed ? "false" : "true");
    var mark = header.querySelector(".fit-section-mark");
    if (mark) mark.textContent = isClosed ? "+" : "–";

    var cards = cardsIn(label);
    for (var i = 0; i < cards.length; i++) cards[i].hidden = isClosed;
  }

  for (var i = 0; i < headers.length; i++) {
    var header = headers[i];
    if (closed[header.getAttribute("data-section")]) apply(header, true);

    header.addEventListener("click", function () {
      var label = this.getAttribute("data-section");
      var next = !closed[label];
      if (next) closed[label] = true;
      else delete closed[label];   // open is the default; don't store it
      write(closed);
      apply(this, next);
    });
  }
})();
