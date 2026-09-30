const REPO="https://github.com/VictorKVS/OTUS-";const BRANCH="feature/otus-homework-site";
const labels={done:"ГОТОВО",review:"REVIEW",draft:"DRAFT",lab:"LAB",materials:"МАТЕРИАЛЫ"};
function list(items){return items&&items.length?'<ul>'+items.map(x=>'<li>'+escapeHtml(typeof x==="string"?x:(x.title||x.name||JSON.stringify(x)))+'</li>').join('')+'</ul>':'<p class="gap">GAP · данных пока нет.</p>'}
function escapeHtml(s){return String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]))}
function qs(name){return new URLSearchParams(location.search).get(name)}
async function getJson(url){const r=await fetch(url,{cache:"no-store"});if(!r.ok)throw new Error(url+" → HTTP "+r.status);return r.json()}
async function init(){
 const id=Number(qs("id")||1);
 const [course,caps]=await Promise.all([getJson("./data/course-manifest.json"),getJson("./data/capabilities.json")]);
 const lesson=course.lessons.find(x=>x.id===id);if(!lesson)throw new Error("Lesson "+id+" not found");
 const ordered=[...course.lessons].sort((a,b)=>a.id-b.id);const pos=ordered.findIndex(x=>x.id===id);
 document.querySelectorAll(".prevLesson").forEach(a=>{const p=pos>0?ordered[pos-1]:null;if(p){a.href="./lesson-template.html?id="+p.id;a.textContent="← Lesson "+String(p.id).padStart(2,"0")}else{a.classList.add("is-disabled");a.removeAttribute("href")}});
 document.querySelectorAll(".nextLesson").forEach(a=>{const n=pos>=0&&pos<ordered.length-1?ordered[pos+1]:null;if(n){a.href="./lesson-template.html?id="+n.id;a.textContent="Lesson "+String(n.id).padStart(2,"0")+" →"}else{a.classList.add("is-disabled");a.removeAttribute("href")}});

 let detail=null;try{detail=await getJson("./data/lesson-details/"+String(id).padStart(2,"0")+".json")}catch(_){detail=null}
 document.title="Lesson "+String(id).padStart(2,"0")+" · "+lesson.title+" · FATHER Architect OS";
 document.querySelector("#lessonEyebrow").textContent="LESSON "+String(id).padStart(2,"0")+" · "+lesson.gate;
 document.querySelector("#lessonTitle").innerHTML=escapeHtml(lesson.title);
 document.querySelector("#lessonPurpose").textContent=detail?.purpose||"Урок ещё не нормализован в detail manifest. Базовая информация загружена из course manifest.";
 document.querySelector("#metaGate").textContent=lesson.gate;document.querySelector("#metaStatus").textContent=labels[lesson.status]||lesson.status;
 document.querySelector("#metaMaturity").textContent=lesson.maturity;const courseStatus=lesson.curriculum?.submission_status||"unknown";document.querySelector("#metaCourse").textContent=courseStatus==="not_submitted_in_source"?"НЕ СДАНО (ИСТОЧНИК)":courseStatus==="accepted"?"ПРИНЯТО":"НЕ ПОДТВЕРЖДЕНО";document.querySelector("#metaCaps").textContent=(lesson.father_production?.capability_ids||[]).length;
 const flow=detail?.schema?.notation?.split(/\s*→\s*/).filter(Boolean)||["OTUS","Architect Pro","FATHER Production","Evidence"];
 document.querySelector("#schemaFlow").innerHTML=flow.map(x=>'<span>'+escapeHtml(x)+'</span>').join("");
 document.querySelector("#schemaNote").textContent=detail?.schema?.description||"GAP · lesson-specific engineering schema ещё не опубликована.";
 const poster=detail?.visual?.poster;
 document.querySelector("#posterWrap").innerHTML=poster?'<img src="'+escapeHtml(poster)+'" alt="'+escapeHtml(detail?.visual?.alt||lesson.title)+'"/>':'<div class="empty">GAP · visual poster будет создан при нормализации урока.</div>';
 document.querySelector("#curriculum").innerHTML='<p>'+escapeHtml(detail?.curriculum?.summary||lesson.evidence)+'</p>'+list(detail?.curriculum?.requirements||[]);
 document.querySelector("#architectPro").innerHTML='<p>'+escapeHtml(detail?.architect_pro?.summary||"Профессиональное расширение пока не нормализовано.")+'</p><b>Методы</b>'+list(detail?.architect_pro?.methods||[])+'<b>Шаблоны</b>'+list(detail?.architect_pro?.templates||[])+'<b>Red flags</b>'+list(detail?.architect_pro?.anti_patterns||[]);
 const ids=lesson.father_production?.capability_ids||[];const related=caps.components.filter(c=>ids.includes(c.id));
 document.querySelector("#fatherProduction").innerHTML='<p>'+escapeHtml(detail?.father_production?.summary||"Production mapping взят из capability manifest.")+'</p><b>Capabilities</b>'+list(related.map(c=>c.id+" · "+c.name))+'<b>Runtime notes</b>'+list(detail?.father_production?.runtime_notes||[]);
 document.querySelector("#artifacts").innerHTML=list(detail?.artifacts||[]);
 document.querySelector("#evidenceList").innerHTML=list(detail?.evidence||[]);
 document.querySelector("#traceability").innerHTML=list(detail?.traceability||[]);
 document.querySelector("#gaps").innerHTML=list(detail?.gaps||["Lesson-specific detail manifest отсутствует или неполон."]);
 document.querySelector("#maturityText").textContent="Текущий уровень: "+lesson.maturity+". Статус: "+(labels[lesson.status]||lesson.status)+". Уровень повышается только после evidence.";
 const src=(detail?.sources||[]).concat([{title:"Git artifacts",url:REPO+"/tree/"+BRANCH+"/"+lesson.path}]);
 document.querySelector("#sources").innerHTML='<ul>'+src.map(s=>'<li><a class="inline-link" target="_blank" rel="noopener" href="'+escapeHtml(s.url)+'">'+escapeHtml(s.title||s.url)+'</a></li>').join('')+'</ul>';
}
const root=document.documentElement;const saved=localStorage.getItem("otus-theme");if(saved)root.dataset.theme=saved;document.querySelector("#themeToggle").onclick=()=>{const n=root.dataset.theme==="light"?"dark":"light";root.dataset.theme=n;localStorage.setItem("otus-theme",n)};
init().catch(e=>{document.querySelector("#lessonTitle").textContent="Ошибка загрузки";document.querySelector("#lessonPurpose").textContent=e.message});
