/* RadioBioCalc canvas charts: compact self-contained renderer, no network dependency.
   Supports the bar / line / logarithmic line configurations used in this project.
   This is a small education-only renderer, not a drop-in replacement for Chart.js. */
(function () {
'use strict';
class ChartLite {
  constructor(canvas, config) {
    this.canvas = canvas; this.config = config;
    this.resize = () => this.draw();
    window.addEventListener('resize', this.resize);
    requestAnimationFrame(this.resize);
  }
  destroy() { window.removeEventListener('resize', this.resize); }
  draw() {
    const cfg=this.config, canvas=this.canvas, parent=canvas.parentElement;
    const rect=parent.getBoundingClientRect();
    const width=Math.max(260,Math.round(rect.width-4));
    const height=Math.max(245,Math.round(rect.height)||300);
    const ratio=Math.min(2,window.devicePixelRatio||1);
    canvas.style.width=width+'px'; canvas.style.height=height+'px';
    canvas.width=Math.round(width*ratio); canvas.height=Math.round(height*ratio);
    const c=canvas.getContext('2d'); c.scale(ratio,ratio); c.clearRect(0,0,width,height);
    c.fillStyle='#fff'; c.fillRect(0,0,width,height);
    const left=55,right=12,top=36,bottom=66;
    const pw=width-left-right, ph=height-top-bottom;
    if(pw<10||ph<10) return;
    const labels=cfg.data.labels||[], sets=cfg.data.datasets||[];
    const log=cfg.options?.scales?.y?.type==='logarithmic';
    const stack=!!cfg.options?.scales?.y?.stacked;
    let vals=[];
    sets.forEach(d=>(d.data||[]).forEach(v=>{if(typeof v==='number'&&Number.isFinite(v)) vals.push(v)}));
    let max=Math.max(1,...vals), min=log?0.0001:0;
    if(stack && cfg.type==='bar') max=Math.max(max,...labels.map((_,i)=>sets.reduce((s,d)=>s+((d.data||[])[i]||0),0)));
    if(log){max=1;min=0.0001;} else max*=1.12;
    const ty=(v)=> log ? top+ph*(1-(Math.log10(Math.max(min,v))-Math.log10(min))/(Math.log10(max)-Math.log10(min))) : top+ph*(1-v/max);
    c.font='12px Arial, sans-serif'; c.textBaseline='middle';
    c.strokeStyle='#e2e8f0'; c.fillStyle='#64748b'; c.lineWidth=1;
    for(let i=0;i<=4;i++){
      let y=top+i*ph/4; c.beginPath();c.moveTo(left,y);c.lineTo(width-right,y);c.stroke();
      let v=log?Math.pow(10,Math.log10(max)-(Math.log10(max)-Math.log10(min))*i/4):max*(1-i/4);
      c.textAlign='right'; c.fillText(v>=100?v.toFixed(0):v>=10?v.toFixed(1):v.toPrecision(2),left-9,y);
    }
    const xStep=pw/Math.max(1,labels.length);
    if(cfg.type==='bar'){
      const groups=sets.length, outer=xStep*0.67;
      labels.forEach((label,i)=>{
        let stackOff=0;
        sets.forEach((d,j)=>{
          let v=Math.max(0,d.data?.[i]||0); let bottomV=stack?stackOff:0;
          let barW=stack?outer:outer/groups;
          let x=left+(i+.5)*xStep-outer/2+(stack?0:j*barW);
          let y=ty(v+bottomV), base=ty(bottomV);
          let color=Array.isArray(d.backgroundColor)?d.backgroundColor[i%d.backgroundColor.length]:d.backgroundColor||'#0284c7';
          c.fillStyle=color; c.beginPath();
          const h=Math.max(0,base-y); const r=Math.min(5,h/3,barW/3);
          c.roundRect(x,y,Math.max(1,barW-2),h,[r,r,0,0]);c.fill();
          if(stack) stackOff+=v;
        });
        c.save();c.translate(left+(i+.5)*xStep,height-bottom+12);
        c.fillStyle='#475569';c.textAlign='center';c.font='10px Arial, sans-serif';
        const s=String(label); const words=s.split(' '), lines=[];let run='';
        words.forEach(w=>{if((run+' '+w).length>15){lines.push(run);run=w;}else run=(run+' '+w).trim();}); if(run) lines.push(run);
        lines.slice(0,3).forEach((line,k)=>c.fillText(line,0,k*12)); c.restore();
      });
    }else{
      const x=(i)=>left+i*pw/Math.max(1,labels.length-1);
      sets.forEach((d,j)=>{
        c.beginPath();c.lineWidth=2.7;c.strokeStyle=d.borderColor||['#0284c7','#e11d48'][j%2];
        let active=false;
        (d.data||[]).forEach((v,i)=>{
          if(v===null||!Number.isFinite(v)){active=false;return;}
          const px=x(i),py=ty(v);
          if(!active){c.moveTo(px,py);active=true}else c.lineTo(px,py);
        });c.stroke();
        if(d.pointRadius>0){(d.data||[]).forEach((v,i)=>{
          if(v==null||!Number.isFinite(v))return;
          c.beginPath();c.fillStyle=d.borderColor||'#e11d48';c.arc(x(i),ty(v),Math.min(d.pointRadius,6),0,2*Math.PI);c.fill();
        });}
      });
      const n=Math.min(6,labels.length-1);for(let i=0;i<=n;i++){
        const id=Math.round((labels.length-1)*i/Math.max(1,n));
        c.fillStyle='#64748b';c.font='11px Arial, sans-serif';c.textAlign='center';c.fillText(String(labels[id]),x(id),top+ph+18);
      }
    }
    // legend at top if >1 dataset
    if(sets.length>1){let legendX=left;sets.forEach((d,j)=>{
      const txt=String(d.label||'').slice(0,25);
      c.fillStyle=(d.borderColor||(Array.isArray(d.backgroundColor)?d.backgroundColor[0]:d.backgroundColor))||'#0284c7';
      c.fillRect(legendX,8,9,9);c.fillStyle='#475569';c.textAlign='left';c.font='10px Arial, sans-serif';c.fillText(txt,legendX+13,13);
      legendX+=Math.min(170,txt.length*5.5+25);
    });}
  }
}
window.Chart=ChartLite;
})();
