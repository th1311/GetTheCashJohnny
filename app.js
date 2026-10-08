'use strict';
window.cashCommand = '';
const frame=document.getElementById('game'),start=document.getElementById('start'),restart=document.getElementById('restart'),music=document.getElementById('music');
let ready=false,state='loading',muted=false,lastScore=0,lastTime=0;
function focusGame(){frame.contentWindow.focus()}
function command(action){if(!ready)return;window.cashCommand=action;focusGame();if(action==='start'||action==='restart'){if(!muted)music.play().catch(()=>{document.getElementById('sound').textContent='Enable sound';});}}
window.cashUpdate=(score,seconds,next)=>{ready=true;lastScore=score;lastTime=seconds;state=next;document.getElementById('loading').hidden=true;document.getElementById('score').textContent='$'+score;document.getElementById('time').innerHTML=seconds+'<span>s</span>';document.getElementById('status').textContent=({ready:'READY TO PLAY',playing:'RUN IN PROGRESS',paused:'PAUSED',over:'GAME OVER'})[next]||next;start.disabled=false;restart.disabled=false;start.textContent=({ready:'Play game',playing:'Pause',paused:'Resume',over:'Play again'})[next];if(next==='paused'||next==='over')music.pause();else if(next==='playing'&&!muted&&music.paused)music.play().catch(()=>{});};
start.onclick=()=>command(state==='playing'?'pause':'start');restart.onclick=()=>command('restart');
window.cashToggleSound=()=>{muted=!muted;music.muted=muted;const b=document.getElementById('sound');b.setAttribute('aria-pressed',String(muted));b.innerHTML=(muted?'Sound off':'Sound on')+' <kbd>M</kbd>';if(!muted&&state==='playing')music.play().catch(()=>{});};
document.getElementById('sound').onclick=window.cashToggleSound;
music.addEventListener('loadedmetadata',()=>{if(music.duration>177)music.currentTime=177;});
document.getElementById('fullscreen').onclick=()=>{const cabinet=document.querySelector('.cabinet');if(document.fullscreenElement)document.exitFullscreen();else if(cabinet.requestFullscreen)cabinet.requestFullscreen().then(focusGame).catch(()=>{});};
document.querySelectorAll('[data-dir]').forEach(b=>b.onclick=()=>command(b.dataset.dir));
window.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown',' ','Enter','r','R','m','M','a','A','w','W','s','S','d','D'].includes(e.key)){if(e.target.tagName==='BUTTON'&&(e.key===' '||e.key==='Enter'))return;e.preventDefault();if(e.key.toLowerCase()==='m')document.getElementById('sound').click();else if(e.key.toLowerCase()==='r')command('restart');else if(e.key===' '||e.key==='Enter')command(state==='playing'?'pause':'start');else command(({ArrowLeft:'left',ArrowRight:'right',ArrowUp:'up',ArrowDown:'down',a:'left',d:'right',w:'up',s:'down'})[e.key]||({a:'left',d:'right',w:'up',s:'down'})[e.key.toLowerCase()]);}});
window.addEventListener('blur',()=>{if(state==='playing'&&document.hidden)window.cashCommand='pause';});
document.addEventListener('visibilitychange',()=>{if(document.hidden&&state==='playing'){window.cashCommand='pause';music.pause();}});
document.getElementById('reload').onclick=()=>location.reload();setTimeout(()=>{if(!ready)document.getElementById('load-help').hidden=false},45000);
const mc=document.modelContext;if(mc?.registerTool){try{Promise.resolve(mc.registerTool({name:'read_game_status',description:'Read the current cash score, survival time, and game state.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:true},execute:()=>({score:lastScore,seconds:lastTime,state})})).catch(()=>{});}catch{}}
