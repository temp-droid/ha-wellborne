// Focused high-res screenshot of the first (charging/dark) card for detailed QA.
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join } from 'node:path';
const pw = await import('/Users/gbovyn/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js');
const chromium = pw.chromium ?? pw.default?.chromium;
const ROOT = process.cwd();
const PORT = 4179;
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.map': 'application/json' };
const server = createServer(async (req, res) => {
  try {
    const url = req.url.split('?')[0];
    const path = join(ROOT, url === '/' ? 'dev/preview.html' : url);
    const body = await readFile(path);
    res.writeHead(200, { 'content-type': TYPES[extname(path)] || 'application/octet-stream' });
    res.end(body);
  } catch { res.writeHead(404); res.end('nf'); }
});
await new Promise((r) => server.listen(PORT, r));
const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 800, height: 900 }, deviceScaleFactor: 3 });
await page.goto(`http://localhost:${PORT}/dev/preview.html`, { waitUntil: 'networkidle' });
await page.waitForTimeout(700);
const card = page.locator('.theme-dark ha-card').first();
await card.screenshot({ path: 'dev/card1.png' });
await browser.close();
server.close();
console.log('wrote dev/card1.png');
