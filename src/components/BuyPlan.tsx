import { useState } from 'react'
import { useAccount, useWriteContract, useWaitForTransactionReceipt } from 'wagmi'
import { parseEther } from 'viem'
import { abi } from '../lib/contract'
import { ShoppingCart, CheckCircle, AlertCircle } from 'lucide-react'

const CONTRACT_ADDRESS = '0x5FbDB2315678afecb367f032d93F642f64180aa3'

const BuyPlan = () => {
  const { address, isConnected } = useAccount()
  const [isLoading, setIsLoading] = useState(false)
  
  const { writeContract, data: hash, error, isPending } = useWriteContract()
  
  const { isLoading: isConfirming, isSuccess } = useWaitForTransactionReceipt({
    hash,
  })

  const handleBuyPlan = async () => {
    if (!isConnected) {
      alert('Please connect your wallet first')
      return
    }

    try {
      setIsLoading(true)
      await writeContract({
        address: CONTRACT_ADDRESS,
        abi: abi,
        functionName: 'buyMonthlyPlan',
        value: parseEther('0.0001'), // 1 ETH
      })
    } catch (err) {
      console.error('Error buying plan:', err)
    } finally {
      setIsLoading(false)
    }
  }

  if (!isConnected) {
    return (
      <div className="macos-glass rounded-lg">
        <div className="bg-white/5 px-4 py-3 border-b border-white/10 rounded-t-lg">
          <h3 className="text-lg font-semibold text-white">Monthly Plan</h3>
        </div>
        <div className="p-6 text-center">
          <AlertCircle className="w-12 h-12 text-yellow-400 mx-auto mb-4" />
          <p className="text-yellow-400 font-medium">Please connect your wallet to buy a plan</p>
        </div>
      </div>
    )
  }

  return (
    <div className="macos-glass rounded-lg">
      <div className="bg-white/5 px-4 py-3 border-b border-white/10 rounded-t-lg">
        <h3 className="text-lg font-semibold text-white">Monthly Plan</h3>
      </div>
      
      <div className="p-6">
        <div className="text-center space-y-6">
          <div className="flex items-center justify-center space-x-3">
            <ShoppingCart className="w-8 h-8 text-blue-400" />
            <span className="text-3xl font-bold text-white">1 ETH</span>
          </div>
          
          <p className="text-blue-200 text-sm font-medium">
            Monthly subscription plan
          </p>

          <button
            onClick={handleBuyPlan}
            disabled={isPending || isConfirming || isLoading}
            className="w-full px-6 py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 macos-button"
          >
            {isPending || isConfirming || isLoading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent animate-spin" />
                <span>
                  {isPending ? 'Confirming...' : isConfirming ? 'Processing...' : 'Buying Plan...'}
                </span>
              </>
            ) : (
              <>
                <ShoppingCart className="w-5 h-5" />
                <span>Buy Monthly Plan</span>
              </>
            )}
          </button>

          {isSuccess && (
            <div className="flex items-center justify-center space-x-2 text-green-400 bg-green-500/10 border border-green-500/20 px-4 py-2 rounded-lg">
              <CheckCircle className="w-5 h-5" />
              <span className="font-medium">Transaction successful!</span>
            </div>
          )}

          {error && (
            <div className="flex items-center justify-center space-x-2 text-red-400 bg-red-500/10 border border-red-500/20 px-4 py-2 rounded-lg">
              <AlertCircle className="w-5 h-5" />
              <span className="font-medium">Transaction failed: {error.message}</span>
            </div>
          )}

          {hash && (
            <div className="text-center bg-white/5 border border-white/10 p-4 rounded-lg">
              <p className="text-blue-300 text-sm font-medium mb-2">Transaction Hash:</p>
              <p className="text-blue-400 text-xs font-mono break-all">{hash}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default BuyPlan
