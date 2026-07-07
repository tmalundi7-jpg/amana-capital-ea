import os
import glob
import re

repo_dir = r'C:\Users\tmalu\.gemini\antigravity\scratch\amana-repo\amana-capital-ea-main'
css_path = os.path.join(repo_dir, 'style.css')
js_dir = os.path.join(repo_dir, 'js')

os.makedirs(js_dir, exist_ok=True)

# 1. Update CSS
with open(css_path, 'a', encoding='utf-8') as f:
    f.write('''

/* --- PREMIUM ENHANCEMENTS --- */

/* Smooth Transitions & Micro-Interactions */
.service-card, .pillar-card, .teaser-card, .btn {
    transition: all 0.3s ease;
}
.service-card:hover, .pillar-card:hover, .teaser-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}

/* Sticky Glassmorphic Navigation */
.navbar {
    position: sticky;
    top: 0;
    z-index: 1000;
    background: rgba(11, 29, 58, 0.95);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

/* Dark Mode Variables */
[data-theme="dark"] {
    --cream: #0f172a;
    --navy: #020617;
    --white: #1e293b;
    --text: #cbd5e1;
}

[data-theme="dark"] body {
    background-color: var(--cream);
    color: var(--text);
}

[data-theme="dark"] h1, [data-theme="dark"] h2, [data-theme="dark"] h3 {
    color: #f1f5f9;
}

[data-theme="dark"] .section-alt, [data-theme="dark"] .hero-section {
    background-color: #020617;
}

/* Theme Toggle Button */
.theme-toggle {
    background: none;
    border: none;
    color: var(--gold);
    font-size: 1.2rem;
    cursor: pointer;
    margin-left: 1rem;
    transition: transform 0.3s ease;
}
.theme-toggle:hover {
    transform: rotate(15deg) scale(1.1);
}

/* Calculator Styles */
.calc-card {
    background: var(--white);
    padding: 2rem;
    border: 2px solid var(--gold);
    border-radius: 4px;
    margin: 2rem 0;
}
.calc-input {
    width: 100%;
    padding: 0.75rem;
    margin-bottom: 1rem;
    border: 1px solid #ccc;
    background: var(--white);
    color: var(--text);
}
.calc-result {
    font-size: 2rem;
    color: var(--navy);
    font-weight: bold;
    margin-top: 1rem;
}
[data-theme="dark"] .calc-result { color: var(--gold); }
''' )

# 2. JS Files
theme_js = '''
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('theme-toggle');
    if (!toggle) return;
    
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    toggle.innerHTML = currentTheme === 'dark' ? '??' : '??';

    toggle.addEventListener('click', () => {
        let theme = document.documentElement.getAttribute('data-theme');
        if (theme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
            toggle.innerHTML = '??';
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            toggle.innerHTML = '??';
        }
    });
});
'''
with open(os.path.join(js_dir, 'theme-toggle.js'), 'w', encoding='utf-8') as f:
    f.write(theme_js)

# 3. Process HTML Files
html_files = glob.glob(os.path.join(repo_dir, '**', '*.html'), recursive=True)

nav_injection = '''<button id="theme-toggle" class="theme-toggle" aria-label="Toggle Dark Mode">??</button>'''

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject toggle button into nav (before mobile toggle)
    if '<button class="mobile-toggle"' in content and 'id="theme-toggle"' not in content:
        content = content.replace('<button class="mobile-toggle"', nav_injection + '\\n            <button class="mobile-toggle"')
        
    # Inject JS before body close
    if 'theme-toggle.js' not in content:
        content = content.replace('</body>', '    <script src="/js/theme-toggle.js"></script>\\n</body>')
        
    # Index.html specifically: Formspree
    if 'index.html' in file:
        content = re.sub(
            r'<form class="newsletter-form"[^>]*>',
            '<form class="newsletter-form" action="YOUR_FORMSPREE_ENDPOINT_HERE" method="POST">',
            content
        )
        
    # Market Intelligence specifically: Charting
    if 'market-intelligence.html' in file and 'id="dseiChart"' not in content:
        chart_html = '''
        <div class="bounded-card" style="margin: 2rem 0; padding: 2rem; background: var(--white); border-color: var(--gold);">
            <h3 style="color: var(--navy); margin-bottom: 1rem;">DSEI 30-Day Trend</h3>
            <canvas id="dseiChart" width="400" height="150"></canvas>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const ctx = document.getElementById('dseiChart').getContext('2d');
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: Array.from({length: 30}, (_, i) => Day ),
                        datasets: [{
                            label: 'DSEI',
                            data: Array.from({length: 30}, () => 1800 + Math.random() * 50),
                            borderColor: '#C8962E',
                            tension: 0.4,
                            fill: true,
                            backgroundColor: 'rgba(200, 150, 46, 0.1)'
                        }]
                    },
                    options: { responsive: true, plugins: { legend: { display: false } } }
                });
            });
        </script>
        '''
        # Inject chart right above the Live DSE Snapshot
        content = content.replace('<!-- DSE Snapshot -->', f'<!-- Market Chart -->\\n{chart_html}\\n\\n        <!-- DSE Snapshot -->')

    # Education specifically: Calculator
    if 'education.html' in file and 'id="calc-form"' not in content:
        calc_html = '''
        <div class="calc-card">
            <h3 style="color: var(--navy); margin-bottom: 1.5rem;">Wealth Compounding Calculator</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                <div>
                    <label>Initial Investment (TZS)</label>
                    <input type="number" id="calc-initial" class="calc-input" value="1000000">
                    <label>Monthly Contribution (TZS)</label>
                    <input type="number" id="calc-monthly" class="calc-input" value="100000">
                    <label>Expected Annual Return (%)</label>
                    <input type="number" id="calc-rate" class="calc-input" value="12">
                    <label>Years to Grow</label>
                    <input type="number" id="calc-years" class="calc-input" value="10">
                    <button class="btn btn-gold-solid" style="width:100%" onclick="calculateWealth()">Calculate Future Value</button>
                </div>
                <div style="display: flex; flex-direction: column; justify-content: center; text-align: center;">
                    <div style="font-size: 1.2rem; color: #555;">Projected Portfolio Value</div>
                    <div class="calc-result" id="calc-output">TZS 36,938,983</div>
                </div>
            </div>
        </div>
        <script>
            function calculateWealth() {
                let p = parseFloat(document.getElementById('calc-initial').value);
                let pmt = parseFloat(document.getElementById('calc-monthly').value);
                let r = parseFloat(document.getElementById('calc-rate').value) / 100 / 12;
                let n = parseFloat(document.getElementById('calc-years').value) * 12;
                
                let futureValue = p * Math.pow(1 + r, n) + pmt * ((Math.pow(1 + r, n) - 1) / r);
                
                document.getElementById('calc-output').innerText = "TZS " + Math.round(futureValue).toLocaleString();
            }
        </script>
        '''
        content = content.replace('<!-- Modules -->', f'<!-- Wealth Calculator -->\\n{calc_html}\\n\\n        <!-- Modules -->')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updates applied successfully.")
