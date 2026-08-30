class PersonalisationEngine {
  constructor() {
    this.userId = this.getUserId();
    this.preferences = this.loadPreferences();
    this.history = this.loadHistory();
    this.init();
  }
  getUserId() {
    let id = localStorage.getItem('amana_user_id');
    if (!id) {
      id = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('amana_user_id', id);
    }
    return id;
  }
  loadPreferences() {
    const stored = localStorage.getItem('amana_preferences');
    if (stored) {
      try { return JSON.parse(stored); } catch (e) { return this.getDefaultPreferences(); }
    }
    return this.getDefaultPreferences();
  }
  getDefaultPreferences() {
    return { investorType: 'retail', preferredAssetClasses: ['equities', 'bonds'], riskTolerance: 'moderate', interests: [], savedWraps: [], watchlist: [] };
  }
  loadHistory() {
    const stored = localStorage.getItem('amana_history');
    if (stored) {
      try { return JSON.parse(stored); } catch (e) { return { pages: [], searches: [], interactions: {} }; }
    }
    return { pages: [], searches: [], interactions: {} };
  }
  savePreferences() { localStorage.setItem('amana_preferences', JSON.stringify(this.preferences)); }
  saveHistory() { localStorage.setItem('amana_history', JSON.stringify(this.history)); }
  trackPage(page) {
    this.history.pages.push({ url: page, timestamp: Date.now() });
    if (this.history.pages.length > 50) this.history.pages = this.history.pages.slice(-50);
    this.saveHistory();
  }
  trackInteraction(type, data) {
    if (!this.history.interactions[type]) this.history.interactions[type] = [];
    this.history.interactions[type].push({ data: data, timestamp: Date.now() });
    this.saveHistory();
  }
  getRecommendations(type = 'wraps', limit = 3) {
    const tagFrequency = {};
    if (this.history.pages.length === 0) return this.getDefaultRecommendations();
    this.history.pages.forEach(page => {
      this.extractTagsFromUrl(page.url).forEach(tag => {
        tagFrequency[tag] = (tagFrequency[tag] || 0) + 1;
      });
    });
    const sortedTags = Object.entries(tagFrequency).sort((a, b) => b[1] - a[1]).slice(0, 5).map(e => e[0]);
    return this.getContentByTags(sortedTags, limit);
  }
  extractTagsFromUrl(url) {
    const tags = [];
    if (url.includes('equity')) tags.push('equities');
    if (url.includes('bond')) tags.push('bonds');
    if (url.includes('etf')) tags.push('etfs');
    if (url.includes('daily-wrap')) tags.push('daily-wrap');
    if (url.includes('market-intelligence')) tags.push('market-intelligence');
    return tags;
  }
  getDefaultRecommendations() {
    return [
      { title: 'Understanding DSE Market Mechanics', url: '/education/dse-basics/' },
      { title: 'Daily Market Wrap – 28 August 2026', url: '/daily-wrap/2026-08-28/' },
      { title: 'Introduction to Bonds in Tanzania', url: '/education/bonds-intro/' },
    ];
  }
  getContentByTags(tags, limit) {
    const content = [
      { title: 'Equity Markets 101', tags: ['equities'], url: '/education/equity-basics/' },
      { title: 'Bond Calculator Guide', tags: ['bonds'], url: '/tools/bond-calculator/' },
      { title: 'ETF Investment Guide', tags: ['etfs'], url: '/education/etf-guide/' },
      { title: 'Daily Market Analysis', tags: ['market-intelligence'], url: '/market-intelligence/' },
    ];
    const matching = content.filter(item => item.tags.some(tag => tags.includes(tag)));
    if (matching.length === 0) return this.getDefaultRecommendations();
    return matching.slice(0, limit);
  }
  updatePreferencesFromBehaviour() {
    const wrapVisits = this.history.pages.filter(p => p.url.includes('daily-wrap'));
    if (wrapVisits.length > 5 && !this.preferences.preferredAssetClasses.includes('equities')) {
      this.preferences.preferredAssetClasses.push('equities');
      this.savePreferences();
    }
  }
  init() {
    this.trackPage(window.location.pathname);
    this.updatePreferencesFromBehaviour();
    this.renderPersonalisedContent();
  }
  renderPersonalisedContent() {
    const recContainer = document.getElementById('personalised-recommendations');
    if (recContainer) {
      recContainer.innerHTML = this.getRecommendations('wraps', 3).map(item => `
        <div class="recommendation-item">
          <a href="${item.url}" class="recommendation-link">
            <span class="recommendation-icon">📈</span>
            <span class="recommendation-title">${item.title}</span>
          </a>
        </div>
      `).join('');
    }
    const greetingContainer = document.getElementById('personalised-greeting');
    if (greetingContainer) {
      const hour = new Date().getHours();
      let greeting = 'Good morning';
      if (hour >= 12 && hour < 17) greeting = 'Good afternoon';
      if (hour >= 17) greeting = 'Good evening';
      let userType = 'investor';
      if (this.preferences.investorType === 'institutional') userType = 'institutional investor';
      if (this.preferences.investorType === 'diaspora') userType = 'diaspora investor';
      greetingContainer.innerHTML = `<span class="greeting-text">${greeting},</span><span class="greeting-user">${userType}</span>`;
    }
    this.renderDashboardStats();
  }
  renderDashboardStats() {
    const statsContainer = document.getElementById('personalised-stats');
    if (!statsContainer) return;
    const wrapCount = this.history.pages.filter(p => p.url.includes('daily-wrap')).length;
    const toolUsage = Object.keys(this.history.interactions).filter(k => k.includes('calculator') || k.includes('modeler')).length;
    statsContainer.innerHTML = `
      <div class="stat-item"><span class="stat-number">${wrapCount}</span><span class="stat-label">Wraps Read</span></div>
      <div class="stat-item"><span class="stat-number">${toolUsage}</span><span class="stat-label">Tools Used</span></div>
      <div class="stat-item"><span class="stat-number">${this.history.pages.length}</span><span class="stat-label">Pages Visited</span></div>
    `;
  }
}
document.addEventListener('DOMContentLoaded', () => window.personalisation = new PersonalisationEngine());
document.addEventListener('swup:content:replace', () => { if (window.personalisation) window.personalisation.renderPersonalisedContent(); });
