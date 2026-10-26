// Public embed copied from the archived original site. No password or token.
(() => {
  const initialize = () => {
    if (document.documentElement.dataset.notaraReady === 'true') return;
    document.documentElement.dataset.notaraReady = 'true';
    new NotaryDatasheetWidget('notary-widget-container', '1499', 'popup', {
      widgetOpenButtonColor: '#7a3674',
      widgetOpenButtonIconColor: '#ffffff',
      speechBubbleText: 'Notartermin online vorbereiten',
      speechBubbleColor: '#7a3674',
      speechBubbleTextColor: '#ffffff'
    });
  };
  const load = () => {
    if (typeof NotaryDatasheetWidget === 'function') { initialize(); return; }
    const script = document.createElement('script');
    script.src = 'https://app.notara.de/js/notary-datasheet-widget.js';
    script.onload = initialize;
    document.head.appendChild(script);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', load, {once:true});
  else load();
})();
