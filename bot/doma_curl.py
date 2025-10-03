import subprocess
import json
import sys

API_KEY = "v1.d25826e8ff3c9607022227c25f76cccafba3a13b0514977d02616ce1b98fa23c"
URL = "https://api-testnet.doma.xyz/v1/poll?eventTypes=NAME_TOKENIZATION_REQUESTED&limit=1"

def test_with_curl():
    """Test using curl command directly"""
    print("🚀 Testing with curl command...")
    
    try:
        # Build curl command
        cmd = [
            'curl',
            URL,
            '--header', f'Api-Key: {API_KEY}'
        ]
        
        print(f"Running: {' '.join(cmd)}")
        
        # Execute curl command
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        print(f"Return code: {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        if result.stderr:
            print(f"STDERR: {result.stderr}")
        
        if result.returncode == 0:
            try:
                # Try to parse as JSON
                json_data = json.loads(result.stdout)
                print("✅ SUCCESS! API Response:")
                print(json.dumps(json_data, indent=2))
                return True
            except json.JSONDecodeError:
                print("✅ SUCCESS! API Response (raw):")
                print(result.stdout)
                return True
        else:
            print("❌ Curl command failed")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Curl command timed out")
        return False
    except FileNotFoundError:
        print("❌ Curl not found. Please install curl or use the Python version.")
        return False
    except Exception as e:
        print(f"❌ Error running curl: {e}")
        return False

def test_with_requests():
    """Test using requests library (mimicking curl)"""
    print("\n🚀 Testing with requests library (mimicking curl)...")
    
    try:
        import requests
        
        headers = {
            'Api-Key': API_KEY
        }
        
        response = requests.get(URL, headers=headers, timeout=15)
        
        print(f"Status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                json_data = response.json()
                print("✅ SUCCESS! API Response:")
                print(json.dumps(json_data, indent=2))
                return True
            except json.JSONDecodeError:
                print("✅ SUCCESS! API Response (raw):")
                print(response.text)
                return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except ImportError:
        print("❌ Requests library not found. Install with: pip install requests")
        return False
    except Exception as e:
        print(f"❌ Error with requests: {e}")
        return False

def test_with_http_client():
    """Test using http.client (mimicking curl)"""
    print("\n🚀 Testing with http.client (mimicking curl)...")
    
    try:
        import http.client
        import gzip
        import zlib
        
        # Parse URL
        conn = http.client.HTTPSConnection("api-testnet.doma.xyz")
        
        headers = {
            'Api-Key': API_KEY
        }
        
        # Make request
        conn.request("GET", "/v1/poll?eventTypes=NAME_TOKENIZATION_REQUESTED&limit=1", headers=headers)
        
        response = conn.getresponse()
        data = response.read()
        
        print(f"Status: {response.status} {response.reason}")
        
        # Handle compression
        content_encoding = response.getheader('Content-Encoding', '').lower()
        if content_encoding == 'gzip':
            data = gzip.decompress(data)
        elif content_encoding == 'deflate':
            data = zlib.decompress(data)
        
        response_text = data.decode('utf-8')
        
        if response.status == 200:
            try:
                json_data = json.loads(response_text)
                print("✅ SUCCESS! API Response:")
                print(json.dumps(json_data, indent=2))
                return True
            except json.JSONDecodeError:
                print("✅ SUCCESS! API Response (raw):")
                print(response_text)
                return True
        else:
            print(f"❌ Error {response.status}: {response_text}")
            return False
            
    except Exception as e:
        print(f"❌ Error with http.client: {e}")
        return False
    finally:
        try:
            conn.close()
        except:
            pass

if __name__ == "__main__":
    print("Testing Doma API with different Python approaches...\n")
    
    # Test 1: Direct curl command
    success = test_with_curl()
    
    if not success:
        # Test 2: Requests library
        success = test_with_requests()
    
    if not success:
        # Test 3: http.client
        success = test_with_http_client()
    
    if success:
        print("\n🎉 Found a working method!")
    else:
        print("\n💡 All methods failed. The API might be temporarily unavailable.")
