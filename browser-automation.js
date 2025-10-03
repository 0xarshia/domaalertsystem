// This requires: npm install puppeteer
// Uncomment and use if other methods fail

/*
import puppeteer from 'puppeteer';

const API_KEY = 'v1.d25826e8ff3c9607022227c25f76cccafba3a13b0514977d02616ce1b98fa23c';
const url = 'https://api-testnet.doma.xyz/v1/poll?eventTypes=NAME_TOKENIZED&limit=1';

(async () => {
  console.log('🚀 Using browser automation to bypass Cloudflare...');
  
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  try {
    const page = await browser.newPage();
    
    // Set realistic viewport and user agent
    await page.setViewport({ width: 1366, height: 768 });
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
    
    // Make the API request
    const response = await page.goto(url, {
      waitUntil: 'networkidle2',
      headers: {
        'Api-Key': API_KEY,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok()) {
      const content = await page.content();
      console.log('✅ Success! Response:', content);
    } else {
      console.log('❌ Failed with status:', response.status());
    }
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    await browser.close();
  }
})();
*/

console.log('To use browser automation:');
console.log('1. Run: npm install puppeteer');
console.log('2. Uncomment the code above');
console.log('3. Run: node browser-automation.js');
