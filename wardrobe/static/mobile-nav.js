/* The More sheet behind the phone tab bar.
 *
 * Everything else about the phone layout is CSS: this file exists only because
 * a sheet has to open and close, which a media query cannot do. It stays inert
 * on desktop — the button it binds to is display:none up there, so nothing can
 * open the sheet — but the breakpoint is still watched, because a rotated
 * phone or a resized window must not leave a sheet stranded over the desktop
 * layout.
 *
 * Navigation is a full page load in this app, so picking a row resets the
 * sheet on its own. There is nothing to close on the way out.
 */
(function () {
  var button = document.getElementById('more-button');
  var sheet = document.getElementById('more-sheet');
  if (!button || !sheet) return;

  var phone = window.matchMedia('(max-width: 760px)');
  /* More is lit by the server when one of its own destinations is the page.
     Opening the sheet lights it too, so closing has to put it back rather than
     just clear it. */
  var litByPage = button.classList.contains('on');

  function setOpen(open) {
    sheet.hidden = !open;
    button.setAttribute('aria-expanded', open ? 'true' : 'false');
    button.classList.toggle('on', open || litByPage);
    /* The sheet is the only thing that should scroll while it is up. */
    document.body.classList.toggle('sheet-open', open);
  }

  button.addEventListener('click', function () {
    setOpen(sheet.hidden);
  });

  /* The scrim is a real button, so a tap and the Enter key both land here. */
  sheet.addEventListener('click', function (event) {
    if (event.target.closest('[data-more-close]')) setOpen(false);
  });

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && !sheet.hidden) setOpen(false);
  });

  /* Crossing the breakpoint drops the sheet rather than hiding it behind CSS:
     the button's aria-expanded would otherwise keep claiming it was open. */
  var onBreakpoint = function (event) {
    if (!event.matches) setOpen(false);
  };
  if (phone.addEventListener) {
    phone.addEventListener('change', onBreakpoint);
  } else if (phone.addListener) {
    phone.addListener(onBreakpoint);
  }
})();
