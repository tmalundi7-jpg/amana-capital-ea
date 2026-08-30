import os
import re

CSS_APPEND = '''
/* ========================================================= */
/* LATEST TIER-1 DESIGN UPGRADES - LEAD FRONTEND DEVELOPER   */
/* ========================================================= */

/* 1. Footer Brand Font Upgrade */
.footer-brand, .footer-logo {
    font-family: var(--font-serif, 'Cormorant Garamond', serif) !important;
    font-size: 1.4rem !important;
    letter-spacing: 2px !important;
    font-weight: 600 !important;
    color: var(--gold) !important;
}

/* 2. Newsletter Section Font Upgrade */
.newsletter-premium .section-eyebrow, 
.newsletter-eyebrow,
.newsletter-left .section-eyebrow {
    color: var(--gold) !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}

.newsletter-premium h2, 
.newsletter-left h2,
.newsletter-box h2 {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 3.2rem !important;
    font-weight: 400 !important;
    line-height: 1.1 !important;
}

.newsletter-premium p, 
.newsletter-left p,
.newsletter-box p {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.15rem !important;
    line-height: 1.6 !important;
    color: rgba(251, 247, 240, 0.9) !important;
}

/* 3. Global Numbers Font Upgrade */
.teaser-prem-stat-value,
#amortization-schedule td,
.snapshot-val,
.snapshot-row,
.bc-result-val,
.numerical,
.number-cell {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-variant-numeric: tabular-nums !important;
}

/* 4. Daily DSE Wrap Re-Redesign */
.home-teaser {
    background-color: var(--cream, #fdfbf7) !important;
}

.home-teaser .teaser-premium {
    border: 1px solid var(--gold) !important;
}

.home-teaser .teaser-prem-left {
    background: #fdfbf7 !important; /* Cream */
    color: var(--navy) !important;
    border-right: 1px solid var(--gold) !important;
}

.home-teaser .teaser-prem-left .teaser-prem-title {
    color: var(--navy) !important;
}

.home-teaser .teaser-prem-left .teaser-prem-body {
    color: var(--navy) !important;
}

.home-teaser .teaser-prem-left .teaser-prem-date,
.home-teaser .teaser-prem-left .teaser-prem-stat-label,
.home-teaser .teaser-prem-left .teaser-prem-label {
    color: rgba(11, 29, 58, 0.7) !important; /* Dark gray/navy */
}

.home-teaser .teaser-prem-left .teaser-prem-stat-value {
    color: var(--navy) !important;
}

.home-teaser .teaser-prem-left .teaser-prem-stat-value.gain {
    color: #16a34a !important; /* Dark green on cream */
}

.home-teaser .teaser-prem-left .teaser-prem-stat-value.loss {
    color: #dc2626 !important; /* Dark red on cream */
}
'''

def update_css():
    css_path = "style.css"
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        if "LATEST TIER-1 DESIGN UPGRADES" not in content:
            with open(css_path, "a", encoding="utf-8") as f:
                f.write(CSS_APPEND)
            print("CSS updated successfully.")
        else:
            print("CSS already contains the new styles.")

def update_html_cache_buster():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Update anything like ?v=20260830_final_polish_X to ?v=20260830_final_polish_6
                new_content = re.sub(r"v=20260830_final_polish_\d+", "v=20260830_final_polish_6", content)
                
                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated cache buster in {path}")

if __name__ == '__main__':
    update_css()
    update_html_cache_buster()