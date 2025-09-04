export default function ResultsList({ results }: { results: any[] }) {
return (
<div>
{results.map((r) => (
<div className="card" key={r.chunk_id}>
<div style={{fontWeight:600}}>{r.original_filename}</div>
<div style={{opacity:0.7}}>Score: {r.score?.toFixed(3)}</div>
<div style={{marginTop:6}}>{r.content}</div>
</div>
))}
</div>
)
}