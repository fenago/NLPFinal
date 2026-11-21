
{
const s=document.getElementById('flow');
const nodes=[['GitHub repo','NLPFinal'],['Research','docs/'],['Roster','13 roles'],['Agents','NLTK + spaCy'],['Build app','by the agents'],['Netlify URL','submit it']];
const draw=()=>{const W=s.clientWidth,H=s.clientHeight;if(!W)return;const narrow=W<520;const cols=narrow?2:3,rows=Math.ceil(nodes.length/cols);const pad=12,cw=(W-pad*2)/cols,rh=(H-pad*2)/rows;const bw=Math.min(cw-28,200),bh=Math.min(rh-34,84);
let out='';const pos=nodes.map((n,i)=>{const r=Math.floor(i/cols);let c=i%cols;if(r%2===1)c=cols-1-c;return{x:pad+c*cw+(cw-bw)/2,y:pad+r*rh+(rh-bh)/2}});
for(let i=0;i<pos.length-1;i++){const a=pos[i],b=pos[i+1];const ax=a.x+bw/2,ay=a.y+bh/2,bx=b.x+bw/2,by=b.y+bh/2;out+=`<line x1="${ax}" y1="${ay}" x2="${bx}" y2="${by}" stroke="currentColor" stroke-opacity=".25" stroke-width="3" stroke-dasharray="6 6"/>`}
pos.forEach((p,i)=>{const last=i===pos.length-1;const cy=p.y+bh/2;out+=`<g><rect x="${p.x+4}" y="${p.y+6}" width="${bw}" height="${bh}" rx="14" fill="#101418" opacity=".12"/><rect x="${p.x}" y="${p.y}" width="${bw}" height="${bh}" rx="14" fill="${last?'#ffd84a':'var(--card)'}" stroke="${last?'#101418':'var(--line)'}"/><circle cx="${p.x+26}" cy="${cy}" r="13" fill="${last?'#101418':'#ffd84a'}"/><text x="${p.x+26}" y="${cy+4.5}" text-anchor="middle" font-size="13" font-weight="800" fill="${last?'#ffd84a':'#101418'}">${i+1}</text><text x="${p.x+48}" y="${cy-3}" font-size="${narrow?14:16}" font-weight="800" fill="${last?'#101418':'var(--ink)'}">${nodes[i][0]}</text><text x="${p.x+48}" y="${cy+15}" font-size="13" fill="${last?'#101418':'var(--soft)'}">${nodes[i][1]}</text></g>`});
s.innerHTML=out};
const ro=new ResizeObserver(draw);ro.observe(s);
document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',async()=>{const t=b.closest('.prompt').querySelector('pre').textContent;try{await navigator.clipboard.writeText(t);b.textContent='Copied'}catch(e){const r=document.createRange();r.selectNodeContents(b.closest('.prompt').querySelector('pre'));const sel=getSelection();sel.removeAllRanges();sel.addRange(r);b.textContent='Selected, press Ctrl/Cmd+C'}setTimeout(()=>b.textContent='Copy',2200)}));
const lb=document.getElementById('lb'),li=document.getElementById('lbimg');
document.querySelectorAll('.zoom').forEach(b=>b.addEventListener('click',()=>{li.src=b.dataset.src;li.alt=b.querySelector('img').alt;try{lb.showModal()}catch(e){}}));
lb.addEventListener('click',e=>{if(e.target===lb)lb.close()});
}
