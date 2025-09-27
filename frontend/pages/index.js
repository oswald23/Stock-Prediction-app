
import { useState } from 'react'
import dynamic from 'next/dynamic'

const Line = dynamic(
  () => import('react-chartjs-2').then(m => m.Line),
  { ssr: false }
)

export default function HomePage() {
  const [ticker, setTicker] = useState('')
  const [forecast, setForecast] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchForecast = async () => {
    const base = process.env.NEXT_PUBLIC_BACKEND_URL
    if (!base) {
      setError('Missing NEXT_PUBLIC_BACKEND_URL')
      return
    }
    setLoading(true); setError('')
    try {
      const res = await fetch(`${base}/forecast?ticker=${encodeURIComponent(ticker)}`)
      if (!res.ok) throw new Error('Failed to fetch')
      const data = await res.json()
      setForecast(data.forecast || [])
    } catch (e) {
      setError('Could not get forecast. Check backend URL and try again.')
    } finally {
      setLoading(false)
    }
  }

  const onSubmit = (e) => {
    e.preventDefault()
    if (!ticker.trim()) { setError('Enter a ticker'); return }
    fetchForecast()
  }

  const labels = forecast.map(p => p.date)
  const values = forecast.map(p => p.price)

  const chartData = {
    labels,
    datasets: [{
      label: 'Forecasted Price',
      data: values,
      fill: false,
      tension: 0.2,
      borderColor: 'rgba(59,130,246,1)',
      backgroundColor: 'rgba(59,130,246,0.2)'
    }]
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-start p-6 bg-gray-50">
      <h1 className="text-3xl font-bold mb-6">Stock Price Forecast</h1>

      <form onSubmit={onSubmit} className="w-full max-w-xl flex gap-3 mb-6">
        <input
          className="flex-1 px-3 py-2 border rounded outline-none"
          placeholder="Enter stock ticker (e.g., AAPL)"
          value={ticker}
          onChange={(e)=>setTicker(e.target.value.toUpperCase())}
        />
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-60"
          disabled={loading}
        >
          {loading ? 'Loading…' : 'Get Forecast'}
        </button>
      </form>

      {error && <p className="text-red-600 mb-4">{error}</p>}

      {forecast.length > 0 && (
        <div className="w-full max-w-3xl bg-white p-4 rounded shadow">
          <Line data={chartData} />
        </div>
      )}
    </div>
  )
}
