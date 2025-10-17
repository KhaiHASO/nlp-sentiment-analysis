import React, { useEffect, useMemo, useRef, useState } from 'react'
import { ChartCard } from './ChartCard'
import {
  ResponsiveContainer,
  ComposedChart,
  Bar,
  Line,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

type SentimentResponse = {
  model_type: string
  model_name: string
  label: string
  score: number
  all_scores?: { label: string; score: number }[]
}

type FillMaskCandidate = { token_str: string; score: number; sequence?: string }
type FillMaskResponse = { model_type: string; model_name: string; top_k: number; candidates: FillMaskCandidate[] }

export const App: React.FC = () => {
  // Theme state with persistence
  const [theme, setTheme] = useState<string>('petal')
  const [modelType, setModelType] = useState<'distilbert' | 'visobert' | 'multilingual'>('visobert')
  const [activeTab, setActiveTab] = useState<'sentiment' | 'fill' | 'scrape'>('sentiment')
  const [text, setText] = useState('Sản phẩm rất tốt và chất lượng.')
  const [maskText, setMaskText] = useState('shop làm ăn như cái <mask>')
  const [maskToken, setMaskToken] = useState('<mask>')
  const maskTextareaRef = useRef<HTMLTextAreaElement | null>(null)
  const [topK, setTopK] = useState(10)

  const [sentiment, setSentiment] = useState<SentimentResponse | null>(null)
  const [mask, setMask] = useState<FillMaskResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [scrapeUrl, setScrapeUrl] = useState('')
  const [scrapeLoading, setScrapeLoading] = useState(false)
  const [scrapeItems, setScrapeItems] = useState<{text:string; label:string; score:number}[] | null>(null)
  const [scrapeSummary, setScrapeSummary] = useState<Record<string, number> | null>(null)
  const [metric, setMetric] = useState<'acc' | 'f1' | 'latency'>('acc')
  const [scrapeLimit, setScrapeLimit] = useState<number>(30)
  const [clientScrapeOnly] = useState<boolean>(true)
  
  useEffect(() => {
    const root = document.getElementById('root')
    if (root) root.setAttribute('data-theme', 'petal')
  }, [])
  
  // Demo chart data (you can swap with real metrics later)
  const chartData = [
    { model: 'ViSoBERT', acc: 91, f1: 90, latency: 42 },
    { model: 'PhoBERT', acc: 90, f1: 89, latency: 55 },
    { model: 'XLM-R', acc: 88, f1: 87, latency: 48 },
    { model: 'mBERT', acc: 86, f1: 85, latency: 60 },
  ]

  const chartColors = {
    acc: '#D2B4DE', // lavender
    f1: '#AFFEEB',  // mint
    latency: '#FFF5B7', // creamy yellow
    area: '#FFB3B3', // peach
  }

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (!active || !payload || !payload.length) return null
    const p = Object.fromEntries(payload.map((d: any) => [d.dataKey, d.value]))
    return (
      <div className="bg-base-100 shadow rounded-xl p-3 text-sm">
        <div className="font-semibold mb-1">{label}</div>
        <div className="flex items-center gap-2"><span className="badge" style={{backgroundColor: chartColors.acc, borderColor: chartColors.acc}}></span> Accuracy: {p.acc}%</div>
        <div className="flex items-center gap-2"><span className="badge" style={{backgroundColor: chartColors.f1, borderColor: chartColors.f1}}></span> F1-score: {p.f1}%</div>
        <div className="flex items-center gap-2"><span className="badge" style={{backgroundColor: chartColors.latency, borderColor: chartColors.latency}}></span> Latency: {p.latency} ms</div>
      </div>
    )
  }

  const canMask = useMemo(() => maskText.includes('<mask>'), [maskText])

  const callSentiment = async () => {
    setLoading(true); setError(null); setSentiment(null)
    try {
      const res = await fetch(`${API_BASE}/sentiment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model_type: modelType, text }),
      })
      if (!res.ok) throw new Error(await res.text())
      const data: SentimentResponse = await res.json()
      setSentiment(data)
      setActiveTab('sentiment')
    } catch (e: any) {
      setError(e.message || 'Request failed')
    } finally {
      setLoading(false)
    }
  }

  const callFillMask = async () => {
    setLoading(true); setError(null); setMask(null)
    try {
      const res = await fetch(`${API_BASE}/fill-mask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: maskText, top_k: topK }),
      })
      if (!res.ok) throw new Error(await res.text())
      const data: FillMaskResponse = await res.json()
      setMask(data)
      setActiveTab('fill')
    } catch (e: any) {
      setError(e.message || 'Request failed')
    } finally {
      setLoading(false)
    }
  }

  const callScrapeAnalyze = async () => {
    if (!scrapeUrl) return
    setScrapeLoading(true); setError(null); setScrapeItems(null)
    try {
      const uRaw = scrapeUrl.trim()
      if (clientScrapeOnly) {
        // Client-only scraping using a read-only proxy (avoids CORS)
        const normalized = uRaw.startsWith('http') ? uRaw : `https://${uRaw}`
        const proxyUrl = `https://r.jina.ai/${normalized}`
        console.log('[scrape] fetching via proxy:', proxyUrl)
        const resp = await fetch(proxyUrl)
        if (!resp.ok) throw new Error(`Proxy HTTP ${resp.status}`)
        const html = await resp.text()
        // Detect common login walls (e.g., Facebook)
        if (/You must log in to continue|Log Into Facebook|login to continue/i.test(html)) {
          throw new Error('Trang yêu cầu đăng nhập, không thể đọc nội dung công khai.')
        }
        const parser = new DOMParser()
        const doc = parser.parseFromString(html, 'text/html')
        const selectors = ['.comment', '.comments', '.cmt', '.reply', '[data-test="comment"]', 'article', 'p']
        const texts: string[] = []
        for (const sel of selectors) {
          const els = Array.from(doc.querySelectorAll(sel)) as HTMLElement[]
          for (const el of els) {
            const txt = (el.innerText || '').trim()
            if (txt && txt.split(/\s+/).length > 3) {
              texts.push(txt)
              if (texts.length >= Math.max(1, Math.min(200, scrapeLimit))) break
            }
          }
          if (texts.length >= Math.max(1, Math.min(200, scrapeLimit))) break
        }
        console.log('[scrape] extracted texts:', texts.length)
        const items = texts.map((t) => ({ text: t, label: 'N/A', score: 0 }))
        setScrapeItems(items)
        setScrapeSummary(null)
      } else {
        // Backend route (disabled for now)
        const params = new URLSearchParams({ url: uRaw, model_type: modelType })
        if (scrapeLimit) params.set('limit', String(Math.max(1, Math.min(200, scrapeLimit))))
        const res = await fetch(`${API_BASE}/scrape-and-analyze?${params.toString()}`)
        if (!res.ok) throw new Error(await res.text())
        const data = await res.json()
        setScrapeItems((data.items || []).map((it: any) => ({ text: it.text, label: it.label, score: it.score })))
        setScrapeSummary(data.summary || null)
      }
      setActiveTab('scrape')
    } catch (e: any) {
      setError(e.message || 'Scrape failed')
    } finally {
      setScrapeLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-base-200 hero-gradient" style={{ fontFamily: 'Inter, system-ui, sans-serif' }}>
      {/* Header */}
      <div className="navbar glass sticky top-0 z-20">
        <div className="flex-1">
          <span className="btn btn-ghost normal-case text-xl">NLP Dashboard</span>
        </div>
        <div className="flex-none items-center gap-2 pr-2">
          <span className="badge badge-outline">API: {API_BASE}</span>
          <div className={`badge ${loading ? 'badge-warning' : 'badge-success'}`}>
            {loading ? 'Running' : 'Ready'}
          </div>
          <span className="badge">Petal</span>
        </div>
      </div>

      {/* Body */}
      <div className="container mx-auto px-4 py-8 grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Left: Controls & Input (with tabs) */}
        <div className="space-y-4">
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Bảng điều khiển</h2>
              <select
                className="select select-sm select-bordered"
                value={modelType}
                onChange={(e) => setModelType(e.target.value as any)}
                title="Model"
              >
                <option value="distilbert">DistilBERT</option>
                <option value="visobert">ViSoBERT</option>
                <option value="multilingual">Multilingual (5-class)</option>
              </select>
            </div>

            <div role="tablist" className="tabs tabs-boxed mb-4">
              <a role="tab" className={`tab ${activeTab==='sentiment' ? 'tab-active' : ''}`} onClick={()=>setActiveTab('sentiment')}>Văn bản</a>
              <a role="tab" className={`tab ${activeTab==='fill' ? 'tab-active' : ''}`} onClick={()=>setActiveTab('fill')}>Fill-Mask</a>
              <a role="tab" className={`tab ${activeTab==='scrape' ? 'tab-active' : ''}`} onClick={()=>setActiveTab('scrape')}>URL</a>
            </div>

            {activeTab === 'sentiment' && (
              <div>
                <textarea
                  className="textarea textarea-bordered w-full"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  rows={6}
                  placeholder="Ví dụ: Tôi rất thích sản phẩm này!"
                />
                <div className="mt-4 flex items-center gap-3">
                  <button className="btn btn-gradient" onClick={callSentiment} disabled={loading}>
                    {loading ? <span className="loading loading-spinner loading-sm mr-2" /> : null}
                    Phân tích
                  </button>
                </div>
              </div>
            )}

            {activeTab === 'fill' && (
              <div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  <div className="md:col-span-2">
                    <textarea
                      className="textarea textarea-bordered w-full"
                      value={maskText}
                      onChange={(e) => setMaskText(e.target.value)}
                      rows={5}
                      placeholder={`Câu có ${maskToken}`}
                      ref={maskTextareaRef}
                    />
                  </div>
                  <div className="md:col-span-1">
                    <label className="label">Mask token</label>
                    <input
                      className="input input-bordered w-full"
                      value={maskToken}
                      onChange={(e) => setMaskToken(e.target.value)}
                      placeholder="<mask>"
                    />
                    <button
                      className="btn btn-outline btn-sm mt-2"
                      onClick={() => {
                        const token = maskToken || '<mask>'
                        const el = maskTextareaRef.current
                        if (!el) {
                          setMaskText((prev) => (prev ? `${prev} ${token}` : token))
                          return
                        }
                        const start = el.selectionStart ?? maskText.length
                        const end = el.selectionEnd ?? start
                        const before = maskText.slice(0, start)
                        const after = maskText.slice(end)
                        const next = `${before}${token}${after}`
                        setMaskText(next)
                        setTimeout(() => {
                          if (maskTextareaRef.current) {
                            const pos = start + token.length
                            maskTextareaRef.current.focus()
                            maskTextareaRef.current.selectionStart = pos
                            maskTextareaRef.current.selectionEnd = pos
                          }
                        }, 0)
                      }}
                    >
                      Chèn mask
                    </button>
                  </div>
                </div>
                <div className="mt-3 flex items-center gap-3">
                  <label className="label gap-2">
                    <span className="label-text">top_k</span>
                    <input
                      className="input input-bordered w-24"
                      type="number"
                      value={topK}
                      onChange={(e) => setTopK(parseInt(e.target.value || '1'))}
                    />
                  </label>
                  <button className="btn btn-primary" onClick={callFillMask} disabled={loading || !canMask}>Suggest Tokens</button>
                </div>
              </div>
            )}

            {activeTab === 'scrape' && (
              <div>
                <input
                  className="input input-bordered w-full"
                  placeholder="Dán URL bài viết (public)"
                  value={scrapeUrl}
                  onChange={(e)=>setScrapeUrl(e.target.value)}
                />
                <div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-3">
                  <label className="form-control w-full md:col-span-1">
                    <div className="label">
                      <span className="label-text">Giới hạn (1-200)</span>
                    </div>
                    <input
                      className="input input-bordered w-full"
                      type="number"
                      min={1}
                      max={200}
                      value={scrapeLimit}
                      onChange={(e)=>setScrapeLimit(parseInt(e.target.value || '30'))}
                    />
                  </label>
                </div>
                <div className="text-xs opacity-70 mt-2">Chỉ hỗ trợ nội dung public. Tôn trọng ToS/robots.txt.</div>
                <button className="btn btn-primary mt-3" onClick={callScrapeAnalyze} disabled={scrapeLoading || !scrapeUrl}>
                  {scrapeLoading && <span className="loading loading-spinner loading-sm mr-2"/>}
                  Tải & Phân tích
                </button>
              </div>
            )}
          </div>

          {/* Tips */}
          <div className="card">
            <div className="text-sm opacity-70">Gợi ý</div>
            <ul className="mt-2 list-disc pl-5 text-sm">
              <li>Multilingual: Very Neg / Neg / Neutral / Pos / Very Pos</li>
              <li>Fill-mask: đảm bảo câu có {maskToken}</li>
            </ul>
          </div>
        </div>

        {/* Center: Main Result */}
        <div className="space-y-6">
          <div className="card flex items-center justify-center text-center py-10 min-h-[300px]">
            <h2 className="text-lg font-semibold mb-3">Khu vực hiển thị kết quả</h2>
            {activeTab === 'sentiment' && (
              sentiment ? (
                <div>
                  <div className={`text-4xl font-extrabold ${sentiment.label.includes('NEG') ? 'text-error' : 'text-success'} mb-1`}>
                    {sentiment.label}
                  </div>
                  <div className="text-2xl font-bold">{(sentiment.score * 100).toFixed(2)}%</div>
                  {sentiment.all_scores && (
                    <div className="mt-4 grid grid-cols-2 gap-2 text-sm opacity-80">
                      {sentiment.all_scores.map((s) => (
                        <div key={s.label} className="flex items-center justify-between">
                          <span>{s.label}</span>
                          <span>{(s.score * 100).toFixed(2)}%</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ) : (
                <div className="opacity-60">Kết quả phân tích sẽ xuất hiện ở đây.</div>
              )
            )}

            {activeTab === 'fill' && (
              mask ? (
                <div className="w-full">
                  <h3 className="text-md font-semibold mb-2">Gợi ý</h3>
                  <div className="overflow-x-auto">
                    <table className="table">
                      <thead>
                        <tr>
                          <th>#</th>
                          <th>Token</th>
                          <th>Score</th>
                          <th>Sequence</th>
                        </tr>
                      </thead>
                      <tbody>
                        {mask.candidates.map((c, idx) => (
                          <tr key={idx}>
                            <td>{idx + 1}</td>
                            <td className="font-medium">{c.token_str}</td>
                            <td>{(c.score * 100).toFixed(2)}%</td>
                            <td className="truncate max-w-xs" title={c.sequence}>{c.sequence}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ) : (
                <div className="opacity-60">Kết quả Fill-Mask sẽ xuất hiện ở đây.</div>
              )
            )}

            {activeTab === 'scrape' && (
              scrapeLoading ? (
                <div className="opacity-70">Đang tải nội dung trang…</div>
              ) : scrapeSummary || scrapeItems ? (
                <div className="w-full">
                  {scrapeSummary && (
                    <div className="mb-4">
                      <div className="text-sm opacity-70 mb-2">Tổng quan</div>
                      <div className="flex flex-wrap gap-2">
                        {Object.entries(scrapeSummary).map(([k,v]) => (
                          <div key={k} className="badge badge-outline">
                            {k}: {v}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  {scrapeItems && (
                    <div className="max-h-72 overflow-auto">
                      <table className="table">
                        <thead>
                          <tr>
                            <th>#</th>
                            <th>Label</th>
                            <th>Score</th>
                            <th>Text</th>
                          </tr>
                        </thead>
                        <tbody>
                          {scrapeItems.map((it, i)=> (
                            <tr key={i}>
                              <td>{i+1}</td>
                              <td className={it.label.includes('NEG') ? 'text-error' : 'text-success'}>{it.label}</td>
                              <td>{(it.score*100).toFixed(2)}%</td>
                              <td className="max-w-lg truncate" title={it.text}>{it.text}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                      <div className="text-xs opacity-70 mt-2">Tổng số: {scrapeItems.length}</div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="opacity-60">Không tìm thấy nội dung bình luận phù hợp từ trang này.</div>
              )
            )}
          </div>
        </div>

        {/* Right: Supplementary (Chart, Status) */}
        <div className="space-y-6">
          <div className="card">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-md font-semibold">So sánh hiệu năng</h3>
              <div className="join">
                <button className={`btn btn-sm join-item ${metric==='acc' ? 'btn-primary' : ''}`} onClick={()=>setMetric('acc')}>Accuracy</button>
                <button className={`btn btn-sm join-item ${metric==='f1' ? 'btn-primary' : ''}`} onClick={()=>setMetric('f1')}>F1-score</button>
                <button className={`btn btn-sm join-item ${metric==='latency' ? 'btn-primary' : ''}`} onClick={()=>setMetric('latency')}>Latency</button>
              </div>
            </div>
            {/* Keep existing ChartCard; selector shown for UX parity */}
            <ChartCard data={chartData} />
          </div>

          <div className="card">
            <h3 className="text-md font-semibold mb-2">Trạng thái</h3>
            <div className="flex items-center gap-2">
              <span className={`badge ${loading ? 'badge-warning' : 'badge-success'}`}>
                {loading ? 'Đang chạy' : 'Sẵn sàng'}
              </span>
              {error && <span className="badge badge-error">Lỗi</span>}
            </div>
            {error && (
              <div className="alert alert-error mt-3">
                <span>{error}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}


