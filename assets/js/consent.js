class ConsentManager {
  constructor() { this.init(); }
  init() {
    if (localStorage.getItem('amana_consent')) return;
    const banner = document.getElementById('consentBanner');
    if (banner) banner.hidden = false;
    document.getElementById('consentAccept')?.addEventListener('click', () => {
      localStorage.setItem('amana_consent', 'true'); banner.hidden = true;
    });
  }
}
document.addEventListener('DOMContentLoaded', () => window.consentManager = new ConsentManager());