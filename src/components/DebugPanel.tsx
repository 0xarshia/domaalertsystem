import { useState } from 'react'

const DebugPanel = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [debugData, setDebugData] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const testApiResponse = async () => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await fetch('http://localhost:5000/api/test-api-response')
      const data = await response.json()
      
      if (data.success) {
        setDebugData(data)
      } else {
        setError(data.error || 'Unknown error')
      }
    } catch (err) {
      setError(`Network error: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="macos-glass rounded-lg">
      <div className="bg-white/5 px-4 py-3 border-b border-white/10 rounded-t-lg">
        <h3 className="text-lg font-semibold text-white">🔍 Debug Panel</h3>
      </div>
      
      <div className="p-6">
        <p className="text-blue-200 mb-4 text-sm font-medium">
          Test the API response to see what domain names look like and debug filtering issues.
        </p>
        
        <button
          onClick={testApiResponse}
          disabled={isLoading}
          className="w-full px-6 py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-all duration-200 disabled:opacity-50 macos-button"
        >
          {isLoading ? 'Testing API...' : 'Test API Response'}
        </button>
        
        {error && (
          <div className="mt-4 p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
            <p className="text-red-300 font-medium">Error: {error}</p>
          </div>
        )}
        
        {debugData && (
          <div className="mt-6 space-y-4">
            <div className="bg-white/5 border border-white/10 p-4 rounded-lg">
              <h4 className="text-white font-semibold mb-2">Domain Information</h4>
              <p className="text-white/80 text-sm">
                <strong>Domain Name:</strong> {debugData.domain_name || 'NOT_FOUND'}
              </p>
              <p className="text-white/80 text-sm">
                <strong>Domain Length:</strong> {debugData.domain_length}
              </p>
              <p className="text-white/80 text-sm">
                <strong>Detected Extensions:</strong> {debugData.domain_extensions.join(', ') || 'None'}
              </p>
            </div>
            
            <div className="bg-white/5 border border-white/10 p-4 rounded-lg">
              <h4 className="text-white font-semibold mb-2">Token Information</h4>
              <p className="text-white/80 text-sm">
                <strong>Token Address:</strong> {debugData.extracted_data?.token_address || 'NOT_FOUND'}
              </p>
              {debugData.extracted_data?.token_address && (
                <p className="text-white/80 text-sm">
                  <strong>Explorer Link:</strong> 
                  <a 
                    href={`https://explorer-testnet.doma.xyz/address/${debugData.extracted_data.token_address}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300 underline ml-1"
                  >
                    View Token Address
                  </a>
                </p>
              )}
              <p className="text-white/80 text-sm">
                <strong>Price (ETH):</strong> {debugData.extracted_data?.price ? (debugData.extracted_data.price / 1e18).toFixed(6) : 'NOT_FOUND'}
              </p>
            </div>
            
            {debugData.all_addresses_found && debugData.all_addresses_found.length > 0 && (
              <div className="bg-white/5 border border-white/10 p-4 rounded-lg">
                <h4 className="text-white font-semibold mb-2">All Addresses Found in Response</h4>
                <div className="space-y-2">
                  {debugData.all_addresses_found.map((address, index) => (
                    <div key={index} className="bg-white/5 p-2 rounded text-xs">
                      <p className="text-white/80">
                        <strong>Field:</strong> <span className="text-blue-400">{address.field_name}</span>
                      </p>
                      <p className="text-white/80">
                        <strong>Path:</strong> <span className="text-green-400">{address.path}</span>
                      </p>
                      <p className="text-white/80">
                        <strong>Value:</strong> <span className="text-yellow-400 font-mono">{address.value}</span>
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            <div className="bg-white/5 border border-white/10 p-4 rounded-lg">
              <h4 className="text-white font-semibold mb-2">Extracted Data</h4>
              <pre className="text-white/80 text-xs overflow-auto">
                {JSON.stringify(debugData.extracted_data, null, 2)}
              </pre>
            </div>
            
            <div className="bg-white/5 border border-white/10 p-4 rounded-lg">
              <h4 className="text-white font-semibold mb-2">Raw API Response</h4>
              <pre className="text-white/80 text-xs overflow-auto max-h-64">
                {JSON.stringify(debugData.raw_response, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default DebugPanel
