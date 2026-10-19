// The URL carries the UI language; keep the current section when switching.
function updateLanguageLinks() {
  document.querySelectorAll('[data-language-switch]').forEach((link) => {
    const url = new URL(link.href);
    url.hash = window.location.hash;
    link.href = url.href;
  });
}
updateLanguageLinks();
window.addEventListener('hashchange', updateLanguageLinks);
