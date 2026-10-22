fetch('./data/father-visual-system.json',{cache:'no-store'}).then(r=>r.json()).then(d=>{
  const colors=d.tokens.colors;
  document.querySelector('#swatches').innerHTML=Object.entries(colors).map(([k,v])=>
    '<div class="swatch" style="background:'+v+'"><b>'+k.replaceAll('_',' ')+'</b><small>'+v+'</small></div>'
  ).join('');
  document.querySelector('#statusDemo').innerHTML=d.status_model.map(s=>
    '<span class="status-pill tone-'+s.tone+'">'+s.id+'</span>'
  ).join('');
}).catch(e=>document.body.insertAdjacentHTML('beforeend','<pre>'+e.message+'</pre>'));