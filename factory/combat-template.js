const q=s=>document.querySelector(s);
fetch('./data/combat-template-c00-c99.json',{cache:'no-store'}).then(r=>r.json()).then(d=>{
 q('#contract').innerHTML=d.stage_contract.map(x=>'<span>'+x.replaceAll('_',' ')+'</span>').join('');
 const card=x=>'<article class="stage '+x.origin+'"><b>'+x.code+'</b><h3>'+x.name.replaceAll('_',' ')+'</h3><small>'+x.gate+' → '+(x.next||'CLOSE')+'</small></article>';
 q('#legacyGrid').innerHTML=d.stages.filter(x=>x.origin==='legacy').map(card).join('');
 const ranges=[[21,30,'Resilience / Scale / Evolution'],[31,39,'Command Documents'],[40,49,'Knowledge / Training'],[50,59,'Agents / Runtime'],[60,69,'LAB / Metrology'],[70,79,'Development / Verification'],[80,89,'DevOps / Operations'],[90,99,'Certification / Feedback / Closeout']];
 q('#bands').innerHTML=ranges.map(([a,b,n])=>'<div class="band"><div class="meta">'+String(a).padStart(2,'0')+'–'+b+'</div><h3>'+n+'</h3><div class="stage-grid">'+d.stages.slice(a,b+1).map(card).join('')+'</div></div>').join('');
}).catch(e=>document.body.insertAdjacentHTML('beforeend','<pre>'+e.message+'</pre>'));