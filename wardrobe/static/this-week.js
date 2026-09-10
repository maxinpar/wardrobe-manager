/* This Week: which day is in the hero, and which day is picked up.

   Those two are the whole job. Everything that CHANGES the week — laying a set
   out, swapping two days, ticking one off — is an ordinary form POST, same as
   every other write in this app. What lives here is the looking: promoting a
   day into the hero is not a change, and the handoff is explicit that it must
   not navigate, because an earlier design had a per-day screen and it was cut.

   THE SERVER RENDERS ALL FIVE HEROES and this file shows one. It used to hold
   each day's copy in data- attributes and rebuild the hero from them, which was
   fine while a hero was a picture and three lines. It is now a picture, three
   lines and up to six garment tiles that are links into the wardrobe, and
   rebuilding that in innerHTML would be a second, worse copy of the template
   living in a .js file. Five panels of markup cost nothing: every render and
   every garment thumbnail on them is a file the day strip below has already
   pulled, so switching days is five cache hits and a class change.

   THE FOCUS SURVIVES A ROUND TRIP. Ticking Wednesday off is a POST and a
   redirect, and coming back to a screen that has jumped to today would undo the
   click that got you there. sessionStorage, keyed to the set so that changing
   set drops it rather than opening the new week on whichever day you were
   looking at in the old one. Same reasoning as layer-switch.js: it is view
   state, it does not belong in Postgres, and it should not outlive the tab.

   Without this file the screen still works: today's hero is the one the server
   marked, the forms still post, and only the Move pills go quiet. */

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

  /* ------------------------------------------------------------- the hero */

  function focus(card) {
    var day = card.getAttribute("data-day-name");

    for (var i = 0; i < days.length; i++) {
      days[i].classList.toggle("is-focus", days[i] === card);
    }
    var heroes = screen.querySelectorAll("[data-hero]");
    for (var j = 0; j < heroes.length; j++) {
      heroes[j].classList.toggle("is-on", heroes[j].getAttribute("data-hero") === day);
    }

    /* The bench puts a variant on the FOCUSED day, so its buttons and its hint
       follow the hero. A worn day is not a target — the tiles dim and stop
       being clickable rather than disappearing, so the set stays visible. */
    var bench = screen.querySelector(".thisweek-bench");
    if (bench) {
      var worn = card.getAttribute("data-worn") === "1";
      var weekday = card.getAttribute("data-weekday");

      var targets = bench.querySelectorAll("[data-bench-weekday]");
      for (var k = 0; k < targets.length; k++) targets[k].value = weekday;

      var picks = bench.querySelectorAll("[data-bench-pick]");
      for (var m = 0; m < picks.length; m++) picks[m].disabled = worn;
      bench.classList.toggle("is-blocked", worn);

      var tags = bench.querySelectorAll("[data-bench-tag]");
      for (var n = 0; n < tags.length; n++) {
        tags[n].textContent = worn ? day + " is worn" : "Put it on " + day;
      }
      var hint = bench.querySelector("[data-bench-hint]");
      var hintDay = bench.querySelector("[data-bench-day]");
      if (worn && hint) {
        hint.textContent = day + " is already worn — pick another day first.";
      } else if (hintDay) {
        hintDay.textContent = day;
      }
    }

    write(day);
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

  var restingHint = screen.querySelector("[data-strip-hint]");
  if (restingHint) restingHint.setAttribute("data-resting", restingHint.textContent.trim());

  for (var i = 0; i < days.length; i++) {
    (function (card) {
      var pick = card.querySelector("[data-day-pick]");
      if (pick) {
        pick.addEventListener("click", function () {
          /* While a day is held, tapping another day IS the swap — that is the
             one-handed path, and it has to beat "focus this day" or the pill
             would be the only way to finish a move. */
          if (isTarget(card)) {
            swap(lifted, card);
          } else {
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
  if (card) focus(card);
})();
