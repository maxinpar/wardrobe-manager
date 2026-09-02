/* The layer switch: one fit, two renders, one state.

   A golf fit built around a quarter-zip, long-sleeve or vest was rendered
   twice — without the layer and with it. The base render is the hero, because
   the rule for the batch is that the fit has to stand up without the layer, so
   "off" is always the starting state and always the picture the server sent.

   Two things this file exists for:

   1. The switch is ONE button that flips, never a segmented pair. A pair moves
      the target when you press it, so going back means chasing it.
   2. The state is shared. Flip a card, open the fit, and the pane opens
      flipped — which means the state has to survive a navigation, because
      opening a fit IS one. sessionStorage, keyed by fit id: it is view state,
      not a fact about the wardrobe, so it does not belong in Postgres and it
      does not deserve to outlive the tab.

   Without this file every switch renders in its off state showing the hero,
   which is the picture the card would have shown anyway. Nothing is hidden,
   only unswitchable. */

(function () {
  "use strict";

  var KEY = "wardrobe.layerOn";

  function read() {
    try {
      return JSON.parse(window.sessionStorage.getItem(KEY) || "{}");
    } catch (e) {
      return {};   // private mode, a full quota, a hand-edited value: start clean
    }
  }

  function write(state) {
    try {
      window.sessionStorage.setItem(KEY, JSON.stringify(state));
    } catch (e) {
      /* Degrade to this-page-only rather than throwing: the switch still works,
         it just stops travelling with you. */
    }
  }

  var state = read();

  function cssEscape(value) {
    return value.replace(/["\\]/g, "\\$&");
  }

  function switchesFor(fitId) {
    return document.querySelectorAll('[data-layer-switch="' + cssEscape(fitId) + '"]');
  }

  /* A picture belongs to a fit when it sits in the same card or pane as that
     fit's switch. The same fit can be on screen twice — a card behind an open
     modal — and one flip has to repaint both. */
  function apply(fitId, on) {
    var buttons = switchesFor(fitId);

    for (var i = 0; i < buttons.length; i++) {
      var button = buttons[i];
      button.classList.toggle("on", on);
      button.setAttribute("aria-pressed", on ? "true" : "false");
      var label = button.querySelector(".layer-label");
      if (label) label.textContent = on ? "Layer on" : "Layer off";

      var scope = button.closest(".fit-card, .look-card, .modal-figure");
      if (!scope) continue;

      var images = scope.querySelectorAll("img[data-look-layered]");
      for (var j = 0; j < images.length; j++) {
        var img = images[j];
        var src = on
          ? img.getAttribute("data-look-layered")
          : img.getAttribute("data-look-base");
        if (src && img.getAttribute("src") !== src) img.setAttribute("src", src);
      }

      var notes = scope.querySelectorAll(".layer-note");
      for (var k = 0; k < notes.length; k++) {
        var text = on
          ? notes[k].getAttribute("data-layer-note-on")
          : notes[k].getAttribute("data-layer-note-off");
        if (text) notes[k].textContent = text;
      }
    }
  }

  var switches = document.querySelectorAll("[data-layer-switch]");
  var seen = {};

  for (var i = 0; i < switches.length; i++) {
    switches[i].addEventListener("click", function (event) {
      /* The card is a link to the fit. Without this, flipping the layer opens
         the fit — which is the one thing the switch must not do. */
      event.preventDefault();
      event.stopPropagation();
      var fitId = this.getAttribute("data-layer-switch");
      state[fitId] = !state[fitId];
      if (!state[fitId]) delete state[fitId];   // off is the default; don't store it
      write(state);
      apply(fitId, !!state[fitId]);
    });

    var id = switches[i].getAttribute("data-layer-switch");
    if (!seen[id]) {
      seen[id] = true;
      if (state[id]) apply(id, true);   // arrive flipped, if that is how you left it
    }
  }
})();
