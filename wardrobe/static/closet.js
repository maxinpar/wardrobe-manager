/* The bulk bar: it only exists when something is selected. Pure progressive
   enhancement — with JS off the buttons still work, the bar is just always on. */
(function () {
  "use strict";
  var form = document.getElementById("closet-form");
  if (!form) return;
  var bar = form.querySelector(".bulk-bar");
  var count = form.querySelector("[data-selected-count]");

  function sync() {
    var n = form.querySelectorAll('input[name="item_id"]:checked').length;
    bar.hidden = n === 0;
    count.textContent = n + " selected";
  }
  form.addEventListener("change", function (e) {
    if (e.target.name === "item_id") sync();
  });
  form.querySelector("[data-clear-selection]").addEventListener("click", function () {
    form.querySelectorAll('input[name="item_id"]:checked').forEach(function (c) {
      c.checked = false;
    });
    sync();
  });
  sync();
})();
