const $=s=>document.querySelector(s);
let DATA=null,RULES=null,selected=null,currentTab='config';
const STORAGE_KEY='father.project-builder.state.v1';
const esc=v=>String(v??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

let STATE={
  project_id:null,
  prompt:'',
  build_lane:[],
  runtime_graph:[],
  matched_rules:[],
  missing_blocks:[],
  configs:{},
  lab_requests:[],
  blocked_blocks:[]
};

function statusClass(s){return 'node-'+String(s||'').toLowerCase().replaceAll(' ','_')}
function blockById(id){return DATA.blocks.find(x=>x.id===id)}
function unique(xs){return [...new Set(xs)]}
function orderBy(ids,order){const set=new Set(ids);return order.filter(x=>set.has(x)).concat(ids.filter(x=>!order.includes(x)))}

function persist(){localStorage.setItem(STORAGE_KEY,JSON.stringify(STATE))}
function restore(){
  try{
    const raw=localStorage.getItem(STORAGE_KEY);
    if(raw) STATE={...STATE,...JSON.parse(raw)};
  }catch(_){}
}
async function projectId(prompt){
  const bytes=new TextEncoder().encode(prompt.trim());
  if(window.crypto?.subtle){
    const h=await crypto.subtle.digest('SHA-256',bytes);
    const hex=[...new Uint8Array(h)].map(x=>x.toString(16).padStart(2,'0')).join('').slice(0,10).toUpperCase();
    return 'PRJ-'+hex;
  }
  return 'PRJ-'+Date.now().toString(36).toUpperCase();
}

function composeFromPrompt(prompt){
  const text=prompt.toLowerCase();
  let build=[...RULES.always_build_lane],runtime=[],matched=[];
  for(const rule of RULES.rules){
    if((rule.match_any||[]).some(k=>text.includes(String(k).toLowerCase()))){
      matched.push(rule.id);
      build.push(...(rule.add_build||[]));
      runtime.push(...(rule.add_runtime||[]));
    }
  }
  build=orderBy(unique(build),RULES.ordering.build_lane);
  runtime=orderBy(unique(runtime),RULES.ordering.runtime_graph);
  const all=[...build,...runtime].map(blockById).filter(Boolean);
  const missing=all.filter(x=>['NEW_BLOCK_REQUIRED','BLOCKED','FAILED'].includes(x.status)).map(x=>x.id);
  return {build_lane:build,runtime_graph:runtime,matched_rules:matched,missing_blocks:missing};
}

function renderPalette(){
  const q=$('#blockSearch').value.toLowerCase();
  const cat=$('#categoryFilter').value;
  const rows=DATA.blocks.filter(x=>(cat==='ALL'||x.category===cat)&&(!q||x.name.toLowerCase().includes(q)||x.id.toLowerCase().includes(q)));
  $('#blockPalette').innerHTML=rows.map(x=>'<div class="palette-block" data-id="'+x.id+'"><b>'+esc(x.name)+'</b><small>'+esc(x.category)+' · '+esc(x.status)+'</small></div>').join('');
  document.querySelectorAll('.palette-block').forEach(x=>x.onclick=()=>inspect(x.dataset.id));
}

function node(x){
  if(!x) return '';
  const blocked=STATE.blocked_blocks.includes(x.id)?' · USER_BLOCKED':'';
  return '<div class="graph-node '+statusClass(x.status)+(STATE.blocked_blocks.includes(x.id)?' user-blocked':'')+'" data-id="'+x.id+'"><b>'+esc(x.name)+'</b><small>'+esc(x.category)+' · '+esc(x.source)+'</small><em>'+esc(x.status)+blocked+'</em></div>';
}
function laneHtml(ids){
  if(!ids.length) return '<div class="lane-empty">Для этой задачи runtime-блоки пока не выбраны.</div>';
  let html='';
  for(let i=0;i<ids.length;i+=2){
    const a=blockById(ids[i]),b=ids[i+1]?blockById(ids[i+1]):null;
    html+='<div class="graph-row"><span class="graph-index">'+String(i+1).padStart(2,'0')+'</span>'+node(a)+(b?'<span class="graph-arrow">→</span>'+node(b):'')+'</div>';
  }
  return html;
}
function renderCanvas(){
  $('#buildLane').innerHTML=laneHtml(STATE.build_lane);
  $('#runtimeGraph').innerHTML=laneHtml(STATE.runtime_graph);
  document.querySelectorAll('.graph-node').forEach(x=>x.onclick=()=>inspect(x.dataset.id));
  $('#gateStrip').innerHTML=DATA.project_template.gates.map(x=>'<span>'+x+'</span>').join('');
  $('#projectId').textContent=STATE.project_id||'—';
  $('#buildCount').textContent=STATE.build_lane.length;
  $('#runtimeCount').textContent=STATE.runtime_graph.length;
  $('#missingCount').textContent=STATE.missing_blocks.length;
  renderCompositionReport();
}
function renderCompositionReport(){
  const count=STATE.build_lane.length+STATE.runtime_graph.length;
  const status=STATE.missing_blocks.length?'HUMAN ENGINEERING REQUIRED':'GRAPH COMPOSED';
  $('#compositionReport').innerHTML=
    '<span>FACTORY CONTROLLER · '+esc(status)+'</span>'+
    '<b>'+count+' blocks · '+STATE.build_lane.length+' build · '+STATE.runtime_graph.length+' runtime</b>'+
    '<small>Rules: '+esc(STATE.matched_rules.join(' · ')||'baseline only')+(STATE.missing_blocks.length?' · Missing: '+esc(STATE.missing_blocks.join(', ')):' · Registry-only composition PASS')+'</small>';
}

const TABS={config:'config',metrics:'metrics',tests:'tests',evidence:'evidence',security:'security',ownership:'ownership',tools:'tools'};
function inspect(id){
  selected=blockById(id); if(!selected)return;
  $('#inspectorEmpty').hidden=true; $('#inspector').hidden=false;
  document.querySelectorAll('.graph-node').forEach(x=>x.classList.toggle('selected',x.dataset.id===id));
  $('#inspectCategory').textContent=selected.category;
  $('#inspectName').textContent=selected.name;
  $('#inspectSource').textContent=selected.source+(selected.agent_id?' · '+selected.agent_id:'');
  $('#inspectStatus').textContent=selected.status;
  $('#inspectDescription').textContent=selected.description;
  $('#inspectInputs').innerHTML=selected.inputs.map(x=>'<span>'+esc(x)+'</span>').join('');
  $('#inspectOutputs').innerHTML=selected.outputs.map(x=>'<span>'+esc(x)+'</span>').join('');
  renderInspectTab();
}
function cfgFor(id){
  STATE.configs[id]??={config:{},selections:{}};
  return STATE.configs[id];
}
function renderInspectTab(){
  if(!selected)return;
  document.querySelectorAll('#inspectTabs button').forEach(x=>x.classList.toggle('active',x.dataset.tab===currentTab));
  const rows=selected[TABS[currentTab]]||[];
  const cfg=cfgFor(selected.id);
  if(currentTab==='config'){
    $('#inspectTabBody').innerHTML=rows.map((x,i)=>{
      const val=cfg.config[x]||'';
      return '<div class="inspect-config-row"><label>'+esc(x)+'</label><input data-config-key="'+esc(x)+'" value="'+esc(val)+'" placeholder="значение / policy / profile"><small>'+String(i+1).padStart(2,'0')+'</small></div>';
    }).join('')||'<p class="muted">Нет параметров.</p>';
    document.querySelectorAll('[data-config-key]').forEach(inp=>inp.oninput=()=>{cfg.config[inp.dataset.configKey]=inp.value;persist()});
  }else{
    cfg.selections[currentTab]??={};
    $('#inspectTabBody').innerHTML=rows.map((x,i)=>{
      const checked=cfg.selections[currentTab][x]!==false;
      return '<div class="inspect-row"><input data-select-key="'+esc(x)+'" type="checkbox" '+(checked?'checked':'')+'><label>'+esc(x)+'</label><small>'+String(i+1).padStart(2,'0')+'</small></div>';
    }).join('')||'<p class="muted">Нет параметров.</p>';
    document.querySelectorAll('[data-select-key]').forEach(inp=>inp.onchange=()=>{cfg.selections[currentTab][inp.dataset.selectKey]=inp.checked;persist()});
  }
}
function renderAgents(){
  const agents=DATA.blocks.filter(x=>x.agent_id);
  $('#agentSummary').innerHTML=agents.map(x=>'<div class="summary-card"><b>'+esc(x.name)+'</b><small>'+esc(x.agent_id)+' · '+esc(x.status)+'</small></div>').join('');
  const current=unique([...STATE.build_lane,...STATE.runtime_graph]).map(blockById).filter(Boolean);
  const truths=current.filter(x=>['NEW_BLOCK_REQUIRED','DESIGN','CANDIDATE_NEEDS_EXTRACTION','EXPERIMENTAL'].includes(x.status));
  $('#truthSummary').innerHTML=truths.map(x=>'<div class="truth-item"><b>'+esc(x.name)+'</b> — '+esc(x.status)+'</div>').join('')||'<div class="truth-item">В текущем графе нет DESIGN/NEW_BLOCK_REQUIRED блоков.</div>';
}

async function compose(){
  const prompt=$('#projectPrompt').value.trim();
  if(!prompt)return;
  const result=composeFromPrompt(prompt);
  STATE.prompt=prompt;
  STATE.project_id=await projectId(prompt);
  STATE.build_lane=result.build_lane;
  STATE.runtime_graph=result.runtime_graph;
  STATE.matched_rules=result.matched_rules;
  STATE.missing_blocks=result.missing_blocks;
  persist();
  $('#projectName').textContent='Project · '+STATE.project_id;
  renderCanvas(); renderAgents();
  inspect(STATE.build_lane[0]);
}

function resetTemplate(){
  const t=DATA.project_template;
  STATE={
    project_id:null,
    prompt:t.task,
    build_lane:[...t.build_lane],
    runtime_graph:[...t.runtime_graph],
    matched_rules:['TEMPLATE'],
    missing_blocks:unique([...t.build_lane,...t.runtime_graph]).map(blockById).filter(x=>x&&x.status==='NEW_BLOCK_REQUIRED').map(x=>x.id),
    configs:{},lab_requests:[],blocked_blocks:[]
  };
  $('#projectPrompt').value=t.task;
  $('#projectName').textContent=t.name;
  persist(); renderCanvas(); renderAgents(); inspect(t.build_lane[0]);
}
function exportState(){
  const payload={
    schema_version:'father-project-graph.v1',
    generated_at:new Date().toISOString(),
    ...STATE,
    blocks:unique([...STATE.build_lane,...STATE.runtime_graph]).map(id=>{
      const b=blockById(id); return {id,status:b?.status,source:b?.source,agent_id:b?.agent_id||null,configuration:STATE.configs[id]||{}};
    })
  };
  const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
  const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=(STATE.project_id||'father-project')+'.json';a.click();URL.revokeObjectURL(url);
}

async function init(){
  const [dr,rr]=await Promise.all([
    fetch('./data/father-builder-blocks.json',{cache:'no-store'}),
    fetch('./data/father-composition-rules.json',{cache:'no-store'})
  ]);
  DATA=await dr.json(); RULES=await rr.json();
  const cats=[...new Set(DATA.blocks.map(x=>x.category))];
  $('#categoryFilter').innerHTML='<option value="ALL">Все категории</option>'+cats.map(x=>'<option>'+x+'</option>').join('');
  restore();
  if(!STATE.build_lane.length&&!STATE.runtime_graph.length){
    STATE.prompt=DATA.project_template.task;
    STATE.build_lane=[...DATA.project_template.build_lane];
    STATE.runtime_graph=[...DATA.project_template.runtime_graph];
    STATE.matched_rules=['TEMPLATE'];
    STATE.missing_blocks=unique([...STATE.build_lane,...STATE.runtime_graph]).map(blockById).filter(x=>x&&x.status==='NEW_BLOCK_REQUIRED').map(x=>x.id);
  }
  $('#projectPrompt').value=STATE.prompt||DATA.project_template.task;
  $('#projectName').textContent=STATE.project_id?'Project · '+STATE.project_id:DATA.project_template.name;
  renderPalette(); renderCanvas(); renderAgents(); inspect((STATE.build_lane[0]||STATE.runtime_graph[0]));
}

$('#blockSearch').addEventListener('input',()=>DATA&&renderPalette());
$('#categoryFilter').addEventListener('change',()=>DATA&&renderPalette());
document.querySelectorAll('#inspectTabs button').forEach(x=>x.onclick=()=>{currentTab=x.dataset.tab;renderInspectTab()});
$('#composeBtn').onclick=()=>compose().catch(e=>alert('COMPOSE BLOCKED: '+e.message));
$('#resetBtn').onclick=()=>DATA&&resetTemplate();
$('#saveConfigBtn').onclick=()=>{persist();alert('Конфигурация блока сохранена локально в Project Builder.')};
$('#sendLabBtn').onclick=()=>{if(!selected)return;STATE.lab_requests=unique([...STATE.lab_requests,selected.id]);persist();alert(selected.name+' отмечен для передачи в LAB. Исполнение LAB пока не подключено к этой странице.')};
$('#blockBtn').onclick=()=>{if(!selected)return;STATE.blocked_blocks=unique([...STATE.blocked_blocks,selected.id]);persist();renderCanvas();inspect(selected.id)};
$('#exportBtn').onclick=()=>exportState();
init().catch(e=>document.body.insertAdjacentHTML('beforeend','<pre>'+esc(e.message)+'</pre>'));