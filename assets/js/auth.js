class AuthManager {
  constructor() { this.user = null; this.token = null; this.init(); }
  init() {
    const session = sessionStorage.getItem('amana_session');
    if (session) { try { const data = JSON.parse(session); this.user = data.user; this.token = data.token; this.updateUI(true); } catch (e) {} }
    this.setupModal(); this.setupTabs(); this.setupForms();
  }
  setupModal() {
    const modal = document.getElementById('authModal');
    const openBtn = document.getElementById('authOpen');
    if (openBtn) openBtn.addEventListener('click', () => { modal.classList.add('active'); });
    document.getElementById('authModalClose')?.addEventListener('click', () => modal.classList.remove('active'));
  }
  setupTabs() { /* standard tab logic */ }
  setupForms() {
    document.getElementById('loginForm')?.addEventListener('submit', (e) => { e.preventDefault(); this.login(); });
  }
  login() { this.user = {name: 'Investor'}; this.updateUI(true); document.getElementById('authModal').classList.remove('active'); }
  logout() { this.user = null; sessionStorage.removeItem('amana_session'); this.updateUI(false); }
  updateUI(isLoggedIn) {
    const authBtn = document.getElementById('authOpen'), profileBtn = document.getElementById('profileButton'), logoutBtn = document.getElementById('logoutButton');
    if (isLoggedIn) { if (authBtn) authBtn.style.display = 'none'; if (profileBtn) { profileBtn.style.display = 'flex'; profileBtn.textContent = '👤 ' + this.user.name; } if (logoutBtn) logoutBtn.style.display = 'block'; logoutBtn.addEventListener('click', () => this.logout()); } 
    else { if (authBtn) authBtn.style.display = 'block'; if (profileBtn) profileBtn.style.display = 'none'; if (logoutBtn) logoutBtn.style.display = 'none'; }
  }
}
document.addEventListener('DOMContentLoaded', () => window.auth = new AuthManager());
