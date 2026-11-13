// Render a publication HTML file to PDF with Chromium (Playwright).
// Usage: node publications/render_pdf.js input.html output.pdf
'use strict';
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const [input, output] = process.argv.slice(2);
  if (!input || !output) { console.error('Usage: node render_pdf.js input.html output.pdf'); process.exit(2); }
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(input), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const missing = await page.evaluate(() => {
    const need = ['800 16px Archivo', '400 16px Archivo', '400 16px "IBM Plex Mono"'];
    return need.filter((f) => !document.fonts.check(f));
  });
  if (missing.length) { console.error('Fonts not loaded:', missing.join(', ')); process.exit(1); }
  await page.pdf({ path: output, preferCSSPageSize: true, printBackground: true, tagged: true, outline: true });
  await browser.close();
  console.log('wrote', output);
})();
