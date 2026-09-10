/* This Week: which day is in the hero, and which day is picked up.

   Those two are the whole job. Everything that CHANGES the week — laying a set
   out, swapping two days, ticking one off — is an ordinary form POST, same as
   every other write in this app. What lives here is the looking: promoting a
   day into the hero is not a change, and the handoff is explicit that it must
   not navigate, because an earlier design had a per-day screen and it was cut.

   So the page arrives with all five days' copy already in it, as data
   attributes on the day cards, and this file moves it into the hero. Nothing is
   fetched and nothing is invented: if a day card says it, the hero can show it.

   THE FOCUS SURVIVES A ROUND TRIP. Ticking Wednesday off is a POST and a
   redirect, and coming back to a screen that has jumped to today would undo the
   click that got you there. sessionStorage, keyed by nothing more than the app:
   it is view state, it does not belong in Postgres, and it should not outlive
   the tab. Same reasoning as layer-switch.js.

   It is stored WITH THE SET, so that changing set drops it rather than opening
   the new week on whichever day you happened to be looking at in the old one.
   A fresh set opens on today, which is what the server drew.

   Without this file the screen still works: the hero shows today, the forms
   still post, and only the Move pills go quiet. */

(function () {
  "use strict";

  var screen = document.querySelector("[data-thisweek]");
  if (!screen) return;

  var KEY = "wardrobe.weekFocus";
  var setKey = screen.getAttribute("data-set") || "";
  var days = Array.prototype.slice.call(screen.querySelectorAll("[data-day-name]"));
  if (!days.length) return;

  var lifted = null;   // the day currently picked up, or null

  function read() {
    try {
      var stored = (window.sessionStorage.getItem(KEY) || "").split("|");
      return stored[0] === setKey ? stored[1] : null;
    } catch (e) {
      return null;     // private mode, a full quota: fall back to today
    }
  }

  function write(day) {
    try {
      window.sessionStorage.setItem(KEY, setKey + "|" + day);
    } catch (e) {
      /* Degrade to this-page-only. The focus still moves, it just stops
         travelling across a swap. */
    }
  }

  function cardFor(day) {
    for (var i = 0; i < days.length; i++) {
      if (days[i].getAttribute("data-day-name") === day) return days[i];
    }
    return null;
  }

  function focused() {
    return screen.querySelector(".thisweek-day.is-focus") || days[0];
  }

  /* ------------------------------------------------------------- the hero */

  function setText(selector, text) {
    var node = screen.querySelector(selector);
    if (node) node.textContent = text;
  }

  function paintHero(card) {
    var frame = screen.querySelector("[data-hero-frame]");
    var image = card.getAttribute("data-image");
    if (frame) {
      if (image) {
        frame.innerHTML = "";
        var figure = document.createElement("span");
        figure.className = "thisweek-hero-figure";
        var img = document.createElement("img");
        img.src = image;
        img.alt = card.getAttribute("data-name");
        figure.appendChild(img);
        frame.appendChild(figure);
      } else {
        frame.innerHTML = "";
        var empty = document.createElement("span");
        empty.className = "thisweek-hero-figure is-empty";
        empty.textContent = "No variant built for this day";
        frame.appendChild(empty);
      }
    }

    setText("[data-hero-day]", card.getAttribute("data-day-line"));
    setText("[data-hero-name]", card.getAttribute("data-name"));
    setText("[data-hero-sub]", card.getAttribute("data-sub"));
    setText("[data-hero-note]", card.getAttribute("data-note"));

    var weekday = screen.querySelector("[data-hero-weekday]");
    if (weekday) weekday.value = card.getAttribute("data-weekday");

    var worn = card.getAttribute("data-worn") === "1";
    var empty = !image;
    var button = screen.querySelector("[data-hero-wear]");
    if (button) {
      button.disabled = empty;
      button.classList.toggle("is-worn", worn && !empty);
      button.textContent = empty ? "Nothing to wear yet" : (worn ? "Worn ✓" : "I wore this");
    }

    /* The bench puts a variant on the FOCUSED day, so its buttons and its hint
       follow the hero. A worn day is not a target — the tiles dim and stop
       being clickable rather than disappearing, so the set is still visible. */
    var day = card.getAttribute("data-day-name");
    var bench = screen.querySelector(".thisweek-bench");
    if (bench) {
      var targets = bench.querySelectorAll("[data-bench-weekday]");
      for (var i = 0; i < targets.length; i++) {
        targets[i].value = card.getAttribute("data-weekday");
      }
      var picks = bench.querySelectorAll("[data-bench-pick]");
      for (var j = 0; j < picks.length; j++) picks[j].disabled = worn;
      bench.classList.toggle("is-blocked", worn);

      var tags = bench.querySelectorAll("[data-bench-tag]");
      for (var k = 0; k < tags.length; k++) {
        tags[k].textContent = worn ? day + " is worn" : "Put it on " + day;
      }
      var hint = bench.querySelector("[data-bench-hint]");
      var hintDay = bench.querySelector("[data-bench-day]");
      if (worn && hint) {
        hint.textContent = day + " is already worn — pick another day first.";
      } else if (hintDay) {
        hintDay.textContent = day;
      }
    }
  }

  function focus(card) {
    for (var i = 0; i < days.length; i++) days[i].classList.remove("is-focus");
    card.classList.add("is-focus");
    write(card.getAttribute("data-day-name"));
    paintHero(card);
  }

  /* ------------------------------------------------------- picking a day up */

  function isTarget(card) {
    return lifted !== null && card !== lifted && card.getAttribute("data-worn") !== "1";
  }

  function paintLift() {
    var hint = screen.querySelector("[data-strip-hint]");
    for (var i = 0; i < days.length; i++) {
      var card = days[i];
      var held = card === lifted;
      var target = isTarget(card);
      card.classList.toggle("is-lifted", held);
      card.classList.toggle("is-target", target);

      var drop = card.querySelector(".thisweek-day-drop");
      if (drop && lifted) {
        drop.textContent = "Swap with " + lifted.getAttribute("data-day-name");
      }
      var move = card.querySelector("[data-day-move]");
      if (move) {
        move.textContent = held ? "Cancel" : (target ? "Swap here" : "Move");
      }
    }
    if (hint) {
      hint.textContent = lifted
        ? "Holding " + lifted.getAttribute("data-day-name") +
          " — drop it on the day you want it to trade with."
        : hint.getAttribute("data-resting");
      hint.classList.toggle("is-holding", !!lifted);
    }
  }

  function swap(a, b) {
    var form = screen.querySelector("[data-swap-form]");
    if (!form) return;
    form.querySelector("[data-swap-a]").value = a.getAttribute("data-weekday");
    form.querySelector("[data-swap-b]").value = b.getAttribute("data-weekday");
    form.submit();
  }

  function lift(card) {
    if (card.getAttribute("data-worn") === "1") return;   // a worn day is inert
    if (lifted === null) {
      lifted = card;
    } else if (lifted === card) {
      lifted = null;                                      // pressing it again cancels
    } else {
      swap(lifted, card);
      return;
    }
    paintLift();
  }

  /* --------------------------------------------------------------- wiring */

  var hint = screen.querySelector("[data-strip-hint]");
  if (hint) hint.setAttribute("data-resting", hint.textContent.trim());

  for (var i = 0; i < days.length; i++) {
    (function (card) {
      var pick = card.querySelector("[data-day-pick]");
      if (pick) {
        pick.addEventListener("click", function () {
          /* While a day is held, tapping another day is the swap — that is the
             one-handed path, and it has to beat "focus this day" or the pill
             would be the only way to finish a move. */
          if (isTarget(card)) swap(lifted, card);
          else {
            lifted = null;
            paintLift();
            focus(card);
          }
        });
      }

      var move = card.querySelector("[data-day-move]");
      if (move) {
        move.addEventListener("click", function (event) {
          event.stopPropagation();
          lift(card);
        });
      }

      card.addEventListener("dragstart", function (event) {
        if (card.getAttribute("data-worn") === "1") {
          event.preventDefault();
          return;
        }
        /* Firefox will not start a drag without data on it. */
        if (event.dataTransfer) {
          event.dataTransfer.effectAllowed = "move";
          try {
            event.dataTransfer.setData("text/plain", card.getAttribute("data-day-name"));
          } catch (e) { /* older browsers refuse setData outside their own types */ }
        }
        lifted = card;
        paintLift();
      });

      card.addEventListener("dragend", function () {
        lifted = null;
        paintLift();
      });

      card.addEventListener("dragover", function (event) {
        if (isTarget(card)) event.preventDefault();
      });

      card.addEventListener("drop", function (event) {
        if (!isTarget(card)) return;
        event.preventDefault();
        swap(lifted, card);
      });
    })(days[i]);
  }

  /* Arrive where you left off — or on today, which is what the server drew. */
  var remembered = read();
  var card = remembered ? cardFor(remembered) : null;
  if (card && card !== focused()) focus(card);
  else focus(focused());
})();
