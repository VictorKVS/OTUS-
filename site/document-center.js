const q=s=>document.querySelector(s);
fetch('./data/site-document-pack.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.json()}).then(d=>{
 const cats={};
 d.required_documents.forEach(x=>(cats[x.category]??=[]).push(x));
 q('#stats').innerHTML='<span class="kpi">'+d.required_documents.length+' controlled documents</span><span class="kpi">'+Object.keys(cats).length+' categories</span><span class="kpi">'+d.gates.length+' gates</span><span class="kpi">'+d.status+'</span>';
 q('#categories').innerHTML=Object.entries(cats).map(([cat,docs])=>'<section class="cat"><p class="eyebrow">'+cat+'</p><h2>'+cat.toUpperCase()+'</h2><div class="docs-grid">'+docs.map(x=>'<article class="doc"><div class="meta"><span class="pill">'+x.id+'</span><span class="pill gate">'+x.gate+'</span></div><h3>'+x.path.split('/').pop().replace('.md','').replaceAll('_',' ')+'</h3><p>'+x.purpose+'</p><p><b>Owner:</b> '+x.owner+'<br><b>Approver:</b> '+x.approver+'<br><b>Status:</b> '+x.status+'</p><a href="../'+x.path+'">Открыть документ →</a></article>').join('')+'</div></section>').join('');
 q('#packStatus').textContent=d.site_id+' · '+d.status;
}).catch(e=>{q('#categories').innerHTML='<pre>DOCUMENT PACK ERROR: '+e.message+'</pre>';q('#packStatus').textContent='ERROR';});