import os
import re

css_append = """
/* 1. Homepage Principles Background */
.why-section {
    background-color: var(--navy, #001f3f) !important;
}
.why-section .section-title, 
.why-section .section-eyebrow, 
.why-section h3, 
.why-section p {
    color: var(--cream, #fdfbf7) !important;
}
.why-card {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255,255,255, 0.1) !important;
}

/* 2. Daily DSE Wrap Redesign */
.home-teaser, .teaser-premium {
    background: linear-gradient(145deg, var(--navy, #001f3f), #0a1128) !important;
    border: 1px solid var(--gold, #c5a059) !important;
    border-radius: 8px !important;
    padding: 4rem 2rem !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15) !important;
    color: var(--cream, #fdfbf7) !important;
}
.home-teaser .section-title, .home-teaser .section-eyebrow {
    color: var(--cream, #fdfbf7) !important;
}
.teaser-premium {
    display: block !important;
    text-align: center !important;
}
.teaser-prem-left, .teaser-prem-right {
    color: var(--cream, #fdfbf7) !important;
    width: 100% !important;
    text-align: center !important;
}
.teaser-prem-eyebrow .teaser-prem-label, .teaser-prem-date {
    color: var(--gold, #c5a059) !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}
.teaser-prem-title {
    color: white !important;
    font-family: var(--font-serif, 'Cormorant Garamond', serif) !important;
    font-size: 2.5rem !important;
    line-height: 1.2 !important;
    margin: 1.5rem auto !important;
    max-width: 800px !important;
}
.teaser-prem-body {
    color: #e0e0e0 !important;
    font-size: 1.2rem !important;
    line-height: 1.8 !important;
    margin: 0 auto 2rem auto !important;
    max-width: 700px !important;
}
.teaser-prem-readmore {
    background-color: var(--gold, #c5a059) !important;
    color: var(--navy, #001f3f) !important;
    border-radius: 4px !important;
    padding: 12px 32px !important;
    font-weight: 700 !important;
    text-decoration: none !important;
    display: inline-block !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

/* 3. Global Mobile Responsiveness */
@media (max-width: 768px) {
    .mi-layout, .snapshot-grid, .archive-row {
        grid-template-columns: 1fr !important;
        display: flex !important;
        flex-direction: column !important;
        width: 100% !important;
    }
    body {
        overflow-x: hidden !important;
    }
    img, table, .container, .section {
        max-width: 100% !important;
    }
}

/* 4. Bond Calculator Table Alignment */
#amortization-schedule table {
    width: 100% !important;
    table-layout: fixed !important;
}
#amortization-schedule th, #amortization-schedule td {
    text-align: right !important;
    padding: 12px 16px !important;
}
#amortization-schedule th:first-child, #amortization-schedule td:first-child {
    text-align: left !important;
}

/* 5. About Page Core Purpose Redesign */
.ab-hero-inner {
    display: block !important;
    text-align: center !important;
    max-width: 900px !important;
    margin: 0 auto !important;
    border: none !important;
}
.ab-hero-inner::before, .ab-hero-inner::after, .ab-hero::before, .ab-hero::after {
    display: none !important; /* Remove any CSS drawn center dividers */
}
.ab-hero-eyebrow {
    color: var(--gold, #c5a059) !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    margin-bottom: 2rem !important;
}
.ab-hero-inner h1 {
    font-family: var(--font-serif, 'Cormorant Garamond', serif) !important;
    font-size: 4rem !important;
    line-height: 1.1 !important;
    margin-bottom: 2rem !important;
}
.ab-hero-inner h1 span {
    color: var(--gold, #c5a059) !important;
}
.ab-hero-bar {
    display: none !important; /* Remove center divider */
}
.ab-mission-card {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin-top: 3rem !important;
}
.ab-mission-card p {
    font-family: var(--font-serif, 'Cormorant Garamond', serif) !important;
    font-size: 2rem !important;
    line-height: 1.6 !important;
    color: var(--gray-dark, #333) !important;
    margin-bottom: 1.5rem !important;
}
.ab-mission-card p strong {
    color: var(--navy, #001f3f) !important;
    font-weight: 600 !important;
}
.ab-hero-sub {
    display: none !important;
}
"""

with open('style.css', 'a', encoding='utf-8') as f:
    f.write(css_append)

print("Updated style.css")

count = 0
for root, dirs, files in os.walk('.'):
    if '.git' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            new_content = re.sub(r'style\.css\?v=[^"\'\s>]+', 'style.css?v=20260830_final_master', content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1

print(f"Updated cache busters in {count} HTML files.")
