(() => {
  const button = document.querySelector('.menu-button');
  const nav = document.querySelector('#navigation');
  const media = window.matchMedia('(max-width: 760px)');
  const close = () => { button.setAttribute('aria-expanded', 'false'); nav.hidden = media.matches; };
  if (button && nav) {
    close();
    media.addEventListener('change', close);
    button.addEventListener('click', () => {
      const open = button.getAttribute('aria-expanded') !== 'true';
      button.setAttribute('aria-expanded', String(open));
      nav.hidden = !open;
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') { close(); button.focus(); }
    });
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
  }
})();
