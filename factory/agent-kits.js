const q=s=>document.querySelector(s);
Promise.all([
 fetch('./data/agent-kit-registry.json',{cache:'no-store'}).then(r=>r.json()),
 fetch('./data/knowledge-registry-v2.json',{cache:'no-store'}).then(r=>r.json())
]).then(([a,k])=>{
 const packNames=Object.fromEntries(k.specialist_packs.map(x=>[x.id,x.name]));
 q('#stats').innerHTML='<span class="kpi">'+a.kits.length+' agent kits</span><span class="kpi">1 shared K0</span><span class="kpi">'+k.specialist_packs.length+' K1 packs</span><span class="kpi">'+k.agent_profiles.length+' knowledge profiles</span>';
 const nodes=[
  ['FATHER Base Kit','identity · lifecycle · evidence'],
  [a.common_knowledge.id,'shared reference · '+a.common_knowledge.version],
  ['K1 Specialist Pack','one or more professional packs'],
  ['Skills + Tools','role capabilities'],
  ['Policies + Memory','scope · permissions · instructions'],
  ['Evaluation + LAB','proof before certification']
 ];
 q('#composition').innerHTML=nodes.map((x,i)=>'<div class="node"><b>'+x[0]+'</b><small>'+x[1]+'</small></div>'+(i<nodes.length-1?'<span class="arrow">→</span>':'')).join('');
 q('#kitGrid').innerHTML=a.kits.map(x=>{
   const profile=k.agent_profiles.find(p=>p.agent_id===x.agent_id);
   const cls=x.status.includes('READY')?'ready':'design';
   const packs=x.specialist_pack_ids.map(id=>'<span class="tag">'+id+'</span>').join('');
   return '<article class="kit"><div class="kit-top"><span class="pill">'+x.agent_id+'</span><span class="pill '+cls+'">'+x.status+'</span></div><h3>'+x.name+'</h3><p><b>Family:</b> '+x.family+'</p><div class="inherit"><b>K0</b><p>'+a.common_knowledge.id+' @ '+a.common_knowledge.version+' · shared_reference</p><b>K1</b><div class="tags">'+packs+'</div></div><p><b>K2:</b> '+(profile?.project_context_id||'—')+'<br><b>Knowledge policy:</b> '+(profile?.retrieval_policy||'missing profile')+'</p></article>';
 }).join('');
}).catch(e=>document.body.insertAdjacentHTML('beforeend','<pre>AGENT KIT CENTER ERROR: '+e.message+'</pre>'));