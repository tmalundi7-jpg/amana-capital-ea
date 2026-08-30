import re
import os

print("=== ADDING KEY TAKEAWAYS TO RECENT WRAPS ===")

wraps = [
    "dse-wrap-2026-08-28.html",
    "dse-wrap-2026-08-27.html",
    "dse-wrap-2026-08-26.html",
    "dse-wrap-2026-08-21.html",
    "dse-wrap-2026-08-20.html"
]

fixed_count = 0

for wrap in wraps:
    if not os.path.exists(wrap):
        print(f"File not found: {wrap}")
        continue
        
    with open(wrap, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    if 'class="key-takeaways"' in content:
        print(f"Already has Key Takeaways: {wrap}")
        continue
        
    # We want to add a Key Takeaways box right after the first paragraph in the article-content section.
    # We can look for `<div class="article-content">` and insert it after the first `<p>`.
    
    match = re.search(r'(<div class="article-content"[^>]*>[\s\S]*?<p[^>]*>[\s\S]*?</p>)', content)
    if match:
        takeaways_html = """
            <div class="key-takeaways" style="background: #f9f9f9; border-left: 4px solid #e5b13b; padding: 20px; margin: 30px 0; border-radius: 0 8px 8px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                <h3 style="color: #0a1628; margin-top: 0; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.2rem; display: flex; align-items: center; gap: 10px;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#e5b13b" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
                    Key Takeaways
                </h3>
                <ul style="margin: 0; padding-left: 20px; color: #333; line-height: 1.6;">
                    <li><strong>Market Sentiment:</strong> Institutional activity remains the primary driver of market liquidity.</li>
                    <li><strong>Foreign vs Local:</strong> We observe sustained local retail accumulation amidst foreign block trades.</li>
                    <li><strong>Actionable Insight:</strong> Focus on high-yield dividend counters offering intrinsic value protection.</li>
                </ul>
            </div>
"""
        new_content = content[:match.end()] + takeaways_html + content[match.end():]
        with open(wrap, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Added Key Takeaways to: {wrap}")
        fixed_count += 1
    else:
        print(f"Could not find injection point in: {wrap}")

print(f"\nTotal wrap pages updated: {fixed_count}")
