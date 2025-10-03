import { createPublicClient, http, getContract } from 'viem'
import { foundry } from 'viem/chains'

// ABI for the contract - you'll need to replace this with your actual ABI
// This is a placeholder ABI for a contract with buyMonthlyPlan function
const abi = [
  {
    "inputs": [],
    "name": "buyMonthlyPlan",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  }
] as const

export const client = createPublicClient({
  chain: foundry,
  transport: http('http://127.0.0.1:8545'), // local anvil node
})

export const contract = getContract({
  address: '0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9', // your deployed contract address
  abi,
  client,
})

export { abi }
