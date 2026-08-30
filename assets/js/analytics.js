class AnalyticsManager {
  constructor() { this.init(); }
  init() { this.initClarity(); this.setupEventTracking(); this.setupPerformanceMonitoring(); }
  initClarity() {
    if (document.getElementById('clarity-script')) return;
    const clarityId = window.analyticsConfig?.clarityId || 'YOUR_CLARITY_PROJECT_ID';
    if (!clarityId || clarityId === 'YOUR_CLARITY_PROJECT_ID') return;
    const script = document.createElement('script'); script.id = 'clarity-script'; script.async = true;
    script.src = `https://www.clarity.ms/tag/${clarityId}`; document.head.appendChild(script);
  }
  setupEventTracking() {
    document.addEventListener('click', (e) => {
      const target = e.target.closest('button, a');
      if (target && target.closest('.btn, .cta-button, .card, .nav-link')) {
        this.trackEvent('click', { element: target.tagName, text: target.textContent?.trim(), href: target.href, id: target.id });
      }
    });
  }
  setupPerformanceMonitoring() { /* omitted for brevity */ }
  trackEvent(event, data) {
    if (window.clarity) window.clarity('event', event, data);
    if (window.gtag) window.gtag('event', event, data);
    console.log(`[Analytics] ${event}:`, data);
  }
}
document.addEventListener('DOMContentLoaded', () => window.analytics = new AnalyticsManager());
