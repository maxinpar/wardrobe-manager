/* Attaching a render to a fit.

   Progressive enhancement, and only where Jinja can't reach: without this file
   the button is still a file input inside a real form and the upload still
   works — it just posts the original file and reloads the hard way.

   What the script adds: the file picker opens from the button, the frame is a
   drop target, and the image is downscaled in the browser before it is sent.
   That last part is the point. The app is reachable from a phone on the same
   wifi, and a phone photo is several megabytes for a card that is 5/8 of a
   column wide. The server downscales again regardless — this is about the wire,
   not about trust. */

(function () {
  var MAX_EDGE = 1000;      // the long edge; matches the server
  var QUALITY = 0.84;

  var form = document.querySelector('[data-render-form]');
  if (!form) return;

  var input = form.querySelector('[data-render-input]');
  var button = form.querySelector('[data-render-pick]');
  var frame = document.querySelector('[data-render-drop]');

  button.addEventListener('click', function (event) {
    event.preventDefault();
    input.click();
  });

  input.addEventListener('change', function () {
    if (input.files && input.files[0]) send(input.files[0]);
  });

  /* Downscale to a JPEG blob. Aspect ratio is preserved — the frame contains
     rather than crops, so a portrait render letterboxes instead of losing its
     head. If anything here fails we post the original file rather than nothing. */
  function shrink(file) {
    return new Promise(function (resolve) {
      var url = URL.createObjectURL(file);
      var img = new Image();
      img.onload = function () {
        URL.revokeObjectURL(url);
        var scale = Math.min(1, MAX_EDGE / Math.max(img.width, img.height));
        var canvas = document.createElement('canvas');
        canvas.width = Math.round(img.width * scale);
        canvas.height = Math.round(img.height * scale);
        var ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        canvas.toBlob(function (blob) { resolve(blob || file); }, 'image/jpeg', QUALITY);
      };
      img.onerror = function () { URL.revokeObjectURL(url); resolve(file); };
      img.src = url;
    });
  }

  function send(file) {
    if (!/^image\//.test(file.type)) return;   // a non-image is ignored, silently
    button.disabled = true;
    button.textContent = 'Uploading…';
    shrink(file).then(function (blob) {
      var data = new FormData();
      data.append('render', blob, 'render.jpg');
      data.append('next', form.querySelector('[name=next]').value);
      return fetch(form.action, { method: 'POST', body: data });
    }).then(function () {
      window.location.reload();
    }).catch(function () {
      // Fall back to the plain form post, which needs the real file.
      button.disabled = false;
      form.submit();
    });
  }

  if (!frame) return;

  /* dragover has to be cancelled on every event or the browser navigates to the
     dropped file instead of handing it over. */
  ['dragenter', 'dragover'].forEach(function (name) {
    frame.addEventListener(name, function (event) {
      event.preventDefault();
      frame.classList.add('drop-active');
    });
  });

  ['dragleave', 'dragend'].forEach(function (name) {
    frame.addEventListener(name, function (event) {
      if (event.target === frame) frame.classList.remove('drop-active');
    });
  });

  frame.addEventListener('drop', function (event) {
    event.preventDefault();
    frame.classList.remove('drop-active');
    var file = event.dataTransfer && event.dataTransfer.files[0];
    if (file) send(file);
  });
})();
