import re

html = """<section class="home-hero">
  <div class="container">
    <div class="home-hero-grid">
      <div class="home-hero-content">
        <div class="home-hero-eyebrow">
          <div class="home-hero-eyebrow-dot"></div>
          <span>Tanzania's Premier Investment Advisory</span>
        </div>
        <h1>Intelligence That<br><em>Builds Wealth</em></h1>
        <p class="home-hero-sub">Institutional-grade market intelligence, daily DSE analysis, and bespoke investment advisory for East Africa's discerning investors.</p>
        <div class="home-hero-cta">
          <a href="/market-intelligence" class="btn btn-primary" style="padding: 1rem 1.5rem; font-weight: 600; text-decoration: none;">Explore Market Data</a>
          <a href="/contact" class="btn" style="border: 1px solid rgba(200,150,46,0.5); color: #c8962e; padding: 1rem 1.5rem; border-radius: 8px; font-weight: 600; text-decoration: none;">Speak to an Advisor</a>
        </div>
        <div class="home-hero-trust">
          Regulated by the Capital Markets and Securities Authority (CMSA)
        </div>
      </div>
      <div class="home-hero-stats">
        <div class="home-stat-card">
          <div class="home-stat-value">250+</div>
          <div class="home-stat-label">Daily Wraps</div>
        </div>
        <div class="home-stat-card">
          <div class="home-stat-value">15 Yrs</div>
          <div class="home-stat-label">Experience</div>
        </div>
        <div class="home-stat-card">
          <div class="home-stat-value">DSE</div>
          <div class="home-stat-label">Licensed Dealer</div>
        </div>
      </div>
    </div>
  </div>
</section>"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'<section class="hero-section enhanced-hero".*?</section>', content, flags=re.DOTALL)
if match:
    old_hero = match.group(0)
    content = content.replace(old_hero, html)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Hero replaced successfully.')
else:
    print('Could not find old hero.')
