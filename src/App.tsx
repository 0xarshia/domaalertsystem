import { WagmiProvider } from 'wagmi'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { config } from './lib/wagmi'
import WalletConnect from './components/WalletConnect'
import BuyPlan from './components/BuyPlan'
import TelegramButton from './components/TelegramButton'
import FilteredPolling from './components/FilteredPolling'
import DebugPanel from './components/DebugPanel'
import { useState } from 'react'

const queryClient = new QueryClient()

function App() {
  const [activeTab, setActiveTab] = useState('wallet')

  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
          {/* macOS style menu bar */}
          <div className="bg-black/20 backdrop-blur-md border-b border-white/10 h-8 flex items-center px-4">
            <div className="flex space-x-2">
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            </div>
            <div className="flex-1 text-center">
              <span className="text-white/80 text-sm font-medium">Doma Alert System</span>
            </div>
          </div>

          {/* Main content area */}
          <div className="flex items-center justify-center min-h-[calc(100vh-2rem)] p-8">
            <div className="w-full max-w-4xl">
              {/* macOS style window */}
              <div className="macos-window">
                <div className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 px-6 py-4 border-b border-white/10 rounded-t-12">
                  <h1 className="text-2xl font-semibold text-white">
                    Doma Alert System
                  </h1>
                  <p className="text-white/60 text-sm mt-1">Advanced Price Monitoring & Filtering</p>
                </div>
                
                {/* Tab Navigation */}
                <div className="bg-black/20 backdrop-blur-md border-b border-white/10">
                  <div className="flex">
                    <button
                      onClick={() => setActiveTab('wallet')}
                      className={`px-6 py-4 font-medium transition-all duration-200 border-r border-white/10 ${
                        activeTab === 'wallet'
                          ? 'bg-white/10 text-white'
                          : 'text-white/60 hover:text-white hover:bg-white/5'
                      }`}
                    >
                      💼 Wallet & Plan
                    </button>
                    <button
                      onClick={() => setActiveTab('alerts')}
                      className={`px-6 py-4 font-medium transition-all duration-200 ${
                        activeTab === 'alerts'
                          ? 'bg-white/10 text-white'
                          : 'text-white/60 hover:text-white hover:bg-white/5'
                      }`}
                    >
                      🔔 Alerts & Filtering
                    </button>
                  </div>
                </div>
                
                {/* Tab Content */}
                <div className="bg-transparent p-6">
                  {activeTab === 'wallet' && (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      <WalletConnect />
                      <BuyPlan />
                    </div>
                  )}
                  
                  {activeTab === 'alerts' && (
                    <div className="space-y-6">
                      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <TelegramButton />
                        <FilteredPolling />
                      </div>
                      <DebugPanel />
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </QueryClientProvider>
    </WagmiProvider>
  )
}

export default App