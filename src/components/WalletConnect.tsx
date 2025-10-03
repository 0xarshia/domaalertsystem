// WalletConnect.tsx
import React from 'react'
import { WagmiProvider } from 'wagmi'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { RainbowKitProvider, ConnectButton, darkTheme } from '@rainbow-me/rainbowkit'
import { getDefaultConfig } from '@rainbow-me/rainbowkit'
import { defineChain } from 'viem'
import { http } from 'wagmi'
import '@rainbow-me/rainbowkit/styles.css'

// ✅ Define your local Foundry/Anvil chain
const anvil = defineChain({
  id: 31337,
  name: 'Anvil Local',
  network: 'anvil',
  nativeCurrency: { name: 'Ether', symbol: 'ETH', decimals: 18 },
  rpcUrls: {
    default: { http: ['http://127.0.0.1:8584'] },
    public: { http: ['http://127.0.0.1:8584'] },
  },
})

// ✅ Wagmi config with only your local chain
const wagmiConfig = getDefaultConfig({
  appName: 'My DApp',
  projectId: 'LOCAL_ONLY_MODE', // doesn’t matter since no WalletConnect cloud
  chains: [anvil],
  transports: {
    [anvil.id]: http('http://127.0.0.1:8584'),
  },
})

const queryClient = new QueryClient()

// ✅ Final WalletConnect component
const WalletConnect = () => {
  return (
    <WagmiProvider config={wagmiConfig}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider chains={[anvil]} theme={darkTheme()}>
          <div className="macos-glass rounded-lg">
            <div className="bg-white/5 px-4 py-3 border-b border-white/10 rounded-t-lg">
              <h3 className="text-lg font-semibold text-white">Wallet Connection</h3>
            </div>
            <div className="p-6">
              <div className="flex justify-center items-center">
                <ConnectButton />
              </div>
            </div>
          </div>
        </RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  )
}

export default WalletConnect
