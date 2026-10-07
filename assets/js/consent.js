class ConsentManager {
  constructor() { this.init(); }
  init() {
    if (localStorage.getItem('amana_consent')) return;
    const banner = document.getElementById('consentBanner');
    if (banner) banner.hidden = false;
    document.getElementById('consentAccept')?.addEventListener('click', () => {
      localStorage.setItem('amana_consent', 'true'); banner.hidden = true;
    });
    // Refined look, Oct 2026: equal-weight Reject option (was accept-only).
    document.getElementById('consentReject')?.addEventListener('click', () => {
      localStorage.setItem('amana_consent', 'false'); banner.hidden = true;
    });
  }
}
document.addEventListener('DOMContentLoaded', () => window.consentManager = new ConsentManager());