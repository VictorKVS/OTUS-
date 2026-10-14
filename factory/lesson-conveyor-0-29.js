fetch('./data/lesson-conveyor-0-29.json').then(r=>r.json()).then(d=>{
 const by=s=>document.querySelector(s);
 by('#stats').innerHTML='<span class="kpi">'+d.lessons.length+' phases</span><span class="kpi">'+d.waves.length+' integration waves</span><span class="kpi">target: working M1 factory</span>';
 by('#wavesGrid').innerHTML=d.waves.map(w=>'<article class="wave"><div class="meta">'+w.id+' · '+w.range[0]+'–'+w.range[1]+'</div><h3>'+w.title+'</h3><p>'+w.result+'</p></article>').join('');
 by('#lessonGrid').innerHTML=d.lessons.map(x=>'<article class="lesson"><div class="n">'+String(x.id).padStart(2,'0')+'</div><div class="meta">'+x.domain+' · '+x.capability+'</div><h3>'+x.title+'</h3><span class="status '+x.status+'">'+x.status+'</span><p><b>Factory output:</b> '+x.output+'</p><small>Station: '+x.station+'</small></article>').join('');
}).catch(e=>document.body.insertAdjacentHTML('beforeend','<pre>'+e+'</pre>'));