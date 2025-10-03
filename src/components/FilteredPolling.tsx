import { useState, useRef, useEffect } from 'react'

const FilteredPolling = () => {
  const [isPolling, setIsPolling] = useState(false)
  const [message, setMessage] = useState('')
  const [lastEventId, setLastEventId] = useState<string | null>(null)
  const intervalRef = useRef<NodeJS.Timeout | null>(null)

  const fetchAndSendApiData = async () => {
    try {
      // Make API call to the Doma API
      const response = await fetch('https://api-testnet.doma.xyz/v1/poll?eventTypes=NAME_TOKEN_LISTED&limit=1', {
        method: 'GET',
        headers: {
          'Api-Key': 'v1.d25826e8ff3c9607022227c25f76cccafba3a13b0514977d02616ce1b98fa23c'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        
        // Extract only the required fields
        if (data.events && data.events.length > 0) {
          const event = data.events[0]
          const extractedData = {
            name: event.name,
            type: event.type,
            price: event.eventData?.payment?.price,
            currencySymbol: event.eventData?.payment?.currencySymbol,
            eventCreatedAt: event.eventData?.eventCreatedAt
          }
          
          // Debug: Log the extracted data
          console.log('🔍 Extracted data:', extractedData)
          console.log('🔍 Full API response:', data)
          
          // Format price to show normal ETH value (remove 18 decimals)
          const formattedPrice = extractedData.price ? 
            (parseFloat(extractedData.price) / 1e18).toFixed(6) : 
            'N/A'
          
          // Create explorer link if txhash is available
          const explorerLink = data.events?.[0]?.txhash || data.events?.[0]?.txHash || data.events?.[0]?.transactionHash
            ? `https://explorer-testnet.doma.xyz/tx/${data.events[0].txhash || data.events[0].txHash || data.events[0].transactionHash}`
            : null
          
          // Build message with all data
          let message = `🌐 Doma API Data:\n\n`
          message += `📝 Name: ${extractedData.name}\n`
          message += `🏷️ Type: ${extractedData.type}\n`
          message += `💰 Price: ${formattedPrice} ${extractedData.currencySymbol}\n`
          message += `📅 Created: ${extractedData.eventCreatedAt}\n`
          message += `🆔 LastId: ${data.lastId}\n`
          
          if (explorerLink) {
            message += `🔗 Transaction: ${explorerLink}\n`
          }
          
          // Send the extracted data to the bot with response data for filtering
          const botResponse = await fetch('http://localhost:5000/api/trigger-telegram', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              message: message,
              responseData: data
            })
          })
          
          if (botResponse.ok) {
            const result = await botResponse.json()
            if (result.filtered) {
              console.log('🚫 Message filtered out due to price range')
            } else {
              console.log('✅ API data sent to Telegram bot users!')
            }
          } else {
            console.log('❌ Failed to send data to bot')
          }
          
          // Acknowledge the last event to get new data next time
          if (data.lastId) {
            try {
              await fetch(`https://api-testnet.doma.xyz/v1/poll/ack/${data.lastId}`, {
                method: 'POST',
                headers: {
                  'Api-Key': 'v1.d25826e8ff3c9607022227c25f76cccafba3a13b0514977d02616ce1b98fa23c'
                }
              })
              setLastEventId(data.lastId)
            } catch (ackError) {
              // Silently handle ack errors - don't show to user
              console.log('Ack call failed:', ackError)
            }
          }
        } else {
          console.log('❌ No events found in API response')
        }
      } else {
        console.log(`❌ API Error: ${response.status} ${response.statusText}`)
      }
    } catch (error) {
      console.log('❌ Error fetching API data:', error)
    }
  }

  const startPolling = async () => {
    if (isPolling) {
      // Stop polling
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
        intervalRef.current = null
      }
      setIsPolling(false)
      setMessage('⏹️ Polling stopped')
      return
    }

    // Start polling
    setMessage('🔄 Starting filtered polling loop...')
    
    // Send first request immediately
    await fetchAndSendApiData()
    
    // Set up interval for every 15 seconds
    intervalRef.current = setInterval(async () => {
      await fetchAndSendApiData()
    }, 15000)
    
    setIsPolling(true)
    setMessage('✅ Filtered polling started! Checking every 15 seconds with price filter')
  }

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [])

  return (
    <div className="macos-glass rounded-lg">
      <div className="bg-white/5 px-4 py-3 border-b border-white/10 rounded-t-lg">
        <h3 className="text-lg font-semibold text-white">Automatic Filtered Polling</h3>
      </div>
      
      <div className="p-6">
        <p className="text-blue-200 mb-6 text-sm font-medium">
          This component automatically polls the Doma API every 15 seconds and sends filtered data to Telegram users based on your configured price range.
        </p>
        
        <button
          onClick={startPolling}
          className={`
            w-full px-6 py-4 font-semibold transition-all duration-200 rounded-lg macos-button
            ${isPolling 
              ? 'bg-red-600 hover:bg-red-700'
              : 'bg-green-600 hover:bg-green-700'
            }
            text-white
          `}
        >
          {isPolling ? (
            '⏹️ Stop Polling'
          ) : (
            '🔄 Start Filtered Polling (15s)'
          )}
        </button>
        
        {message && (
          <div className={`mt-4 p-4 border rounded-lg ${
            message.includes('✅') 
              ? 'bg-green-500/10 border-green-500/20 text-green-300' 
              : 'bg-red-500/10 border-red-500/20 text-red-300'
          }`}>
            <p className="font-medium">{message}</p>
          </div>
        )}
        
        {lastEventId && (
          <div className="mt-4 p-4 bg-white/5 border border-white/10 rounded-lg">
            <p className="text-blue-300 text-sm font-medium">
              📊 Last processed event ID: {lastEventId}
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default FilteredPolling
