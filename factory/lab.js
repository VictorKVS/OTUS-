const q=s=>document.querySelector(s);
const state={data:null,gates:null,filter:'all'};
function badge(text){return '<span class="tag">'+text+'</span>';}
async function load(){
 const [r,g]=await Promise.all([
  fetch('./data/lab-registry.json',{cache:'no-store'}),
  fetch('./data/verification-gates.json',{cache:'no-store'})
 ]);
 if(!r.ok) throw new Error('LAB registry HTTP '+r.status);
 if(!g.ok) throw new Error('Verification gates HTTP '+g.status);
 state.data=await r.json();
 state.gates=await g.json();
 render();
 renderVerification();
}
function render(){
 const d=state.data;
 q('#labStats').innerHTML=[
  [d.projects.length,'project labs'],
  [d.labAreas.length,'test areas'],
  [d.experiments.length,'registered experiments'],
  [d.datasets.reduce((a,x)=>a+x.cases,0),'dataset cases'],
  [d.champions.length,'champion profiles']
 ].map(x=>'<span class="kpi"><b>'+x[0]+'</b> '+x[1]+'</span>').join('');
 q('#labAreas').innerHTML=d.labAreas.map(x=>'<article class="lab-card"><div class="icon">'+x.icon+'</div><div class="meta">'+x.id+'</div><h3>'+x.title+'</h3><p>'+x.purpose+'</p><div class="tags">'+x.targets.map(badge).join('')+'</div></article>').join('');
 q('#projectLabs').innerHTML=d.projects.map(x=>'<article class="project-lab"><div class="project-head"><div class="meta">'+x.id+'</div><span class="project-status">'+x.status+'</span></div><h3>'+x.icon+' '+x.title+'</h3><p>'+x.purpose+'</p><ul>'+x.labs.map(v=>'<li>'+v+'</li>').join('')+'</ul></article>').join('');
 q('#alinaLabs').innerHTML=d.alinaLabs.map(x=>'<article class="lab-card"><div class="icon">'+x.icon+'</div><h3>'+x.title+'</h3><p>'+x.purpose+'</p></article>').join('');
 q('#alinaFlow').innerHTML=d.alinaFlow.map(x=>'<div class="vstep">'+x+'</div>').join('');
 q('#qualityGates').innerHTML=d.qualityGates.map(x=>'<article class="quality-card"><div class="meta">'+x.id+'</div><h3>'+x.title+'</h3><p>'+x.rule+'</p></article>').join('');
 q('#qualityLane').innerHTML=d.qualityLane.map((x,i)=>'<div class="step"><b>'+x+'</b></div>'+(i<d.qualityLane.length-1?'<span class="arrow">→</span>':'')).join('');
 q('#datasets').innerHTML=d.datasets.map(x=>'<article class="dataset-card"><div class="meta">'+x.id+'</div><h3>'+x.title+'</h3><strong>'+x.cases+'</strong><p>'+x.purpose+'</p></article>').join('');
 q('#championProfiles').innerHTML=d.champions.map(x=>'<article class="champion-card"><div class="winner">'+x.profile+'</div><h3>'+x.winner+'</h3><p>'+x.reason+'</p></article>').join('');
 renderExperiments();
}
function renderExperiments(){
 const xs=state.data.experiments.filter(x=>state.filter==='all'||x.project===state.filter);
 q('#experimentGrid').innerHTML=xs.map(x=>'<article class="experiment"><div class="exp-top"><span class="exp-id">'+x.id+' · '+x.project+'</span><span class="exp-state '+x.state+'">'+x.state.toUpperCase()+'</span></div><h3>'+x.title+'</h3><p><b>Hypothesis:</b> '+x.hypothesis+'</p><div class="variant-row"><div class="variant"><b>A · baseline</b>'+x.a+'</div><div class="variant"><b>B · challenger</b>'+x.b+'</div></div><div class="score-row">'+x.metrics.map(badge).join('')+'</div></article>').join('')||'<div class="card">Нет экспериментов по фильтру.</div>';
}
q('#projectFilter').addEventListener('change',e=>{state.filter=e.target.value;renderExperiments();});
load().catch(e=>document.body.insertAdjacentHTML('beforeend','<pre>LAB DATA ERROR: '+e.message+'</pre>'));

function renderVerification(){
 const g=state.gates;
 q('#verificationGateGrid').innerHTML=g.gates.map(x=>
  '<article class="quality-card"><div class="meta">'+x.id+' · '+x.domain+'</div><h3>'+x.check.replaceAll('_',' ')+'</h3><p>mandatory: <b>'+x.mandatory+'</b> · failure → <b>'+x.failure+'</b></p></article>'
 ).join('');
 q('#promotionStates').innerHTML=g.promotion_states.map(x=>'<code>'+x+'</code>').join('');
}
