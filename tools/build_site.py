#!/usr/bin/env python3
"""สร้าง docs/ ของแอปประจำเล่ม คู่มือการจัดทำงบกระแสเงินสด TAS 7 จาก src/tool1-6.html
ใช้: python3 build_site.py OUT_DOCS_DIR"""
import os, re, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
GATE_HASH = '30bbac4ed235952c14f284ee9df8f6ae0fcabe8beca6b4fb70cf67bf128dd116'  # SHA-256 ของรหัสเข้าแอป
AUTH_TH = 'ดร.วิทยา อรุณศิริเพ็ชร · อาจารย์พงษ์ธร ดวงปัญญา'
TITLE_TH = 'คู่มือการจัดทำงบกระแสเงินสด TAS 7 สำหรับบริษัทจดทะเบียนและบริษัทจำกัด'
TITLE_EN = 'A Guide to Preparing the Statement of Cash Flows under TAS 7 for Listed and Limited Companies'
NOTE = 'เนื้อหาเป็นการถอดความของคณะผู้เขียน ไม่ใช่ถ้อยคำของมาตรฐาน'
TOOLS = [
    (1, 'ทดสอบเงินสดและรายการเทียบเท่าเงินสด', 'บทที่ 2 · TAS 7 ย่อหน้า 6–9, 45–48'),
    (2, 'จัดกิจกรรมกระแสเงินสด', 'บทที่ 3 · TAS 7 ย่อหน้า 6, 12, 14–17, 31–36, 43'),
    (3, 'กระดาษทำการวิธีทางอ้อม', 'บทที่ 4 และบทที่ 6 · TAS 7 ย่อหน้า 18.2, 20, 43'),
    (4, 'งบกระแสเงินสดวิธีทางตรง', 'บทที่ 5 · TAS 7 ย่อหน้า 14, 18.1, 19'),
    (5, 'เลือกกรอบมาตรฐานและแบบรายการย่อ', 'บทที่ 1 และบทที่ 6 · NPAEs 2.1–2.4, 4.2'),
    (6, 'กระทบยอดหนี้สินตามสัญญาเช่า', 'บทที่ 11 · TFRS 16 ย่อหน้า 50 · TAS 7 ย่อหน้า 17, 43, 44ก–44จ'),
]

GATE = '''
<div id="gate" role="dialog" aria-modal="true" aria-labelledby="gate-h" style="position:fixed;inset:0;z-index:99999;background:#f5f7fa;display:flex;align-items:center;justify-content:center;padding:16px;font-family:'IBM Plex Sans Thai',system-ui,sans-serif;color:#18212e">
 <form id="gate-f" style="background:#fff;border:1px solid #d9dfe7;border-top:6px solid #E8731B;border-radius:12px;padding:22px 20px;max-width:420px;width:100%;display:grid;gap:12px">
  <img src="logo.png" alt="Dr.VIT &amp; PD" style="height:44px;width:auto;justify-self:start">
  <h2 id="gate-h" style="margin:0;font-size:1.1rem;line-height:1.4;color:#1D3E9E">แอปประกอบคู่มือการจัดทำงบกระแสเงินสด TAS 7</h2>
  <p style="margin:0;font-size:.92rem;color:#5a6676">สำหรับผู้ซื้อคู่มือ ใส่รหัสเข้าแอปที่พิมพ์ไว้ใต้ QR code ในเล่ม</p>
  <label style="display:grid;gap:4px;font-size:.88rem">รหัสเข้าแอป
   <span style="display:flex;gap:6px"><input id="gate-in" type="password" autocomplete="off" autocapitalize="characters" spellcheck="false" style="flex:1;min-width:0;font:inherit;font-size:1rem;padding:8px 10px;border:1px solid #d9dfe7;border-radius:8px">
   <button type="button" id="gate-show" style="font:inherit;font-size:.85rem;border:1px solid #d9dfe7;background:#fff;border-radius:8px;padding:0 10px;cursor:pointer">แสดง</button></span></label>
  <label style="display:flex;gap:8px;align-items:center;font-size:.88rem"><input type="checkbox" id="gate-rem" checked> จำรหัสในเครื่องนี้</label>
  <p id="gate-err" role="alert" style="margin:0;color:#b3362b;font-size:.88rem" hidden>รหัสไม่ถูกต้อง โปรดดูรหัสที่พิมพ์ไว้ในคู่มือ</p>
  <button type="submit" style="font:inherit;font-weight:600;border:0;border-radius:8px;padding:10px;background:#1D3E9E;color:#fff;cursor:pointer">เปิดแอป</button>
  <p style="margin:0;font-size:.78rem;color:#5a6676">''' + AUTH_TH + '''</p>
 </form>
</div>
<script>
(function(){
 var H='%s',K='tas7cf-ok',g=document.getElementById('gate');
 function ok(){try{if(localStorage.getItem(K)===H||sessionStorage.getItem(K)===H)return true}catch(e){}return false}
 function open(){g.remove();document.documentElement.style.overflow=''}
 if(ok()){open();return}
 document.documentElement.style.overflow='hidden';
 var inp=document.getElementById('gate-in');
 document.getElementById('gate-show').onclick=function(){var p=inp.type==='password';inp.type=p?'text':'password';this.textContent=p?'ซ่อน':'แสดง'};
 document.getElementById('gate-f').onsubmit=function(e){e.preventDefault();
  var v=inp.value.toUpperCase().replace(/[\\s-]/g,'');
  crypto.subtle.digest('SHA-256',new TextEncoder().encode(v)).then(function(b){
   var h=Array.from(new Uint8Array(b)).map(function(x){return x.toString(16).padStart(2,'0')}).join('');
   if(h!==H){document.getElementById('gate-err').hidden=false;return}
   try{(document.getElementById('gate-rem').checked?localStorage:sessionStorage).setItem(K,H)}catch(e){}
   open()})};
 inp.focus();
})();
</script>
''' % GATE_HASH

BRAND_IMG = re.compile(r'<img src="data:image/jpeg;base64,[^"]+" alt="Dr\.VIT &amp; PD"[^>]*>')
NEW_IMG = '<a href="index.html" title="หน้าแรกของแอป"><img src="logo.png" alt="Dr.VIT &amp; PD" style="height:40px;width:auto;display:block"></a>'
OLD_SPAN = 'คู่มือการจัดทำงบกระแสเงินสด TAS 7<br>ดร.วิทยา อรุณศิริเพ็ชร</span>'
NEW_SPAN = 'คู่มือการจัดทำงบกระแสเงินสด TAS 7<br>ดร.วิทยา อรุณศิริเพ็ชร<br>อาจารย์พงษ์ธร ดวงปัญญา' + '<br><a href="index.html" style="color:#1D3E9E">กลับหน้าแรกของแอป</a></span>'

for n, name, ref in TOOLS:
    s = open(os.path.join(HERE, 'src', f'tool{n}.html'), encoding='utf-8').read()
    if s.lower().startswith('<!doctype html><html><head><meta charset=utf8>'):   # ตัวห่อจากการอ่านแอปเดิม
        s = s[s.index('<!DOCTYPE html>'):]
    s, k1 = BRAND_IMG.subn(NEW_IMG, s); assert k1 == 1, (n, 'logo')
    assert s.count(OLD_SPAN) == 1, (n, 'span'); s = s.replace(OLD_SPAN, NEW_SPAN)
    s = s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '').replace('<meta name="claude:viewport-fit-sides" content="cover">', '')
    s = s.replace('© ดร.วิทยา อรุณศิริเพ็ชร</p>', '© ดร.วิทยา อรุณศิริเพ็ชร และ อาจารย์พงษ์ธร ดวงปัญญา · ' + NOTE + '</p>')
    if NOTE not in s:   # เครื่องมือที่ 1 ไม่มีบรรทัด ©
        s = s.replace('ไม่ใช่ความเห็นทางวิชาชีพสำหรับกรณีเฉพาะ</p>\n</div>', 'ไม่ใช่ความเห็นทางวิชาชีพสำหรับกรณีเฉพาะ</p>\n  <p class="foot">© ดร.วิทยา อรุณศิริเพ็ชร และ อาจารย์พงษ์ธร ดวงปัญญา · ' + NOTE + '</p>\n</div>', 1)
    assert NOTE in s, (n, 'note')
    s = s.rstrip()
    s = (s[:-len('</html>')] + GATE + '</html>\n') if s.endswith('</html>') else (s + '\n' + GATE)
    open(os.path.join(OUT, f'tool{n}.html'), 'w', encoding='utf-8').write(s)

cards = ''.join(f'''<a class="card" href="tool{n}.html"><span class="no">{n}</span><span><b>{name}</b><small>{ref}</small></span></a>''' for n, name, ref in TOOLS)
INDEX = f'''<!DOCTYPE html>
<html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>แอปประกอบคู่มือ TAS 7</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;600;700&family=Sarabun:ital,wght@0,400;1,400&display=swap">
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#f5f7fa;color:#18212e;font-family:"IBM Plex Sans Thai",system-ui,sans-serif;line-height:1.6}}
.bar{{height:8px;background:linear-gradient(90deg,#E8731B 0%,#C8612A 30%,#5B4C8C 62%,#1D3E9E 100%)}}
.wrap{{max-width:880px;margin:0 auto;padding:24px 16px 40px;display:grid;gap:18px}}
.logo{{height:52px;width:auto}}
h1{{margin:0;font-size:clamp(1.3rem,3.6vw,1.8rem);line-height:1.35;color:#1D3E9E}}
.en{{font-family:Sarabun,sans-serif;font-style:italic;color:#1F3864;margin:4px 0 0}}
.au{{margin:0;color:#5a6676}}
.intro{{background:#FBF1E8;border-left:5px solid #E8731B;border-radius:0 10px 10px 0;padding:12px 14px;font-size:.95rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}}
.card{{display:grid;grid-template-columns:36px minmax(0,1fr);gap:10px;align-items:start;background:#fff;border:1px solid #d9dfe7;border-radius:10px;padding:14px;text-decoration:none;color:inherit}}
.card:hover,.card:focus-visible{{border-color:#1D3E9E;outline:none;box-shadow:0 0 0 2px #e3ecf8}}
.no{{width:36px;height:36px;border-radius:50%;background:#1D3E9E;color:#fff;display:grid;place-items:center;font-weight:700}}
.card b{{display:block;color:#1D3E9E}} .card small{{color:#5a6676;font-size:.82rem}}
footer{{font-size:.82rem;color:#5a6676;border-top:1px solid #d9dfe7;padding-top:12px}}
</style></head><body>
<div class="bar"></div>
<div class="wrap">
 <img class="logo" src="logo.png" alt="Dr.VIT &amp; PD">
 <header><h1>แอปประกอบ{TITLE_TH}</h1><p class="en">{TITLE_EN}</p><p class="au">{AUTH_TH}</p></header>
 <p class="intro">แอป 6 เครื่องมือนี้ใช้คู่กับคู่มือ ข้อมูลตั้งต้นเป็นตัวอย่างชุดเดียวกับในเล่ม เปิดเครื่องมือจาก QR code ท้ายบทที่เกี่ยวข้อง หรือเลือกจากรายการด้านล่าง แก้ตัวเลขได้ทุกช่องเพื่อทดลองสถานการณ์อื่น</p>
 <nav class="grid" aria-label="เครื่องมือทั้ง 6">{cards}</nav>
 <footer>{NOTE} เครื่องมือใช้เพื่อการเรียนรู้ ไม่ใช่ความเห็นทางวิชาชีพสำหรับกรณีเฉพาะ · © {AUTH_TH} · Dr.VIT &amp; PD</footer>
</div>
{GATE}
</body></html>
'''
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(INDEX)
shutil.copy(os.path.join(HERE, 'logo.png'), os.path.join(OUT, 'logo.png'))
open(os.path.join(OUT, '.nojekyll'), 'w').close()
print('สร้างแล้ว', sorted(os.listdir(OUT)))
