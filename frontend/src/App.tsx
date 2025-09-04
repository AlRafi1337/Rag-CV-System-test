import { useEffect, useState } from 'react'
import SearchBar from './component/SearchBar'
import ResultsList from './component/ResultsList'
import GraphView from './component/GraphView'
import { search, searchGraph, upload, listDocuments } from './api'


export default function App() {
const [results, setResults] = useState<any[]>([])
const [graph, setGraph] = useState<{nodes:any[]; edges:any[]}>({nodes:[], edges:[]})
const [docs, setDocs] = useState<any[]>([])


useEffect(() => { listDocuments().then(setDocs) }, [])


async function onSearch(q: string) {
const [r, g] = await Promise.all([search(q, 20), searchGraph(q, 20)])
setResults(r.results)
setGraph(g)
}


async function onUpload(files: FileList | null) {
if (!files || files.length === 0) return;
const r = await upload(Array.from(files))
setTimeout(() => listDocuments().then(setDocs), 500)
}


return (
<div className="app">
<div className="sidebar">
<h2>RAG CV Search</h2>
<SearchBar onSearch={onSearch} />
<label htmlFor="file-upload" style={{ display: 'block', marginTop: 10 }}>
	<span className="btn" style={{ marginBottom: 8, display: 'inline-block' }}>Upload CV(s)</span>
	<input id="file-upload" className="file" type="file" multiple style={{ display: 'none' }} onChange={e => onUpload(e.target.files)} />
</label>
<div style={{marginTop:16}}>
<h3>Recent Documents</h3>
{docs.map(d => (
<div key={d.id} className="card">
<div style={{fontWeight:600}}>{d.original_filename}</div>
<div style={{opacity:0.7}}>Chunks: {d.chunk_count}</div>
</div>
))}
</div>
</div>
<div className="main">
<h3>Graph</h3>
<GraphView data={graph} />
<h3>Results</h3>
<ResultsList results={results} />
</div>
</div>
)
}