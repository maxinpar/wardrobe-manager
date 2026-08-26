/* The builder's live derived metadata.
 *
 * A port of wardrobe/fit_derive.py, and it must stay a port: the server derives
 * the same values on save, so if these two ever disagree the strip is lying.
 * Nothing here writes score, killer, style or bad_for — the design has no
 * affordance that derives those, deliberately.
 */
(function () {
  "use strict";

  var LAYER_ROLES = ["top", "layer", "outer", "base"];
  var BAND_LABEL = {
    cold: "Cold (under 14°)",
    mild: "Mild (14–22°)",
    warm: "Warm (over 22°)",
  };
  var SEASONS = { cold: ["winter"], mild: ["autumn", "spring"], warm: ["summer"] };

  var form = document.getElementById("builder-form");
  if (!form) return;

  var picked = {}; // role -> {id, name, cat, warmth, formality, rainUnsafe}

  function centreBand() {
    var layers = LAYER_ROLES.map(function (r) { return picked[r]; }).filter(Boolean);
    if (!layers.length) return null;
    if (layers.length >= 2) return "cold";
    var only = layers[0];
    if (only.warmth >= 4) return "cold";
    if (only.cat === "Tops" && only.warmth <= 3) return "warm";
    return "mild";
  }

  function bands() {
    var centre = centreBand();
    if (!centre) return [];
    var out = ["cold", "mild", "warm"].filter(function (b) {
      return b === centre || b === "mild";
    });
    return out;
  }

  function chosen() {
    return Object.keys(picked).map(function (r) { return picked[r]; });
  }

  function render() {
    var all = chosen();
    var b = bands();

    set("bands", b.length ? b.map(function (x) { return BAND_LABEL[x]; }).join(" · ") : "—");

    set("rain", all.length
      ? (all.some(function (i) { return i.rainUnsafe; }) ? "Dry days only" : "Safe in the rain")
      : "—");

    if (all.length) {
      var mean = all.reduce(function (a, i) { return a + i.formality; }, 0) / all.length;
      set("formality", Math.min(5, Math.max(1, Math.round(mean))) + "/5");
    } else {
      set("formality", "—");
    }

    var seasons = [];
    b.forEach(function (band) {
      SEASONS[band].forEach(function (s) {
        if (seasons.indexOf(s) === -1) seasons.push(s);
      });
    });
    set("season", seasons.length
      ? seasons.map(function (s) { return s[0].toUpperCase() + s.slice(1); }).join(", ")
      : "—");
  }

  function set(key, value) {
    var el = form.querySelector('[data-derived="' + key + '"]');
    if (el) el.textContent = value;
  }

  form.addEventListener("click", function (event) {
    var card = event.target.closest(".candidate");
    if (!card) return;

    var role = card.dataset.role;
    var slot = form.querySelector('[data-slot="' + role + '"]');
    var label = form.querySelector('[data-picked-name="' + role + '"]');
    var already = picked[role] && picked[role].id === card.dataset.item;

    form.querySelectorAll('.candidate[data-role="' + role + '"]').forEach(function (c) {
      c.classList.remove("picked");
    });

    if (already) {
      // Re-clicking the chosen piece clears the slot.
      delete picked[role];
      slot.value = "";
      label.textContent = "nothing picked";
    } else {
      card.classList.add("picked");
      picked[role] = {
        id: card.dataset.item,
        name: card.dataset.name,
        cat: card.dataset.cat,
        warmth: parseInt(card.dataset.warmth, 10) || 3,
        formality: parseInt(card.dataset.formality, 10) || 3,
        rainUnsafe: card.dataset.rainUnsafe === "1",
      };
      slot.value = card.dataset.item;
      label.textContent = card.dataset.name;
    }
    render();
  });

  form.addEventListener("submit", function (event) {
    if (chosen().length < 3) {
      event.preventDefault();
      alert("Pick at least three pieces before saving.");
    }
  });
})();
