import { createConfig, http } from 'wagmi'
import { foundry } from 'viem/chains'
import { injected } from 'wagmi/connectors'

export const config = createConfig({
  chains: [foundry],
  connectors: [
    injected(),
  ],
  transports: {
    [foundry.id]: http('http://127.0.0.1:8545'),
  },
})

declare module 'wagmi' {
  interface Register {
    config: typeof config
  }
}
