// Static preview: preserve original form content, prevent any submission.
document.addEventListener('submit', function (event) {
  event.preventDefault();
  event.stopImmediatePropagation();
}, true);
