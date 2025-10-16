import React from 'react'
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

type Props = {
  data: { model: string; acc: number; f1: number; latency: number }[]
}

export const ChartCard: React.FC<Props> = ({ data }) => {
  return (
    <div className="card">
      <h3 className="text-md font-semibold mb-2">So sánh hiệu năng các mô hình NLP</h3>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data} margin={{ top: 10, right: 20, left: -10, bottom: 5 }}>
            <defs>
              <linearGradient id="accGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#60a5fa" stopOpacity={0.8} />
                <stop offset="100%" stopColor="#60a5fa" stopOpacity={0.2} />
              </linearGradient>
              <linearGradient id="f1Gradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#34d399" stopOpacity={0.8} />
                <stop offset="100%" stopColor="#34d399" stopOpacity={0.2} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="model" />
            <YAxis yAxisId="left" orientation="left" stroke="#334155" />
            <YAxis yAxisId="right" orientation="right" stroke="#f59e0b" />
            <Tooltip content={({ active, payload, label }) => {
              if (!active || !payload || !payload.length) return null
              const p = Object.fromEntries(payload.map((d: any) => [d.dataKey, d.value]))
              return (
                <div className="bg-base-100 shadow rounded-xl p-3 text-sm">
                  <div className="font-semibold mb-1">{label}</div>
                  <div>Accuracy: {p.acc}%</div>
                  <div>F1-score: {p.f1}%</div>
                  <div>Latency: {p.latency} ms</div>
                </div>
              )
            }} />
            <Legend />
            <Area yAxisId="left" type="monotone" dataKey="acc" name="Accuracy %" fill="url(#accGradient)" stroke="#60a5fa" strokeWidth={2} />
            <Bar yAxisId="left" dataKey="f1" name="F1-score %" fill="url(#f1Gradient)" />
            <Line yAxisId="right" type="monotone" dataKey="latency" name="Latency (ms)" stroke="#f59e0b" strokeWidth={2} dot={{ r: 3 }} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}


