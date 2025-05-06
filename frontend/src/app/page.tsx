'use client'
import { useState } from 'react'

// test4
export default function Page() {
  const [prdId, setPrdId] = useState('')
  const [result, setResult] = useState<{ NAME: string; PRICE: number } | null>(null)
  const [error, setError] = useState('')

  const fetchProduct = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/product/${prdId}`)
      if (!res.ok) throw new Error('データが見つかりません')
      const data = await res.json()
      setResult(data)
      setError('')
    } catch (err) {
      setError((err as Error).message)
      setResult(null)
    }
  }

  return (
    <div className="p-4">
      <input
        type="number"
        placeholder="PRD_IDを入力"
        value={prdId}
        onChange={(e) => setPrdId(e.target.value)}
        className="border p-2 mr-2"
      />
      <button onClick={fetchProduct} className="bg-blue-500 text-white px-4 py-2 rounded">
        取得
      </button>
      {result && (
        <div className="mt-4">
          <p>商品名: {result.NAME}</p>
          <p>価格: ¥{result.PRICE}</p>
        </div>
      )}
      {error && <p className="text-red-500 mt-4">{error}</p>}
    </div>
  )
}
