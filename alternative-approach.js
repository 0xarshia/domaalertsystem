import fetch from 'node-fetch';

const API_KEY = 'v1.d25826e8ff3c9607022227c25f76cccafba3a13b0514977d02616ce1b98fa23c';

// Try different endpoints or approaches
const endpoints = [
  'https://api-testnet.doma.xyz/v1/poll?eventTypes=NAME_TOKENIZED&limit=1',
  'https://api.doma.xyz/v1/poll?eventTypes=NAME_TOKENIZED&limit=1', // Try production endpoint
  'https://testnet.doma.xyz/api/v1/poll?eventTypes=NAME_TOKENIZED&limit=1' // Alternative path
];

const makeRequest = async (url, attempt = 1) => {
  console.log(`🔍 Attempt ${attempt} - Trying: ${url}`);
  
  try {
    // Very realistic browser headers
    const headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'en-US,en;q=0.9',
      'Accept-Encoding': 'gzip, deflate, br',
      'DNT': '1',
      'Connection': 'keep-alive',
      'Upgrade-Insecure-Requests': '1',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'cross-site',
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache',
      'Referer': 'https://doma.xyz/',
      'Origin': 'https://doma.xyz',
      'Api-Key': API_KEY,
      'Content-Type': 'application/json'
    };

    const response = await fetch(url, {
      method: 'GET',
      headers,
      redirect: 'follow',
      follow: 5,
      timeout: 20000
    });

    console.log(`Status: ${response.status} ${response.statusText}`);
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ SUCCESS! API Response:\n', JSON.stringify(data, null, 2));
      return true;
    } else {
      const errorText = await response.text();
      console.log(`❌ Failed: ${errorText.substring(0, 100)}...`);
      return false;
    }
  } catch (error) {
    console.error(`❌ Error:`, error.message);
    return false;
  }
};

(async () => {
  console.log('🚀 Trying alternative approaches...\n');
  
  for (const endpoint of endpoints) {
    const success = await makeRequest(endpoint);
    if (success) {
      console.log('🎉 Found working endpoint!');
      process.exit(0);
    }
    console.log('---\n');
  }
  
  console.log('💡 All endpoints failed. Possible solutions:');
  console.log('1. Your IP might be temporarily blocked by Cloudflare');
  console.log('2. Try using a VPN to change your IP address');
  console.log('3. Wait 15-30 minutes and try again');
  console.log('4. Contact Doma support for proper API access');
  console.log('5. Check if you need to register your IP with Doma');
})();
