// Headless screenshot of dev/preview.html for autonomous visual QA.
// Usage: node dev/shot.mjs  (run from charger-card/, after `npm run build`)
// Serves the dir on a local port, loads preview.html, writes dev/preview.png.
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join } from 'node:path';
const pw = await import('/Users/gbovyn/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js');
const chromium = pw.chromium ?? pw.default?.chromium;

const ROOT = process.cwd();
const PORT = 4178;
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.png': 'image/png', '.mjs': 'text/javascript', '.map': 'application/json' };

const server = createServer(async (req, res) => {
  try {
    const url = req.url.split('?')[0];
    const path = join(ROOT, url === '/' ? 'dev/preview.html' : url);
    const body = await readFile(path);
    res.writeHead(200, { 'content-type': TYPES[extname(path)] || 'application/octet-stream' });
    res.end(body);
  } catch {
    res.writeHead(404); res.end('not found');
  }
});

await new Promise((r) => server.listen(PORT, r));

const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 1200, height: 1000 }, deviceScaleFactor: 2 });
await page.goto(`http://localhost:${PORT}/dev/preview.html`, { waitUntil: 'networkidle' });
await page.waitForTimeout(700); // let curve/ring animations settle
await page.screenshot({ path: 'dev/preview.png', fullPage: true });
await browser.close();
server.close();
console.log('wrote dev/preview.png');
