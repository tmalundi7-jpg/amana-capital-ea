# Daily DSE Wrap Format Specification

This specification defines the exact formatting rules for Daily DSE Wraps on the Amana Capital EA website, based on the 13 August 2026 master reference.

## 1. Page Header & Structure
- **Container:** The content is placed inside a `<div class="card" style="padding: 3rem;">`.
- **Header Box:** 
  - Tag: `<div class="dse-header-box">`
  - Inline Styles: `background-color: var(--cream); border: 1px solid rgba(200, 150, 46, 0.3); border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; display: flex; flex-direction: column; gap: 0.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05);`
- **Main Heading (H1):**
  - Text: `Daily DSE Wrap | [Day, Date]`
  - Inline Styles: `margin-top: 0; color: var(--navy); font-size: 2.2rem; margin-bottom: 0.5rem;`
- **Subtitle / Secondary Heading:**
  - Tag: `<p>`
  - Inline Styles: `font-size: 1.1rem; color: var(--mist); margin-bottom: 0; font-weight: 600;`

## 2. Section Headings (H2)
- **Tag:** `<h2>`
- **Inline Styles:** `color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.5rem;`
- **Usage:** Used for all main numbered sections (e.g., "1. Market Snapshot").

## 3. Body Text & Paragraphs
- **Tag:** `<p>`
- No inline styles required for standard paragraphs.
- Emphasis is handled with standard `<em>` or `<strong>` tags.
- Links are standard `<a>` tags with `target="_blank"` where applicable.

## 4. Tables
- **Wrapper:** `<div class="table-responsive" style="overflow-x: auto; margin-bottom: 1rem;">`
- **Table Element:** `<table class="data-table" style="width: 100%; border-collapse: collapse;">`
- **Table Header (thead > tr):**
  - Inline Styles: `background-color: var(--navy); color: var(--white); text-align: left;`
  - **th cells:** `style="padding: 1rem;"`
- **Table Body (tbody > tr):**
  - **Even rows:** Standard `<tr>`
  - **Odd rows (alternating):** `<tr style="background-color: var(--cream);">`
  - **td cells:** `style="padding: 1rem;"`
- **Data Highlighting (within td):**
  - **Positive Change (Gain):** Add `color: var(--gain); font-weight: 600;` to the td style.
  - **Negative Change (Loss):** Add `color: var(--loss); font-weight: 600;` to the td style.
  - **First Column (Metric/Ticker):** Use `font-weight: 600;` on the td and wrap text in `<strong style="color: #000;">`.

## 5. Lists
- Use standard `<ul>` and `<li>` tags for bulleted lists.

## 6. Highlighted Blocks (e.g., Multi-Year Framework)
- **Wrapper:** `<div style="background: var(--cream); border-left: 4px solid var(--gold); padding: 2rem; border-radius: 4px; margin-top: 3rem;">`
- **Internal Heading (H3):** `<h3 style="color: var(--navy); margin-top: 0; font-size: 1.4rem;">`
- **Internal Paragraph:** `<p style="margin-bottom: 0;">`

## 7. Disclaimer
- **Wrapper:** `<div class="article-disclaimer" style="margin-top: 3rem; font-size: 0.85rem; color: #666; border-top: 1px solid var(--stone); padding-top: 1rem;">`
- **Content:** Wrapped in `<p><em>...</em></p>`
