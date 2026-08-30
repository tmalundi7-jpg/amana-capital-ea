class ClientEngagement {
  constructor() {
    this.watchlist = this.loadWatchlist();
    this.savedWraps = this.loadSavedWraps();
    this.alerts = this.loadAlerts();
    this.init();
  }
  loadWatchlist() { try { return JSON.parse(localStorage.getItem('amana_watchlist')) || []; } catch(e) { return []; } }
  loadSavedWraps() { try { return JSON.parse(localStorage.getItem('amana_saved_wraps')) || []; } catch(e) { return []; } }
  loadAlerts() { try { return JSON.parse(localStorage.getItem('amana_alerts')) || []; } catch(e) { return []; } }
  saveWatchlist() { localStorage.setItem('amana_watchlist', JSON.stringify(this.watchlist)); }
  saveSavedWraps() { localStorage.setItem('amana_saved_wraps', JSON.stringify(this.savedWraps)); }
  saveAlerts() { localStorage.setItem('amana_alerts', JSON.stringify(this.alerts)); }
  addToWatchlist(symbol, name) {
    if (!this.watchlist.find(item => item.symbol === symbol)) {
      this.watchlist.push({ symbol, name, addedAt: Date.now() });
      this.saveWatchlist(); this.renderWatchlist(); return true;
    }
    return false;
  }
  removeFromWatchlist(symbol) {
    this.watchlist = this.watchlist.filter(item => item.symbol !== symbol);
    this.saveWatchlist(); this.renderWatchlist();
  }
  isInWatchlist(symbol) { return this.watchlist.some(item => item.symbol === symbol); }
  renderWatchlist() {
    const container = document.getElementById('watchlist-container');
    if (!container) return;
    if (this.watchlist.length === 0) {
      container.innerHTML = `<div class="watchlist-empty"><p>Your watchlist is empty.</p><p class="watchlist-hint">Click the ☆ icon on any stock to add it.</p></div>`;
      return;
    }
    container.innerHTML = `<ul class="watchlist-items">${this.watchlist.map(item => `
      <li class="watchlist-item"><span class="watchlist-symbol">${item.symbol}</span><span class="watchlist-name">${item.name || ''}</span>
      <button class="watchlist-remove" data-symbol="${item.symbol}">✕</button></li>`).join('')}</ul>`;
    container.querySelectorAll('.watchlist-remove').forEach(btn => btn.addEventListener('click', () => this.removeFromWatchlist(btn.dataset.symbol)));
  }
  toggleSaveWrap(wrapId, wrapTitle) {
    const existing = this.savedWraps.find(item => item.id === wrapId);
    if (existing) {
      this.savedWraps = this.savedWraps.filter(item => item.id !== wrapId);
      this.saveSavedWraps(); this.renderSavedWraps(); this.updateSaveButton(wrapId, false); return false;
    } else {
      this.savedWraps.push({ id: wrapId, title: wrapTitle, savedAt: Date.now() });
      this.saveSavedWraps(); this.renderSavedWraps(); this.updateSaveButton(wrapId, true); return true;
    }
  }
  isWrapSaved(wrapId) { return this.savedWraps.some(item => item.id === wrapId); }
  renderSavedWraps() {
    const container = document.getElementById('saved-wraps-container');
    if (!container) return;
    if (this.savedWraps.length === 0) {
      container.innerHTML = `<div class="saved-wraps-empty"><p>No saved wraps yet.</p></div>`; return;
    }
    container.innerHTML = `<ul class="saved-wraps-items">${this.savedWraps.map(item => `
      <li class="saved-wrap-item"><a href="/daily-wrap/${item.id}/" class="saved-wrap-link"><span class="saved-wrap-title">${item.title}</span></a>
      <button class="saved-wrap-remove" data-id="${item.id}">✕</button></li>`).join('')}</ul>`;
    container.querySelectorAll('.saved-wrap-remove').forEach(btn => btn.addEventListener('click', () => {
      this.savedWraps = this.savedWraps.filter(i => i.id !== btn.dataset.id); this.saveSavedWraps(); this.renderSavedWraps();
    }));
  }
  updateSaveButton(wrapId, isSaved) {
    const btn = document.querySelector(`[data-wrap-id="${wrapId}"] .save-wrap-btn`);
    if (btn) { btn.textContent = isSaved ? '★ Saved' : '☆ Save'; btn.classList.toggle('saved', isSaved); }
  }
  addAlert(asset, condition, value) {
    this.alerts.push({ id: 'alert_' + Date.now(), asset, condition, value, createdAt: Date.now(), triggered: false });
    this.saveAlerts(); this.renderAlerts();
  }
  removeAlert(alertId) {
    this.alerts = this.alerts.filter(item => item.id !== alertId);
    this.saveAlerts(); this.renderAlerts();
  }
  renderAlerts() {
    const container = document.getElementById('alerts-container');
    if (!container) return;
    if (this.alerts.length === 0) { container.innerHTML = `<div class="alerts-empty"><p>No alerts set.</p></div>`; return; }
    container.innerHTML = `<ul class="alert-items">${this.alerts.map(a => `
      <li class="alert-item"><span class="alert-asset">${a.asset}</span><span class="alert-condition">${a.condition} ${a.value}</span>
      <span class="alert-status ${a.triggered ? 'triggered' : 'active'}">${a.triggered ? '✓ Triggered' : 'Active'}</span>
      <button class="alert-remove" data-id="${a.id}">✕</button></li>`).join('')}</ul>`;
    container.querySelectorAll('.alert-remove').forEach(btn => btn.addEventListener('click', () => this.removeAlert(btn.dataset.id)));
  }
  init() {
    this.renderWatchlist(); this.renderSavedWraps(); this.renderAlerts();
    document.querySelectorAll('.add-to-watchlist').forEach(btn => {
      btn.addEventListener('click', () => {
        this.addToWatchlist(btn.dataset.symbol, btn.dataset.name || btn.dataset.symbol);
        btn.textContent = '★ In Watchlist'; btn.classList.add('in-watchlist');
      });
    });
    document.querySelectorAll('.save-wrap-btn').forEach(btn => {
      if (this.isWrapSaved(btn.dataset.wrapId)) { btn.textContent = '★ Saved'; btn.classList.add('saved'); }
      btn.addEventListener('click', () => this.toggleSaveWrap(btn.dataset.wrapId, btn.dataset.wrapTitle || 'Daily Wrap'));
    });
  }
}
document.addEventListener('DOMContentLoaded', () => window.engagement = new ClientEngagement());
