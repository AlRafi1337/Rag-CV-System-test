import { useState } from 'react'


export default function SearchBar({ onSearch }: { onSearch: (q: string) => void }) {
const [q, setQ] = useState('')
return (
<div>

<input className="input" placeholder="Search by skills, roles, companies, education…" value={q} onChange={e => setQ(e.target.value)} onKeyDown={e => { if (e.key === 'Enter') onSearch(q) }} />
<div style={{height: 8}} />
<button className="btn" onClick={() => onSearch(q)}>Search</button>
</div>
)
}