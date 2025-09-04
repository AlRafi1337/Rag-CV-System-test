import { useEffect, useRef } from 'react'


type Node = { id: string; label: string; type: string; score?: number }


export default function GraphView({ data }: { data: { nodes: Node[]; edges: { source: string; target: string; weight: number }[] } }) {
const ref = useRef<HTMLCanvasElement | null>(null)


useEffect(() => {
const canvas = ref.current!
const ctx = canvas.getContext('2d')!
const width = canvas.width = canvas.clientWidth
const height = canvas.height = canvas.clientHeight


// Very small, dependency-free force layout
const nodes = data.nodes.map(n => ({...n, x: Math.random()*width, y: Math.random()*height, vx:0, vy:0 })) as any[]
const edges = data.edges


function step() {
// Hook forces towards connected nodes
for (const e of edges) {
const a = nodes.find(n => n.id === e.source)!; const b = nodes.find(n => n.id === e.target)!
const dx = b.x - a.x; const dy = b.y - a.y; const d = Math.max(20, Math.hypot(dx, dy))
const k = 0.001 * e.weight
const fx = k * dx; const fy = k * dy
a.vx += fx; a.vy += fy; b.vx -= fx; b.vy -= fy
}
for (const n of nodes) {
n.vx *= 0.9; n.vy *= 0.9; n.x += n.vx; n.y += n.vy
n.x = Math.max(10, Math.min(width-10, n.x)); n.y = Math.max(10, Math.min(height-10, n.y))
}
}


function draw() {
ctx.clearRect(0,0,width,height)
ctx.globalAlpha = 0.6
ctx.strokeStyle = '#CBD5E1'
for (const e of edges) {
const a = nodes.find(n => n.id === e.source)!; const b = nodes.find(n => n.id === e.target)!
ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke()
}
ctx.globalAlpha = 1
for (const n of nodes) {
const color = n.type === 'query' ? '#1F2937' : (n.type === 'document' ? '#3B82F6' : '#10B981')
ctx.fillStyle = color
ctx.beginPath(); ctx.arc(n.x, n.y, n.type==='document'?7:n.type==='query'?9:5, 0, Math.PI*2); ctx.fill()
ctx.fillStyle = '#111827'; ctx.font = '12px sans-serif'
ctx.fillText(n.label.slice(0, 40), n.x+8, n.y-8)
}
}


let raf = 0
function tick() { step(); draw(); raf = requestAnimationFrame(tick) }
tick()
return () => cancelAnimationFrame(raf)
}, [data])


return <canvas className="graph" ref={ref}></canvas>
}