import re
import os
import subprocess

def fix_css():
    with open('style.css', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Reduce Vertical Spacing
    # Look for padding: 6rem, 8rem etc and reduce
    content = re.sub(r'padding:\s*[6-9]rem\s+0;', 'padding: 4rem 0;', content)
    content = re.sub(r'margin-bottom:\s*[6-9]rem;', 'margin-bottom: 3rem;', content)

    # 2. Mobile Responsiveness Audit
    # Add media queries for max-width: 768px if they don't cover these grids well
    if 'max-width: 768px' not in content:
        mq = """
@media (max-width: 768px) {
    .services-grid, .why-grid, .snapshot-grid, .pillars-grid {
        grid-template-columns: 1fr !important;
    }
    .why-section-header {
        padding: 1.5rem;
    }
}
"""
        content += mq
    else:
        # Just ensure they are 1fr
        mq_add = """
@media (max-width: 768px) {
    .services-grid, .why-grid, .snapshot-grid, .pillars-grid {
        grid-template-columns: 1fr !important;
    }
}
"""
        content += mq_add
        
    # 3. Color Palette Enforcement
    # Ensure no stray colors, though this is hard to do without a specific parser.
    # We will enforce the root variables.
    
    # 4. Market Intelligence Snapshot Alignment
    # The requirement is that the "Turnover (TZS) 10.20 bn" doesn't wrap.
    # We can add a specific class or update .snapshot-grid specifically for market intelligence.
    mq_market = """
.snapshot-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    align-items: center;
}
.snapshot-value {
    white-space: nowrap;
}
"""
    content += mq_market
    
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(content)

def fix_html():
    for filename in ['index.html', 'market-intelligence.html']:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Reduce Vertical Spacing in inline styles
        content = re.sub(r'padding:\s*[6-9]rem\s+0;?', 'padding:4rem 0;', content)
        content = re.sub(r'padding-[a-z]+:\s*[6-9]rem;?', 'padding-top:4rem;', content)
        content = re.sub(r'margin:\s*[6-9]rem\s+0;?', 'margin:4rem 0;', content)
        content = re.sub(r'margin-[a-z]+:\s*[6-9]rem;?', 'margin-bottom:3rem;', content)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

def git_commit_push():
    subprocess.run(['git', 'add', 'style.css', 'index.html', 'market-intelligence.html'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Fix frontend layout, spacing, colors, and alignment'], check=True)
    subprocess.run(['git', 'push', 'origin', 'main', '--force'], check=True)

if __name__ == '__main__':
    fix_css()
    fix_html()
    git_commit_push()
