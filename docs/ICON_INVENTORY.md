# Icon Inventory & Consistency

## Current State
- **Primary Library:** Font Awesome (Free) – detected via `fa-` classes.
- **Secondary Usage:** Inline SVGs in a few places (social icons, brand logo).
- **Consistency Score:** 7/10 – Some icons have different stroke widths and visual weights.

## Recommendations
1. **Standardise on Font Awesome 6 (Free)** for all new icons.
2. **Replace inline SVGs** with Font Awesome equivalents where possible (except brand logo).
3. **Define a restricted icon set** in the design system – no custom one-offs.

## Approved Icon Set
| Purpose | Icon Name | Font Awesome Class |
| :--- | :--- | :--- |
| Market | Trending Up | `fa-solid fa-arrow-trend-up` |
| Calculator | Calculator | `fa-solid fa-calculator` |
| Education | Book Open | `fa-solid fa-book-open` |
| Contact | Envelope | `fa-solid fa-envelope` |

## Action Plan
- Replace any non-standard icons with the approved set.
- Ensure all icons have `aria-hidden="true"` and `role="img"` for accessibility.

---
*Last Updated: 30 August 2026*
