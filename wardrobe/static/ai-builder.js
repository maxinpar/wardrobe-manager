/* Ask AI — the brief, and the swap between setup and results.
 *
 * The only state here is what Max has chosen: seeds, day, occasion, sharpness,
 * note. Nothing is derived in this file and nothing is styled by it — the fits
 * come back from the server as rendered HTML, because the fit card is a Jinja
 * partial and a second copy of it in JavaScript would be free to drift.
 *
 * Same ES5 idiom as builder.js: no framework, no build step.
 */
(function () {
  "use strict";

  var root = document.getElementById("ai-builder");
  if (!root) return;

  var setup = document.getElementById("ai-setup");
  var results = document.getElementById("ai-results");
  var briefForm = document.getElementById("ai-brief");
  var search = document.getElementById("ai-search");
  var note = document.getElementById("ai-note");
  var chips = root.querySelector("[data-seed-chips]");
  var seedCount = root.querySelector("[data-seed-count]");
  var goButton = root.querySelector("[data-go]");

  var tiles = [].slice.call(root.querySelectorAll(".ai-tile"));
  var tabs = [].slice.call(root.querySelectorAll(".ai-tab"));

  var state = {
    seeds: [],
    tab: "Everything",
    day: (root.querySelector(".ai-day.on") || {}).dataset
      ? root.querySelector(".ai-day.on").dataset.day
      : "",
    occasion: "work",
    sharpness: 3,
    busy: false,
  };

  var names = {};
  tiles.forEach(function (tile) {
    names[tile.dataset.item] = tile.dataset.name;
  });

  // ------------------------------------------------------------- seeds --

  function renderSeeds() {
    chips.innerHTML = "";
    chips.hidden = state.seeds.length === 0;
    state.seeds.forEach(function (id) {
      var chip = document.createElement("button");
      chip.type = "button";
      chip.className = "ai-chip";
      chip.innerHTML = "";
      chip.appendChild(document.createTextNode(names[id] || id));
      var cross = document.createElement("span");
      cross.className = "x";
      cross.textContent = "×";
      chip.appendChild(cross);
      chip.addEventListener("click", function () { toggleSeed(id); });
      chips.appendChild(chip);
    });

    seedCount.textContent = state.seeds.length
      ? state.seeds.length + " locked in"
      : "nothing locked in";
    goButton.textContent = state.seeds.length ? "Build around these" : "Build me a fit";

    tiles.forEach(function (tile) {
      var on = state.seeds.indexOf(tile.dataset.item) !== -1;
      tile.classList.toggle("on", on);
      tile.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function toggleSeed(id) {
    var at = state.seeds.indexOf(id);
    if (at === -1) state.seeds.push(id);
    else state.seeds.splice(at, 1);
    renderSeeds();
  }

  tiles.forEach(function (tile) {
    tile.addEventListener("click", function () { toggleSeed(tile.dataset.item); });
  });

  // ------------------------------------------------- search and tabs --

  /* Tabs count what the search left, and a tab with nothing behind it hides
     itself rather than sitting there returning an empty grid. Everything never
     hides — it is how you get back. */
  function applyFilter() {
    var query = (search.value || "").trim().toLowerCase();
    var counts = {};
    var shown = 0;

    tiles.forEach(function (tile) {
      var matches = !query || tile.dataset.search.indexOf(query) !== -1;
      var tab = tile.dataset.tab;
      if (matches) counts[tab] = (counts[tab] || 0) + 1;
      var visible = matches && (state.tab === "Everything" || state.tab === tab);
      tile.hidden = !visible;
      if (visible) shown += 1;
    });

    tabs.forEach(function (tab) {
      var label = tab.dataset.tab;
      var count = label === "Everything"
        ? Object.keys(counts).reduce(function (sum, k) { return sum + counts[k]; }, 0)
        : counts[label] || 0;
      var box = tab.querySelector(".count");
      if (box) box.textContent = count;
      tab.hidden = label !== "Everything" && count === 0;
      tab.classList.toggle("on", label === state.tab);
    });

    // A search that narrows to a tab which then hides would strand the grid.
    if (state.tab !== "Everything" && !counts[state.tab]) {
      state.tab = "Everything";
      applyFilter();
      return;
    }
    root.classList.toggle("empty-search", shown === 0);
  }

  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      state.tab = tab.dataset.tab;
      applyFilter();
    });
  });
  search.addEventListener("input", applyFilter);

  // ------------------------------------------------------- the brief --

  function pick(selector, attr, key, after) {
    [].slice.call(root.querySelectorAll(selector)).forEach(function (button) {
      button.addEventListener("click", function () {
        state[key] = button.dataset[attr];
        [].slice.call(root.querySelectorAll(selector)).forEach(function (other) {
          other.classList.toggle("on", other === button);
        });
        if (after) after(button);
      });
    });
  }

  pick(".ai-day", "day", "day", function (button) {
    root.querySelector("[data-day-temp]").textContent = button.dataset.temp;
    root.querySelector("[data-day-sky]").textContent = button.dataset.sky;
  });
  pick(".ai-occ button", "occ", "occasion");

  // The dial fills up to the chosen bar rather than marking one of five: the
  // reading is "how far along", not "which segment".
  var bars = [].slice.call(root.querySelectorAll(".ai-dial-bar"));
  bars.forEach(function (bar) {
    bar.addEventListener("click", function () {
      state.sharpness = parseInt(bar.dataset.level, 10);
      bars.forEach(function (other) {
        other.classList.toggle("on", parseInt(other.dataset.level, 10) <= state.sharpness);
      });
      root.querySelector("[data-sharp-label]").textContent = bar.dataset.label;
    });
  });

  // ---------------------------------------------------------- the ask --

  function body(again) {
    var form = new FormData();
    form.append("day", state.day);
    form.append("occasion", state.occasion);
    form.append("sharpness", state.sharpness);
    form.append("note", note.value || "");
    if (again) form.append("again", "1");
    state.seeds.forEach(function (id) { form.append("seed", id); });
    return form;
  }

  function ask(again) {
    if (state.busy) return;
    state.busy = true;
    setup.hidden = true;
    results.hidden = false;
    /* Forty seconds is a long time to look at nothing, and it is the honest
       number — the wait is the model thinking, not the network. Saying so beats
       a spinner that implies something is stuck. */
    results.innerHTML =
      '<div class="ai-thinking">' +
      '<span class="ai-dots"><i></i><i></i><i></i></span>' +
      "<p>Reading the closet and dressing you for the day.</p>" +
      '<p class="mono">This takes about half a minute.</p>' +
      "</div>";

    fetch(root.dataset.endpoint, { method: "POST", body: body(again) })
      .then(function (response) {
        /* A non-OK response is a whole error PAGE, not a fragment. Injecting one
           here put the app's own layout — scripts included — inside the overlay
           and navigated the browser away from the builder entirely. Anything but
           a 200 is turned into the readable failure below instead. */
        if (!response.ok) throw new Error("HTTP " + response.status);
        return response.text();
      })
      .then(function (html) {
        results.innerHTML = html;
        wireResults();
      })
      .catch(function () {
        results.innerHTML =
          '<div class="ai-error"><p class="ai-error-msg">' +
          "That didn't get through — the app couldn't be reached.</p>" +
          '<p class="mono">Check the connection, or build it by hand in Manual.</p>' +
          '<div class="ai-recap-tools">' +
          '<button type="button" class="btn" data-back>Change the brief</button>' +
          '<button type="button" class="btn-brass" data-again>Try again</button>' +
          "</div></div>";
        wireResults();
      })
      .then(function () { state.busy = false; });
  }

  briefForm.addEventListener("submit", function (event) {
    event.preventDefault();
    ask(false);
  });

  /* Buttons inside the returned fragment are wired after every swap, because
     the fragment is new markup each time. */
  function wireResults() {
    var back = results.querySelector("[data-back]");
    if (back) {
      back.addEventListener("click", function () {
        results.hidden = true;
        setup.hidden = false;
      });
    }
    var again = results.querySelector("[data-again]");
    if (again) again.addEventListener("click", function () { ask(true); });

    [].slice.call(results.querySelectorAll("[data-tweak]")).forEach(function (button) {
      button.addEventListener("click", function () {
        /* Hands the picks to the manual builder as query parameters and lets
           builder.js click them in, so the derived strip is computed by the one
           implementation that owns it rather than copied here. */
        var picks = JSON.parse(button.dataset.picks || "[]");
        var query = ["build=1", "name=" + encodeURIComponent(button.dataset.name)];
        picks.forEach(function (p) {
          query.push("pick_" + encodeURIComponent(p.role) + "=" + encodeURIComponent(p.id));
        });
        window.location.href = "/fits?" + query.join("&");
      });
    });
  }

  renderSeeds();
  applyFilter();
})();
