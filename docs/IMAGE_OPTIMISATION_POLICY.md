# Image Optimisation Policy

To preserve Core Web Vitals and maintain the site's exceptional performance, all images must adhere to the following standards:

## 1. Format
- **Primary:** WebP (or AVIF for modern browsers with fallback).
- **Fallback:** JPEG for photographs, PNG for graphics with transparency.

## 2. Responsive Images
- Use `srcset` with multiple widths (e.g., `400w`, `800w`, `1200w`) and `sizes` attribute.
- Example:
  ```html
  <img
    src="image-800w.webp"
    srcset="image-400w.webp 400w, image-800w.webp 800w, image-1200w.webp 1200w"
    sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 800px"
    alt="Description"
    loading="lazy"
    decoding="async"
  />
  ```

## 3. Lazy Loading
- All non-LCP images must use `loading="lazy"`.
- Hero images (above the fold) can use `loading="eager"` but should be highly optimised.

## 4. CDN Optimisation
- If using Cloudflare, enable Polish and Mirage for automatic image optimisation.
- Consider using Cloudflare Images or a dedicated image CDN for larger libraries.

## 5. File Size Limits
- Maximum size for decorative images: 200KB.
- Maximum size for hero images: 500KB (with WebP).

## 6. Accessibility
- Every `<img>` must have an `alt` attribute with meaningful description.
- Decorative images can use `alt=""`.

*Last Updated: 30 August 2026*
