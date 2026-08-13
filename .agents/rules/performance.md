# Website Performance Rule

**Critical Directive**: When making any updates to this website (HTML, CSS, JS, or assets), you MUST prioritize fast page load times and optimal web performance. 

## Guidelines:
1. **No Bloat**: Do not add unnecessary third-party scripts, large unoptimized images, or heavy libraries unless explicitly requested.
2. **Minification**: Keep CSS and JS additions concise. If there is a build step or minified file (e.g., `style.min.css`), ensure it remains optimized.
3. **Asset Optimization**: Any new images must be properly compressed, appropriately sized, and use modern formats (like WebP) where applicable.
4. **Performance Budgets**: Ensure that DOM size remains reasonable and that no new render-blocking resources are added to the `<head>` unless absolutely necessary.
5. **Efficiency**: When adding DOM elements, reuse existing CSS classes instead of adding large blocks of inline styles or redundant CSS rules.
