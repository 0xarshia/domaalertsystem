import { useState, useRef } from 'react'

const TelegramButton = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [isConfigured, setIsConfigured] = useState(false)
  const [minPrice, setMinPrice] = useState('')
  const [maxPrice, setMaxPrice] = useState('')
  const [maxLetters, setMaxLetters] = useState('')
  const [domainExtensions, setDomainExtensions] = useState<string[]>([])
  const [keyword, setKeyword] = useState('')
  const [sellerAddress, setSellerAddress] = useState('')
  const [isConfiguring, setIsConfiguring] = useState(false)

  const configureFilter = async () => {
    if (!minPrice && !maxPrice && !maxLetters && domainExtensions.length === 0 && !keyword && !sellerAddress) {
      setMessage('❌ Please configure at least one filter')
      return
    }

    const min = minPrice ? parseFloat(minPrice) : 0
    const max = maxPrice ? parseFloat(maxPrice) : Number.MAX_SAFE_INTEGER

    if (min > max) {
      setMessage('❌ Minimum price cannot be greater than maximum price')
      return
    }

    const maxLetterCount = maxLetters ? parseInt(maxLetters) : null
    if (maxLetterCount && maxLetterCount < 1) {
      setMessage('❌ Maximum letters must be at least 1')
      return
    }

    setIsConfiguring(true)
    setMessage('🔄 Configuring advanced filters...')

    try {
      const response = await fetch('http://localhost:5000/api/configure-filter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          minPrice: min,
          maxPrice: max,
          maxLetters: maxLetterCount,
          domainExtensions: domainExtensions,
          keyword: keyword.trim(),
          sellerAddress: sellerAddress.trim()
        })
      })

      if (response.ok) {
        setIsConfigured(true)
        const activeFilters = []
        if (minPrice || maxPrice) activeFilters.push(`Price: ${minPrice || '0'} - ${maxPrice || '∞'} ETH`)
        if (maxLetterCount) activeFilters.push(`Max letters: ${maxLetterCount}`)
        if (domainExtensions.length > 0) activeFilters.push(`Extensions: ${domainExtensions.join(', ')}`)
        if (keyword) activeFilters.push(`Keyword: "${keyword}"`)
        if (sellerAddress) activeFilters.push(`Seller: ${sellerAddress}`)
        
        setMessage(`✅ Advanced filters configured! Active filters: ${activeFilters.join(' | ')}`)
      } else {
        const errorData = await response.json()
        setMessage(`❌ Failed to configure filters: ${errorData.error}`)
      }
    } catch (error) {
      setMessage(`❌ Error configuring filters: ${error}`)
    } finally {
      setIsConfiguring(false)
    }
  }

  const resetFilter = () => {
    setMinPrice('')
    setMaxPrice('')
    setMaxLetters('')
    setDomainExtensions([])
    setKeyword('')
    setSellerAddress('')
    setIsConfigured(false)
    setMessage('')
  }

  const toggleDomainExtension = (extension: string) => {
    setDomainExtensions(prev => 
      prev.includes(extension) 
        ? prev.filter(ext => ext !== extension)
        : [...prev, extension]
    )
  }

  return (
    <div className="macos-glass rounded-lg">
      <div className="bg-white/5 px-4 py-3 border-b border-white/10 rounded-t-lg">
        <h3 className="text-lg font-semibold text-white">Advanced Filter Configuration</h3>
      </div>
      
      <div className="p-6">
        <p className="text-blue-200 mb-6 text-sm font-medium">
          Configure advanced filters for the bot. The bot will only send messages for events that match your specified criteria.
        </p>
        
        <div className="space-y-6">
          {/* Price Range */}
          <div>
            <h4 className="text-md font-semibold text-white mb-3">💰 Price Range</h4>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-white/80 mb-2">
                  Minimum Price (ETH)
                </label>
                <input
                  type="number"
                  step="0.001"
                  placeholder="0.001"
                  value={minPrice}
                  onChange={(e) => setMinPrice(e.target.value)}
                  className="w-full px-4 py-3 bg-white/5 border border-white/20 text-white placeholder-white/40 focus:outline-none focus:border-blue-400 font-mono rounded-lg macos-input"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-white/80 mb-2">
                  Maximum Price (ETH)
                </label>
                <input
                  type="number"
                  step="0.001"
                  placeholder="10.0"
                  value={maxPrice}
                  onChange={(e) => setMaxPrice(e.target.value)}
                  className="w-full px-4 py-3 bg-white/5 border border-white/20 text-white placeholder-white/40 focus:outline-none focus:border-blue-400 font-mono rounded-lg macos-input"
                />
              </div>
            </div>
          </div>

          {/* Domain Filters */}
          <div>
            <h4 className="text-md font-semibold text-white mb-3">🌐 Domain Filters</h4>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-white/80 mb-2">
                  Maximum Letters in Domain
                </label>
                <input
                  type="number"
                  min="1"
                  placeholder="20"
                  value={maxLetters}
                  onChange={(e) => setMaxLetters(e.target.value)}
                  className="w-full px-4 py-3 bg-white/5 border border-white/20 text-white placeholder-white/40 focus:outline-none focus:border-blue-400 font-mono rounded-lg macos-input"
                />
              </div>
              
              <div>
                <label className="block text-sm font-semibold text-white/80 mb-2">
                  Domain Extensions
                </label>
                <div className="flex flex-wrap gap-2">
                  {['.com', '.ai', '.io', '.org', '.net', '.xyz', '.eth'].map(ext => (
                    <button
                      key={ext}
                      onClick={() => toggleDomainExtension(ext)}
                      className={`px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                        domainExtensions.includes(ext)
                          ? 'bg-blue-600 text-white'
                          : 'bg-white/10 text-white/60 hover:bg-white/20 hover:text-white'
                      }`}
                    >
                      {ext}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-white/80 mb-2">
                  Keyword in Domain
                </label>
                <input
                  type="text"
                  placeholder="ai, crypto, nft..."
                  value={keyword}
                  onChange={(e) => setKeyword(e.target.value)}
                  className="w-full px-4 py-3 bg-white/5 border border-white/20 text-white placeholder-white/40 focus:outline-none focus:border-blue-400 rounded-lg macos-input"
                />
              </div>
            </div>
          </div>

          {/* Seller Address */}
          <div>
            <h4 className="text-md font-semibold text-white mb-3">👤 Seller Address</h4>
            <div>
              <label className="block text-sm font-semibold text-white/80 mb-2">
                Filter by Seller Address
              </label>
              <input
                type="text"
                placeholder="0x1234...abcd"
                value={sellerAddress}
                onChange={(e) => setSellerAddress(e.target.value)}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 text-white placeholder-white/40 focus:outline-none focus:border-blue-400 font-mono rounded-lg macos-input"
              />
            </div>
          </div>
          
          <div className="flex space-x-3">
            <button
              onClick={configureFilter}
              disabled={isConfiguring || (!minPrice && !maxPrice && !maxLetters && domainExtensions.length === 0 && !keyword && !sellerAddress)}
              className={`
                flex-1 px-6 py-4 font-semibold transition-all duration-200 rounded-lg macos-button
                ${isConfiguring || (!minPrice && !maxPrice && !maxLetters && domainExtensions.length === 0 && !keyword && !sellerAddress)
                  ? 'bg-white/10 cursor-not-allowed text-white/40 macos-disabled' 
                  : 'bg-blue-600 hover:bg-blue-700 text-white'
                }
              `}
            >
              {isConfiguring ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin w-5 h-5 border-2 border-white border-t-transparent mr-2"></div>
                  Configuring...
                </div>
              ) : (
                '⚙️ Configure Filter'
              )}
            </button>
            
            {isConfigured && (
              <button
                onClick={resetFilter}
                className="px-6 py-4 bg-red-600 hover:bg-red-700 text-white font-semibold transition-all duration-200 rounded-lg macos-button"
              >
                🔄 Reset
              </button>
            )}
          </div>
          
          {isConfigured && (
            <div className="bg-green-500/10 border border-green-500/20 p-4 rounded-lg">
              <p className="text-green-300 text-sm font-medium">
                ✅ Filter is active! Bot will only send messages for prices between {minPrice || '0'} and {maxPrice || '∞'} ETH
              </p>
            </div>
          )}
        </div>
        
        {message && (
          <div className={`mt-4 p-4 border rounded-lg ${
            message.includes('✅') 
              ? 'bg-green-500/10 border-green-500/20 text-green-300' 
              : 'bg-red-500/10 border-red-500/20 text-red-300'
          }`}>
            <p className="font-medium">{message}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default TelegramButton
