const BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';


export async function search(query: string, k = 20) {
const r = await fetch(`${BASE}/search`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query, k }) });
return r.json();
}
export async function searchGraph(query: string, k = 20) {
const r = await fetch(`${BASE}/search/graph`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query, k }) });
return r.json();
}
export async function upload(files: File[]) {
const fd = new FormData();
files.forEach(f => fd.append('files', f));
const r = await fetch(`${BASE}/upload`, { method: 'POST', body: fd });
return r.json();
}
export async function listDocuments() {
const r = await fetch(`${BASE}/documents`);
return r.json();
}