const q=s=>document.querySelector(s);
const esc=v=>String(v??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
Promise.all([
 fetch('./data/trace-registry.json',{cache:'no-store'}).then(r=>r.json()),
 fetch('./data/runtime-traces.json',{cache:'no-store'}).then(r=>r.json()).catch(()=>({runs:[]}))
]).then(([registry,runtime])=>{
 const runs=[...(runtime.runs||[])];
 if(!runs.length && registry.design_sample) runs.push({...registry.design_sample,status:'DESIGN_SAMPLE'});
 q('#stats').innerHTML='<span class="kpi">'+(runtime.runs||[]).length+' runtime runs</span><span class="kpi">'+registry.sources.length+' trace sources</span><span class="kpi">'+registry.event_statuses.length+' event states</span>';
 q('#runsList').innerHTML=runs.map(run=>{
   const sample=run.kind==='DESIGN_SAMPLE';
   const events=(run.events||[]).map(e=>'<div class="evt"><b class="'+esc((e.status||'').toLowerCase())+'">'+esc(e.status)+'</b><small>'+esc(e.event)+'</small><small>'+esc(e.duration_ms==null?'':e.duration_ms+' ms')+'</small><small>'+esc(JSON.stringify(e.metadata||{}))+'</small></div>').join('');
   return '<article class="trace '+(sample?'sample':'run')+'"><div class="trace-head"><div><div class="meta">'+esc(run.agent_id)+'</div><h3>'+esc(run.trace_id)+'</h3></div><span class="tag">'+esc(sample?'DESIGN_SAMPLE':run.status||'RUNTIME')+'</span></div><div class="timeline">'+events+'</div></article>';
 }).join('');
}).catch(e=>q('#runsList').innerHTML='<pre>TRACE CENTER ERROR: '+esc(e.message)+'</pre>');