import { useMemo, useState } from 'react'
import { Activity, BarChart3, Database, FileUp, FlaskConical, LayoutDashboard, RefreshCw, ShieldCheck, Sparkles, UploadCloud } from 'lucide-react'
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

const API = 'http://127.0.0.1:5000'

export default function App() {
  const [file, setFile] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [connected, setConnected] = useState('not checked')

  const chartData = useMemo(() => {
    if (!analysis?.numeric_summary) return []
    return Object.entries(analysis.numeric_summary).slice(0, 6).map(([name, values]) => ({
      name: name.length > 14 ? name.slice(0, 12) + '…' : name,
      mean: Number(values.mean ?? 0)
    }))
  }, [analysis])

  async function checkBackend() {
    try {
      const res = await fetch(`${API}/api/health`)
      if (!res.ok) throw new Error('Backend returned an error')
      setConnected('connected')
      setError('')
    } catch {
      setConnected('offline')
      setError('Cannot reach Flask backend. Start it in a separate terminal using: cd backend, then python app.py')
    }
  }

  async function uploadFile() {
    if (!file) {
      setError('Choose a CSV file first.')
      return
    }
    setLoading(true)
    setError('')
    const body = new FormData()
    body.append('file', file)
    try {
      const res = await fetch(`${API}/api/analyze`, { method: 'POST', body })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Upload failed')
      setAnalysis(data)
      setConnected('connected')
    } catch (e) {
      setError(e.message || 'Something went wrong while uploading.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><div className="brand-mark"><Activity size={22}/></div><div><strong>EconoCausal</strong><span>PRICING INTELLIGENCE</span></div></div>
        <div className="nav-label">WORKSPACE</div>
        <div className="nav-item active"><LayoutDashboard size={18}/> Dashboard</div>
        <div className="nav-item"><Database size={18}/> Data workspace</div>
        <div className="nav-item"><FlaskConical size={18}/> Causal analysis <span className="soon">SOON</span></div>
        <div className="nav-item"><BarChart3 size={18}/> Budget optimizer <span className="soon">SOON</span></div>
        <div className="sidebar-bottom"><ShieldCheck size={17}/><span>Local prototype<br/><small>Your uploaded file is analyzed by your local backend.</small></span></div>
      </aside>

      <main className="main">
        <header className="topbar"><div><p className="eyebrow">ECONOMICS × MACHINE LEARNING</p><h1>Pricing intelligence dashboard</h1><p className="subtitle">Understand your data before estimating the impact of discounts.</p></div><button className="outline-btn" onClick={checkBackend}><RefreshCw size={16}/> Test connection</button></header>

        <section className="welcome"><div><div className="pill"><Sparkles size={14}/> WEEK 1 PROJECT FOUNDATION</div><h2>Make every discount a data-driven decision.</h2><p>Start by uploading a CSV. EconoCausal will inspect the dataset and prepare it for causal analysis.</p></div><div className="welcome-icon"><BarChart3 size={44}/></div></section>

        <section className="metrics">
          <Metric icon={<Database size={19}/>} label="Rows in dataset" value={analysis ? analysis.rows.toLocaleString() : '—'} note="After CSV upload"/>
          <Metric icon={<BarChart3 size={19}/>} label="Columns detected" value={analysis ? analysis.columns.length : '—'} note="Features and outcomes"/>
          <Metric icon={<Activity size={19}/>} label="Numeric fields" value={analysis ? Object.keys(analysis.numeric_summary || {}).length : '—'} note="Ready for exploration"/>
          <Metric icon={<ShieldCheck size={19}/>} label="API status" value={connected === 'connected' ? 'Online' : connected === 'offline' ? 'Offline' : 'Unknown'} note="Flask connection"/>
        </section>

        <section className="content-grid">
          <div className="panel upload-panel"><div className="panel-heading"><div><h3>Dataset workspace</h3><p>Upload your pricing or sales data</p></div><span className="step-tag">STEP 01</span></div>
            <label className="dropzone"><input type="file" accept=".csv,text/csv" onChange={e => { setFile(e.target.files?.[0] || null); setError('') }}/><div className="upload-icon"><UploadCloud size={25}/></div><strong>{file ? file.name : 'Choose a CSV file'}</strong><span>{file ? `${(file.size / 1024).toFixed(1)} KB · ready to analyze` : 'Click here to browse your computer'}</span><small>CSV format · Include column headers</small></label>
            <div className="button-row"><button className="primary-btn" onClick={uploadFile} disabled={loading}>{loading ? 'Analyzing…' : <><FileUp size={17}/> Upload & analyze</>}</button><button className="text-btn" onClick={() => { setFile(null); setAnalysis(null); setError('') }}>Clear</button></div>
            {error && <div className="error-box">{error}</div>}
            {analysis && <div className="success-box">Dataset loaded successfully. Basic profile generated.</div>}
            <div className="tip"><strong>Tip</strong><span>Try <code>sample_data/pricing_data.csv</code> from the downloaded project folder.</span></div>
          </div>

          <div className="panel chart-panel"><div className="panel-heading"><div><h3>Numeric field overview</h3><p>Average values for the first six numeric columns</p></div></div>
            {chartData.length ? <div className="chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={chartData} margin={{top:10,right:8,left:0,bottom:25}}><CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e8eee9"/><XAxis dataKey="name" tick={{fontSize:11, fill:'#64756d'}} angle={-18} textAnchor="end" interval={0}/><YAxis tick={{fontSize:11, fill:'#64756d'}}/><Tooltip/><Bar dataKey="mean" name="Mean" fill="#28745a" radius={[5,5,0,0]}/></BarChart></ResponsiveContainer></div> : <div className="empty-chart"><div className="empty-icon"><BarChart3 size={28}/></div><strong>Your chart will appear here</strong><span>Upload a CSV to view basic numeric summaries.</span></div>}
          </div>
        </section>

        <section className="panel schema-panel"><div className="panel-heading"><div><h3>Dataset profile</h3><p>{analysis ? 'Detected column names and data types' : 'Column details will appear after upload'}</p></div></div>
          {analysis ? <div className="table-wrap"><table><thead><tr><th>Column</th><th>Data type</th><th>Missing values</th></tr></thead><tbody>{analysis.columns.map(c => <tr key={c.name}><td>{c.name}</td><td><span className="type-chip">{c.dtype}</span></td><td>{c.missing}</td></tr>)}</tbody></table></div> : <div className="schema-placeholder"><Database size={18}/> No dataset loaded yet</div>}
        </section>
        <footer>ECONOCAUSAL <span>•</span> Week 1 foundation <span>•</span> Double Machine Learning is a planned next step</footer>
      </main>
    </div>
  )
}

function Metric({ icon, label, value, note }) {
  return <div className="metric-card"><div className="metric-top"><span className="metric-icon">{icon}</span><span className="metric-note">{note}</span></div><div className="metric-value">{value}</div><div className="metric-label">{label}</div></div>
}
