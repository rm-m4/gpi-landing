// Open a beta.goldenpi.com bond page's collapsed sections and Cashflow Timeline modal.
// Usage: node crawl/bond_expand.js <outdir> [/bonds/...path]

const path=require('path');
const {chromium}=require(path.resolve('node_modules/playwright-core'));
const fs=require('fs');
(async()=>{
 const cache=path.join(process.env.HOME,'Library/Caches/ms-playwright');
 const b=fs.readdirSync(cache).filter(d=>/^chromium-\d+$/.test(d)).sort((a,b)=>a.split('-')[1]-b.split('-')[1]).pop();
 const exe=['chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing','chrome-mac/Chromium.app/Contents/MacOS/Chromium'].map(r=>path.join(cache,b,r)).find(fs.existsSync);
 const br=await chromium.launch({executablePath:exe});
 const ctx=await br.newContext({viewport:{width:1440,height:1000},deviceScaleFactor:2});
 await ctx.addCookies([{name:'gp-locale',value:'en',domain:'beta.goldenpi.com',path:'/'}]);
 const p=await ctx.newPage();
 await p.goto('https://beta.goldenpi.com'+(process.argv[3]||'/bonds/INE911L07154/mahaveer-1200-bond-yield?src=view_details'),{waitUntil:'networkidle',timeout:120000});
 await p.waitForTimeout(3000);
 for(const t of ['Documents','Cashflow','Financial Ratio']){
   const h=p.getByText(t,{exact:true}).last();
   await h.scrollIntoViewIfNeeded(); await h.click(); await p.waitForTimeout(2500);
 }
 await p.screenshot({path:process.argv[2]+'/expanded.png',fullPage:true});
 // The financial charts are <canvas>; keep their pixels as <img> so a static copy shows them.
 await p.evaluate(()=>document.querySelectorAll('canvas').forEach(c=>{
   if(!c.width) return;
   const i=document.createElement('img'); i.src=c.toDataURL('image/png'); i.alt='';
   i.setAttribute('style',c.getAttribute('style')||''); i.className=c.className; c.replaceWith(i);
 }));
 fs.writeFileSync(process.argv[2]+'/expanded.html',await p.content());
 fs.writeFileSync(process.argv[2]+'/expanded.txt',await p.locator('main').first().innerText().catch(()=>p.innerText('body')));
 // cashflow timeline modal: whatever the click adds to <body> is the modal (portal + overlay)
 const before=await p.evaluate(()=>document.body.children.length);
 await p.locator('button:visible', {hasText:'Cashflow Timeline'}).first().click(); await p.waitForTimeout(2500);
 await p.screenshot({path:process.argv[2]+'/timeline.png'});
 const dlg=await p.locator('[role=dialog]').last().innerText().catch(()=>'(no dialog)');
 fs.writeFileSync(process.argv[2]+'/timeline.txt',dlg);
 fs.writeFileSync(process.argv[2]+'/timeline.html',await p.evaluate(n=>[...document.body.children].slice(n).map(e=>e.outerHTML).join('\n'),before));
 await br.close();
})();
