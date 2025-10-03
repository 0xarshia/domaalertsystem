# Doma Alert - Wallet Integration

A simple React application with wallet connection and smart contract interaction using Wagmi and Viem.

## Features

- 🔗 Wallet connection (MetaMask, WalletConnect, Injected)
- 💰 Buy monthly plan function (1 ETH)
- 🎨 Beautiful UI with Tailwind CSS
- ⚡ Built with Vite and TypeScript

## Setup

1. Make sure your local Anvil node is running on `http://127.0.0.1:8545`
2. Deploy your contract and update the address in `src/lib/contract.ts`
3. Update the ABI in `src/lib/contract.ts` with your actual contract ABI
4. Install dependencies:
   ```bash
   npm install
   ```
5. Start the development server:
   ```bash
   npm run dev
   ```

## Contract Configuration

Update the contract address and ABI in `src/lib/contract.ts`:

```typescript
export const contract = getContract({
  address: '0x5FbDB2315678afecb367f032d93F642f64180aa3', // Your contract address
  abi, // Your contract ABI
  client,
})
```

## WalletConnect Setup

To use WalletConnect, update the project ID in `src/lib/wagmi.ts`:

```typescript
walletConnect({
  projectId: 'your-project-id', // Replace with your WalletConnect project ID
}),
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Tech Stack

- React 18
- TypeScript
- Vite
- Tailwind CSS
- Wagmi v2
- Viem
- React Query
