const $=s=>document.querySelector(s);
const esc=v=>String(v??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

function roleClass(v){
  const x=String(v||'').toLowerCase();
  if(['owner','approver','specialist'].includes(x)) return 'role-strong';
  if(['review','support','consumer_producer','validation','test','evidence','acceptance'].includes(x)) return 'role-medium';
  if(['none'].includes(x)) return 'role-none';
  return 'role-light';
}
function renderBranch(system,id){
  const b=system.domain_branches.find(x=>x.id===id)||system.domain_branches[0];
  document.querySelectorAll('.domain-tab').forEach(x=>x.classList.toggle('active',x.dataset.id===b.id));
  const participation=Object.entries(b.workshop_participation||{}).map(([w,r])=>'<span class="'+roleClass(r)+'">'+esc(w)+' · '+esc(r)+'</span>').join('');
  $('#domainPanel').innerHTML=
    '<div class="domain-head"><div><p class="eyebrow">'+esc(b.agent_family)+' · '+esc(b.overlay)+'</p><h3>'+esc(b.tab)+'</h3><p>'+esc(b.role)+'</p></div><b class="domain-status">'+esc(b.status)+'</b></div>'+
    '<div class="domain-details">'+
      '<article><b>INPUT</b>'+(b.input||[]).map(x=>'<span>'+esc(x)+'</span>').join('')+'</article>'+
      '<article><b>OUTPUT</b>'+(b.output||[]).map(x=>'<span>'+esc(x)+'</span>').join('')+'</article>'+
      '<article><b>WORKSHOPS</b><div class="role-cloud">'+participation+'</div></article>'+
    '</div>'+
    '<div class="domain-contract">'+esc(b.common_contract)+'</div>';
}
fetch('./data/father-unified-system.json',{cache:'no-store'}).then(r=>r.json()).then(system=>{
  $('#branchCount').textContent=system.domain_branches.length;
  $('#workshopCount').textContent=system.flow.workshops.length;
  $('#k1Count').textContent=system.current_known_k1.length;
  $('#kitCount').textContent=system.current_agent_kits.length;

  const base=[
    ['Analytical Core',system.common_base.analytical_core],
    ['Knowledge',system.common_base.common_knowledge],
    ['Dossier',system.common_base.dossier],
    ['LAB',system.common_base.lab],
    ['Operations',system.common_base.operations],
    ['Regulations',system.common_base.regulations.join(' · ')]
  ];
  $('#baseGrid').innerHTML=base.map(([a,b])=>'<article><span>'+esc(a)+'</span><b>'+esc(b)+'</b></article>').join('');

  $('#workshopLane').innerHTML=system.flow.workshops.map((w,i)=>'<article class="workshop"><span>'+esc(w.id)+'</span><b>'+esc(w.name.replaceAll('_',' '))+'</b><small>'+esc(w.purpose)+'</small></article>'+(i<system.flow.workshops.length-1?'<i>→</i>':'')).join('');

  $('#domainTabs').innerHTML=system.domain_branches.map((b,i)=>'<button class="domain-tab '+(i===0?'active':'')+'" data-id="'+esc(b.id)+'">'+esc(b.tab)+'</button>').join('');
  document.querySelectorAll('.domain-tab').forEach(btn=>btn.addEventListener('click',()=>renderBranch(system,btn.dataset.id)));
  renderBranch(system,'analytics');

  const header='<thead><tr><th>Ветка</th>'+system.flow.workshops.map(w=>'<th>'+esc(w.id)+'<small>'+esc(w.name.replaceAll('_',' '))+'</small></th>').join('')+'</tr></thead>';
  const body='<tbody>'+system.domain_branches.map(b=>'<tr><td><b>'+esc(b.tab)+'</b><small>'+esc(b.overlay)+'</small></td>'+system.flow.workshops.map(w=>{const r=(b.workshop_participation||{})[w.id]||'—';return '<td><span class="matrix-role '+roleClass(r)+'">'+esc(r)+'</span></td>';}).join('')+'</tr>').join('')+'</tbody>';
  $('#participationMatrix').innerHTML=header+body;

  const contract=['INPUT','REGULATION','RESPONSIBLE ROLE','PROCESS','TOOLS / MODELS / KNOWLEDGE','ARTIFACTS','TESTS / VALIDATION','EVIDENCE','GATE','OUTPUT','NEXT WORKSHOP'];
  $('#contractFlow').innerHTML=contract.map((x,i)=>'<span>'+esc(x)+'</span>'+(i<contract.length-1?'<i>→</i>':'')).join('');
}).catch(e=>document.body.insertAdjacentHTML('beforeend','<pre>UNIFIED SYSTEM ERROR: '+esc(e.message)+'</pre>'));