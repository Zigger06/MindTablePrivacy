'use strict';

// Progressive enhancement only. Policy text and navigation work without JavaScript.
document.querySelectorAll('[data-print]').forEach((button) => {
  button.hidden = false;
  button.addEventListener('click', () => window.print());
});

if ('IntersectionObserver' in window) {
  const links = new Map([...document.querySelectorAll('.toc a')].map((link) => [link.hash.slice(1), link]));
  const observer = new IntersectionObserver((entries) => {
    const current = entries.find((entry) => entry.isIntersecting);
    if (!current) return;
    links.forEach((link) => link.removeAttribute('aria-current'));
    links.get(current.target.id)?.setAttribute('aria-current', 'location');
  }, { rootMargin: '-15% 0px -65% 0px' });
  document.querySelectorAll('.policy-section').forEach((section) => observer.observe(section));
}
