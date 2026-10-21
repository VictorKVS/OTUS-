const q=s=>document.querySelector(s);
const arrow='<span class="arrow">→</span>';
fetch('./data/knowledge-registry-v2.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.json()}).then(d=>{
 q('#stats').innerHTML=[
  '<span class="kpi">1 common core</span>',
  '<span class="kpi">'+d.specialist_packs.length+' specialist packs</span>',
  '<span class="kpi">'+d.project_contexts.length+' project contexts</span>',
  '<span class="kpi">'+d.agent_profiles.length+' agent profiles</span>'
 ].join('');
 q('#layersGrid').innerHTML=[
  '<article class="kcard"><div class="layer">K0 · REQUIRED</div><h3>🌐 '+d.common_core.name+'</h3><p>'+d.common_core.modules.map(x=>x.name).join(' · ')+'</p><span class="ok">'+d.common_core.status+'</span></article>',
  '<article class="kcard"><div class="layer">K1 · REQUIRED FOR SPECIALISTS</div><h3>🎓 Specialist Knowledge Pack</h3><p>Профессиональные источники, методы, ontology, cases, benchmarks и связь со Skill Tree.</p></article>',
  '<article class="kcard"><div class="layer">K2 · OPTIONAL</div><h3>🗂 Project / Organization Context</h3><p>Scoped overlay конкретного проекта. Не переписывает K0/K1 и имеет отдельную access policy.</p></article>'
 ].join('');
 q('#packsGrid').innerHTML=d.specialist_packs.map(x=>'<article class="pack"><div class="layer">'+x.id+' · '+x.status+'</div><h3>'+x.name+'</h3><p><b>Family:</b> '+x.family+'</p><p>'+x.topics.join(' · ')+'</p><div class="tags">'+x.depends_on.map(v=>'<span class="tag">'+v+'</span>').join('')+'</div></article>').join('');
 q('#profilesGrid').innerHTML=d.agent_profiles.map(x=>'<article class="profile"><div class="layer">'+x.agent_id+'</div><h3>'+x.name+'</h3><p><b>K0:</b> '+x.common_core_id+' @ '+x.common_core_version+'</p><p><b>K1:</b> '+x.specialist_pack_ids.join(' + ')+'</p><p><b>K2:</b> '+(x.project_context_id||'—')+'</p><p><b>Conflict:</b> '+x.conflict_policy+'</p></article>').join('');
 const route=['Intent / Domain','K0 Common','K1 Specialist','K2 if allowed','Merge','Deduplicate','Rank','Conflict Check','Evidence Bundle','Agent'];
 q('#routerFlow').innerHTML=route.map((x,i)=>'<div class="node"><b>'+x+'</b><small>'+(['detect task','shared foundation','professional knowledge','project scope','combine evidence','remove duplicates','relevance/authority','never hide conflict','retain provenance','reason over evidence'][i])+'</small></div>'+(i<route.length-1?arrow:'')).join('');
 q('#policies').innerHTML=[
  ['Mutation',d.common_core.mutation_policy],
  ['Retrieval',d.common_core.retrieval_policy],
  ['Citation',d.common_core.citation_policy],
  ['Conflict',d.common_core.conflict_policy]
 ].map(x=>'<div class="route"><code>'+x[0]+'</code><br>'+x[1]+'</div>').join('');
 q('#separateGrid').innerHTML=Object.entries(d.separate_systems).map(([k,v])=>'<article class="kcard"><div class="layer">'+k.toUpperCase()+'</div><h3>'+k+'</h3><p>'+v+'</p></article>').join('');
}).catch(e=>document.body.insertAdjacentHTML('beforeend','<pre>KNOWLEDGE CENTER ERROR: '+e.message+'</pre>'));