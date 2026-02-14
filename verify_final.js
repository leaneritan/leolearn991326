const { chromium } = require('playwright');
const path = require('path');

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();

    // Serve the app folder using a simple server
    const { spawn } = require('child_process');
    const server = spawn('python3', ['-m', 'http.server', '8080'], { cwd: path.join(__dirname, 'app') });

    await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for server

    await page.goto('http://localhost:8080');

    // Wait for content
    await page.waitForSelector('.nav-item');

    // 1. Mark page 1 as finished
    await page.click('#mark-complete');
    await page.waitForTimeout(500);

    // 2. Search for "Noun"
    await page.fill('#search', 'Noun');
    await page.waitForSelector('#search-results:not(.hidden)');

    // Take screenshot
    await page.screenshot({ path: '/home/jules/verification/final_app.png', fullPage: true });

    console.log('Final verification screenshot taken');

    server.kill();
    await browser.close();
})();
