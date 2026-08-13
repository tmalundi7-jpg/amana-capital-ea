# Daily DSE Wrap Updates

When updating the Daily DSE Wrap and creating new HTML files, follow these guidelines to prevent duplication and date errors:

1. **Avoid Duplicate Headers**: 
   When copying from a previous day's template (e.g., `dse-wrap-2026-08-12.html`), ensure you replace the EXACT `<div class="dse-header-box">` and its contents rather than appending to it. Be careful not to leave behind the old title/subtitle.
   
2. **Update the Dates Accurately**: 
   When generating a new wrap, remember to update the dates in the following places:
   - The `<title>` tag of the new HTML file.
   - The `<div class="dse-header-box">` heading in the new HTML file.
   - The "Daily DSE Wrap Archive" section preview inside `market-intelligence.html`. Make sure the `archive-date` div and the `href` link both reflect the NEW date.
   - The `market-intelligence-archive.html` file, by moving the *previous* day's wrap into the archive list and ensuring the date is correctly labeled.

3. **Preserve Rich Text Formatting and Interactive Elements**:
   When extracting content from the daily wrap `.docx` source files (e.g. `Daily DSE Wrap [Date].docx`), you must ensure that all formatting is faithfully preserved. This includes:
   - **Bold text**: Highlighted or bolded text in the source (for example, "Upper limit: ..." and "Lower limit: ...") must be wrapped in `<strong>` tags in the HTML.
   - **Italics**: Preserve `<em>` tags where appropriate.
   - **Links and Interactive Elements**: Any hyperlinks or interactive parts meant to link between other pages in the website must be adhered to and correctly formatted as `<a href="...">` in the HTML. 
   Do not just extract raw plain text if it strips away these important elements.

4. **Performance Preservation**:
   All updates must adhere to the `performance.md` guidelines. Do not include excessive unused CSS, keep image sizes optimized, and do not introduce render-blocking scripts.
