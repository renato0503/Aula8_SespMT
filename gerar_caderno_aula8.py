# -*- coding: utf-8 -*-
"""Gerador do caderno HTML da Aula 8 - SESP/MT.

Foco: construir o MVP (TypeScript + Python, PWA) no Antigravity a partir do
contexto.md e do sprint.md vindos do NotebookLM, versionar no GitHub e publicar
no GitHub Pages. Inclui biblioteca de prompts para o agente.

Mesmo sistema visual das Aulas 3-7 (CSS base copiado do gerador da Aula 6).

Uso:
    python gerar_caderno_aula8.py                  # gera caderno-dia8.html
    python gerar_caderno_aula8.py paginas.json     # idem, com nº de página no sumário
O PDF é gerado por exportar_pdf.py (que chama este script duas vezes).
"""
import html
import json
import pathlib
import re
import sys

AQUI = pathlib.Path(__file__).resolve().parent
OUT = AQUI / "caderno-dia8.html"
PAGINAS = {}
if len(sys.argv) > 1 and pathlib.Path(sys.argv[1]).exists():
    PAGINAS = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))

# =================================================================
# CSS
# =================================================================
CSS_BASE = r"""
:root{
  --paper:#faf9f6; --surface:#ffffff; --raised:#f3f1ec;
  --ink:#1a1d1e; --ink-soft:#4a4f52; --ink-faint:#82888c;
  --accent:#1f4b8f; --accent-soft:#e8eefa;
  --verde:#1c8a5b; --verde-soft:#e4f5ec;
  --ambar:#b4790a; --ambar-soft:#fbeed9;
  --vermelho:#c33b3b; --vermelho-soft:#fbe7e7;
  --roxo:#6b3fa0; --roxo-soft:#efe6f8;
  --border:#e3e0d8; --code-bg:#1e2124; --code-ink:#e6e6e6;
  --shadow: 0 1px 2px rgba(0,0,0,.04), 0 4px 14px rgba(0,0,0,.05);
}
:root[data-theme="dark"]{
  --paper:#15171a; --surface:#1b1e22; --raised:#20242a;
  --ink:#eceeef; --ink-soft:#b6bcc2; --ink-faint:#7d858c;
  --accent:#6fa1e8; --accent-soft:#1c2a3f;
  --verde:#5cc797; --verde-soft:#123528;
  --ambar:#e0ac4c; --ambar-soft:#3a2c11;
  --vermelho:#e77f7f; --vermelho-soft:#3a1c1c;
  --roxo:#b18ce0; --roxo-soft:#2a1f3a;
  --border:#2c3036; --code-bg:#0f1113; --code-ink:#d8dadb;
  --shadow: 0 1px 2px rgba(0,0,0,.3), 0 4px 18px rgba(0,0,0,.35);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#15171a; --surface:#1b1e22; --raised:#20242a;
    --ink:#eceeef; --ink-soft:#b6bcc2; --ink-faint:#7d858c;
    --accent:#6fa1e8; --accent-soft:#1c2a3f;
    --verde:#5cc797; --verde-soft:#123528;
    --ambar:#e0ac4c; --ambar-soft:#3a2c11;
    --vermelho:#e77f7f; --vermelho-soft:#3a1c1c;
    --roxo:#b18ce0; --roxo-soft:#2a1f3a;
    --border:#2c3036; --code-bg:#0f1113; --code-ink:#d8dadb;
  }
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:'Source Serif 4', Georgia, serif; font-size:17px; line-height:1.65;
}
h1,h2,h3,h4,.ui{font-family:'Archivo',sans-serif}
code,pre,.mono{font-family:'JetBrains Mono',monospace}
a{color:var(--accent)}
header.top{
  padding:40px 24px 28px; border-bottom:1px solid var(--border);
  background:linear-gradient(180deg,var(--surface),var(--paper));
}
header.top .inner{max-width:1160px;margin:0 auto}
.kicker{font-family:'Archivo',sans-serif;font-size:12.5px;letter-spacing:.09em;text-transform:uppercase;
  color:var(--accent); background:var(--accent-soft); display:inline-block; padding:4px 10px; border-radius:20px; font-weight:600;}
header.top h1{font-size:clamp(28px,4vw,42px); margin:14px 0 6px; letter-spacing:-.01em}
header.top p.sub{color:var(--ink-soft); font-size:17px; margin:0; max-width:760px}
header.top .meta{margin-top:14px; font-size:13.5px; color:var(--ink-faint); font-family:'Archivo',sans-serif}
.wrap.shell{
  max-width:1160px; margin:0 auto; padding:28px 24px 100px;
  display:grid; grid-template-columns:1fr; gap:28px;
}
@media(min-width:1000px){ .wrap.shell{grid-template-columns:250px 1fr;} }
nav.toc{
  align-self:start; position:sticky; top:16px; max-height:calc(100vh - 32px); overflow:auto;
  background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:16px;
  font-family:'Archivo',sans-serif; font-size:13.3px;
}
nav.toc input{
  width:100%; padding:8px 10px; margin-bottom:10px; border-radius:8px; border:1px solid var(--border);
  background:var(--paper); color:var(--ink); font-family:inherit; font-size:12.8px;
}
nav.toc .grp{color:var(--ink-faint); text-transform:uppercase; letter-spacing:.06em; font-size:10.8px;
  font-weight:700; margin:14px 0 5px;}
nav.toc .grp:first-child{margin-top:0}
nav.toc a{display:block; color:var(--ink-soft); text-decoration:none; padding:4.5px 8px; border-radius:7px; line-height:1.35}
nav.toc a:hover{background:var(--raised); color:var(--ink)}
nav.toc a.active{background:var(--accent-soft); color:var(--accent); font-weight:600}
main section{
  background:var(--surface); border:1px solid var(--border); border-radius:16px;
  padding:30px 32px; margin-bottom:22px; box-shadow:var(--shadow); scroll-margin-top:16px;
}
main section .secnum{font-family:'Archivo',sans-serif; font-size:12px; color:var(--ink-faint); letter-spacing:.08em; text-transform:uppercase}
main section h2{font-size:24px; margin:6px 0 16px; letter-spacing:-.01em}
main section h3{font-size:17.5px; margin:22px 0 8px}
main section p{margin:0 0 13px}
main section ul, main section ol{margin:0 0 13px; padding-left:22px}
main section li{margin-bottom:5px}
.ficha{border-radius:12px; padding:16px 18px; margin:16px 0; border-left:4px solid var(--accent); background:var(--accent-soft); font-family:'Archivo',sans-serif; font-size:15px}
.ficha.g{border-color:var(--verde); background:var(--verde-soft)}
.ficha.a{border-color:var(--ambar); background:var(--ambar-soft)}
.ficha.r{border-color:var(--vermelho); background:var(--vermelho-soft)}
.ficha.p{border-color:var(--roxo); background:var(--roxo-soft)}
.ficha b.lbl{display:block; text-transform:uppercase; font-size:11px; letter-spacing:.08em; margin-bottom:5px; opacity:.85}
.callout{border-radius:12px; padding:14px 18px; margin:16px 0; font-size:15.3px; border:1px solid var(--border); background:var(--raised)}
.callout.note{border-color:var(--accent); background:var(--accent-soft)}
.callout.tip{border-color:var(--verde); background:var(--verde-soft)}
.callout.err{border-color:var(--vermelho); background:var(--vermelho-soft)}
.callout.purple{border-color:var(--roxo); background:var(--roxo-soft)}
.callout b.lbl{font-family:'Archivo',sans-serif; text-transform:uppercase; font-size:11px; letter-spacing:.08em; display:block; margin-bottom:5px}
ul.f{list-style:none; margin:16px 0; padding:14px 16px; border-radius:12px; background:var(--code-bg); color:var(--code-ink);
  font-family:'JetBrains Mono',monospace; font-size:13.6px; overflow-x:auto; position:relative;}
ul.f li{white-space:pre; margin:0; padding:1px 0}
ul.f::before{content:attr(data-lang); position:absolute; top:8px; right:14px; font-family:'Archivo',sans-serif;
  font-size:10px; letter-spacing:.08em; text-transform:uppercase; color:#8b9199;}
.tk{color:#e6e6e6}.tk-k{color:#7fb4ea}.tk-s{color:#a8d18d}.tk-c{color:#7e8792;font-style:italic}.tk-n{color:#e0ac4c}.tk-b{color:#e39fd6;font-weight:700}
.tbl{overflow-x:auto; margin:16px 0}
table{width:100%; border-collapse:collapse; font-family:'Archivo',sans-serif; font-size:14.3px}
table th{text-align:left; background:var(--raised); padding:9px 12px; border-bottom:2px solid var(--border); font-weight:700}
table td{padding:9px 12px; border-bottom:1px solid var(--border); vertical-align:top}
table td.num, table th.num{text-align:right}
ol.step{list-style:none; margin:16px 0; padding:0; counter-reset:stp}
ol.step li{counter-increment:stp; position:relative; padding:4px 0 14px 40px; border-left:2px solid var(--border); margin-left:14px}
ol.step li:last-child{border-color:transparent; padding-bottom:0}
ol.step li::before{content:counter(stp); position:absolute; left:-14px; top:0; width:28px; height:28px; border-radius:50%;
  background:var(--accent); color:#fff; font-family:'Archivo',sans-serif; font-weight:700; font-size:13px; display:flex; align-items:center; justify-content:center}
ol.step .stitle{font-family:'Archivo',sans-serif; font-weight:700; font-size:15.5px; margin-bottom:2px}
ol.step .snote{color:var(--ink-faint); font-size:13.6px; margin-top:4px}
.btnref{display:inline-block; font-family:'JetBrains Mono',monospace; font-size:12.8px; background:var(--raised);
  border:1px solid var(--border); border-radius:6px; padding:1.5px 7px; color:var(--ink)}
.q{border:1px solid var(--border); border-radius:12px; padding:14px 18px; margin:12px 0; background:var(--raised)}
.q .stem{font-family:'Archivo',sans-serif; font-weight:700; margin-bottom:8px}
.q details summary{cursor:pointer; color:var(--accent); font-family:'Archivo',sans-serif; font-size:13.8px; font-weight:600}
.q details[open] summary{margin-bottom:6px}
.aplicab{display:grid; grid-template-columns:1fr; gap:12px; margin:16px 0}
@media(min-width:760px){.aplicab{grid-template-columns:1fr 1fr 1fr}}
.aplicab > div{border:1px solid var(--border); border-radius:12px; padding:14px 16px; background:var(--raised)}
.aplicab .lbl{font-family:'Archivo',sans-serif; font-weight:700; font-size:12px; text-transform:uppercase; letter-spacing:.06em; margin-bottom:6px; color:var(--accent)}
.grid2{display:grid; grid-template-columns:1fr; gap:14px; margin:16px 0}
@media(min-width:760px){.grid2{grid-template-columns:1fr 1fr}}
.card{border:1px solid var(--border); border-radius:12px; padding:16px 18px; background:var(--raised)}
.card h4{margin:0 0 8px; font-size:15.5px}
.uimock{border:1px solid var(--border); border-radius:12px; overflow:hidden; margin:16px 0; background:var(--surface)}
.uimock .bar{background:var(--raised); padding:8px 14px; display:flex; gap:7px; align-items:center; border-bottom:1px solid var(--border)}
.uimock .dot{width:9px;height:9px;border-radius:50%; background:var(--ink-faint); opacity:.5}
.uimock .barlabel{font-family:'Archivo',sans-serif; font-size:12px; color:var(--ink-faint); margin-left:6px}
.uimock .body{display:grid; grid-template-columns:44px 200px 1fr; min-height:230px}
@media(max-width:700px){.uimock .body{grid-template-columns:34px 1fr; }  .uimock .body .panel-side{display:none}}
.uimock .rail{background:var(--raised); border-right:1px solid var(--border); display:flex; flex-direction:column; align-items:center; padding:10px 0; gap:16px}
.uimock .rail .ico{width:22px;height:22px;border-radius:6px; background:var(--border)}
.uimock .rail .ico.on{background:var(--accent)}
.uimock .panel-side{background:var(--surface); border-right:1px solid var(--border); padding:12px}
.uimock .panel-side .ttl{font-family:'Archivo',sans-serif; font-weight:700; font-size:12.5px; margin-bottom:8px; color:var(--ink-faint); text-transform:uppercase; letter-spacing:.05em}
.uimock .fileline{font-family:'JetBrains Mono',monospace; font-size:12.6px; padding:3px 6px; border-radius:5px; color:var(--ink-soft)}
.uimock .fileline.mod{color:var(--ambar)}
.uimock .fileline.new{color:var(--verde)}
.uimock .canvas{padding:16px}
.actbar{display:flex; flex-wrap:wrap; gap:0; border:1px solid var(--border); border-radius:12px; overflow:hidden; margin:16px 0; background:var(--surface)}
.actbar .rail2{background:var(--code-bg); padding:18px 22px 18px 14px; display:flex; flex-direction:column; gap:13px; align-items:flex-start}
.actbar .rail2 .aicon{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;background:rgba(255,255,255,.07); position:relative; color:#e6e6e6}
.actbar .rail2 .aicon.on{background:var(--accent)}
.actbar .rail2 .aicon .num{position:absolute; left:-18px; top:50%; transform:translateY(-50%); font-family:'JetBrains Mono',monospace; font-size:10.5px; color:#9aa0a6}
.actbar .legend{flex:1 1 280px; padding:14px 18px; font-family:'Archivo',sans-serif; font-size:13.2px; min-width:240px}
.actbar .legend .li{display:flex; gap:10px; padding:6px 0; border-bottom:1px dashed var(--border)}
.actbar .legend .li:last-child{border:none}
.actbar .legend .li .n{min-width:20px; font-family:'JetBrains Mono',monospace; color:var(--accent); font-weight:700}
.actbar .legend .li b{display:block}
.actbar .legend .li span.d{color:var(--ink-soft); font-size:12.6px}
.welcomemock{padding:30px 20px; text-align:center}
.welcomemock .wlogo{font-size:30px; margin-bottom:6px}
.welcomemock .wtitle{font-family:'Archivo',sans-serif; font-weight:700; font-size:17px; margin-bottom:20px}
.welcomemock .wbtns{display:flex; flex-direction:column; gap:10px; max-width:260px; margin:0 auto}
.welcomemock .wbtn{padding:10px 16px; border-radius:8px; border:1px solid var(--border); font-family:'Archivo',sans-serif; font-size:13.6px; font-weight:600; text-align:left}
.welcomemock .wbtn.primary{background:var(--accent); color:#fff; border-color:var(--accent)}
.welcomemock .wspaces{text-align:left; max-width:300px; margin:26px auto 0}
.welcomemock .wlbl{font-family:'Archivo',sans-serif; font-size:10.8px; color:var(--ink-faint); text-transform:uppercase; letter-spacing:.07em; margin-bottom:8px}
.welcomemock .wsitem{font-family:'Archivo',sans-serif; font-size:13px; padding:6px 10px; border-radius:7px; color:var(--ink-soft); border:1px solid var(--border); margin-bottom:6px}
.welcomemock .wsitem small{display:block; font-size:11px; color:var(--ink-faint)}
.agentmock{display:flex; flex-direction:column; min-height:270px}
.agentmock .ahead{padding:10px 16px; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; font-family:'Archivo',sans-serif; font-weight:700; font-size:13.5px}
.agentmock .ahead .aicons{font-weight:400; color:var(--ink-faint); font-size:15px; letter-spacing:6px}
.agentmock .abody{flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:6px}
.agentmock .abody .alogo{font-size:26px}
.agentmock .abody .aname{font-family:'Archivo',sans-serif; font-weight:700; color:var(--ink-soft)}
.agentmock .ainput{margin:14px; border:1px solid var(--border); border-radius:12px; padding:12px 14px; font-family:'Archivo',sans-serif}
.agentmock .ainput .ph{color:var(--ink-faint); font-size:13px; margin-bottom:10px}
.agentmock .ainput .arow{display:flex; justify-content:space-between; align-items:center; font-size:11.8px; color:var(--ink-faint)}
.agentmock .adisc{text-align:center; font-family:'Archivo',sans-serif; font-size:10.6px; color:var(--ink-faint); padding:0 16px 12px}
.flow{display:flex; flex-wrap:wrap; align-items:stretch; gap:0; margin:18px 0}
.flow .fnode{flex:1 1 140px; text-align:center; padding:16px 10px; position:relative}
.flow .fnode .circ{width:64px;height:64px;border-radius:50%;border:2.5px solid var(--accent); margin:0 auto 10px;
  display:flex; align-items:center; justify-content:center; background:var(--surface); font-size:22px}
.flow .fnode .lbl{font-family:'Archivo',sans-serif; font-weight:600; font-size:13.4px}
.flow .fnode:not(:last-child)::after{content:"→"; position:absolute; right:-6px; top:26px; color:var(--accent); font-size:20px; font-weight:700}
.kpi{display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:14px; margin:16px 0}
.kpi .k{border:1px solid var(--border); border-radius:12px; padding:16px; text-align:center; background:var(--raised)}
.kpi .k .val{font-family:'Archivo',sans-serif; font-weight:800; font-size:28px; color:var(--accent)}
.kpi .k .lbl{font-size:12.6px; color:var(--ink-faint); font-family:'Archivo',sans-serif; margin-top:4px}
.glossary dt{font-family:'Archivo',sans-serif; font-weight:700; margin-top:10px}
.glossary dd{margin:2px 0 0; color:var(--ink-soft)}
.themebtn,.pdfbtn{position:fixed; right:20px; z-index:50; font-family:'Archivo',sans-serif; font-size:12.8px; font-weight:600;
  border:1px solid var(--border); background:var(--surface); color:var(--ink); border-radius:24px; padding:9px 16px; cursor:pointer; box-shadow:var(--shadow)}
.themebtn{bottom:20px}
.pdfbtn{bottom:66px}
footer.pagefoot{max-width:1160px;margin:0 auto;padding:0 24px 60px;color:var(--ink-faint);font-family:'Archivo',sans-serif;font-size:12.5px;text-align:center}
"""

CSS_EXTRA = r"""
/* coluna do grid não estica com blocos de código longos (sem rolagem lateral no celular) */
.wrap.shell{grid-template-columns:minmax(0,1fr)}
@media(min-width:1000px){ .wrap.shell{grid-template-columns:250px minmax(0,1fr)} }
main{min-width:0}
/* celular: índice no topo, sem ficar grudado sobre o conteúdo */
@media(max-width:999px){ nav.toc{position:static; max-height:none} }
@media screen and (max-width:600px){ .flow{flex-direction:column; align-items:center}
  .flow .fnode{flex:none; width:100%; padding:8px 10px 18px}
  .flow .fnode:not(:last-child)::after{content:"↓"; right:auto; left:50%; transform:translateX(-50%); top:auto; bottom:-6px} }
.grid2 > *, .legenda > *, .antesdepois > *, .aplicab > *, .kpi > *{min-width:0}
code{overflow-wrap:anywhere; font-size:.9em; background:var(--raised); border:1px solid var(--border); border-radius:5px; padding:0 4px}
ul.f code, table code{background:none; border:none; padding:0}
ul.f{padding-top:30px}
ul.f.pr li{white-space:pre-wrap}
ul.f .ph{background:rgba(224,172,76,.22); color:#f2c46d; border-radius:4px; padding:0 3px}
ul.f .cpy{position:absolute; top:6px; left:14px; font-family:'Archivo',sans-serif; font-size:10.5px; font-weight:700;
  letter-spacing:.06em; text-transform:uppercase; background:rgba(255,255,255,.08); color:#c9cdd2; border:1px solid rgba(255,255,255,.14);
  border-radius:6px; padding:2px 9px; cursor:pointer}
ul.f .cpy:hover{background:rgba(255,255,255,.16)}
.phead{display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:18px 0 -8px; font-family:'Archivo',sans-serif; font-size:13.8px; font-weight:700}
.phead .onde{font-weight:600; font-size:11px; color:var(--ink-faint); text-transform:uppercase; letter-spacing:.05em;
  border:1px solid var(--border); border-radius:20px; padding:1px 9px; background:var(--raised)}
.parte{border-radius:14px; padding:18px 22px; margin:-6px 0 22px; background:var(--accent); color:#fff}
.parte .pk{font-family:'Archivo',sans-serif; font-size:11.5px; font-weight:700; letter-spacing:.12em; text-transform:uppercase; opacity:.85}
.parte .pt{font-family:'Archivo',sans-serif; font-size:23px; font-weight:800; margin:2px 0 6px; line-height:1.2}
.parte .pd{font-size:15px; opacity:.95; margin:0}
.parte ol{margin:10px 0 0; padding-left:20px; font-family:'Archivo',sans-serif; font-size:13.4px; opacity:.95}
.parte ol li{margin:1px 0}
.antesdepois{display:grid; grid-template-columns:1fr; gap:12px; margin:14px 0}
@media(min-width:760px){.antesdepois{grid-template-columns:1fr 1fr}}
.antesdepois > div{border-radius:12px; padding:12px 14px; border:1px solid var(--border)}
.antesdepois .ruim{background:var(--vermelho-soft); border-color:var(--vermelho)}
.antesdepois .bom{background:var(--verde-soft); border-color:var(--verde)}
.antesdepois .lbl{font-family:'Archivo',sans-serif; font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; margin-bottom:6px}
.antesdepois .ruim .lbl{color:var(--vermelho)} .antesdepois .bom .lbl{color:var(--verde)}
.antesdepois p{margin:0; font-size:14.6px}
.sprint{display:grid; grid-template-columns:46px 1fr; gap:14px; border:1px solid var(--border); border-radius:12px;
  padding:14px 16px; margin:12px 0; background:var(--raised)}
.sprint .n{width:38px; height:38px; border-radius:10px; background:var(--verde); color:#fff;
  display:flex; align-items:center; justify-content:center; font-family:'Archivo',sans-serif; font-weight:800; font-size:18px}
.sprint h4{margin:0 0 4px; font-family:'Archivo',sans-serif; font-size:15.5px}
.sprint .meta{font-size:12.5px; color:var(--ink-faint); font-family:'Archivo',sans-serif; margin-bottom:6px}
.sprint ul{margin:6px 0 0 0; padding-left:20px; font-size:14.6px}
.check{list-style:none; padding-left:0 !important}
.check li{padding-left:28px; position:relative}
.check li::before{content:"☐"; position:absolute; left:4px; top:-1px; color:var(--accent); font-size:17px}
.legenda{display:grid; grid-template-columns:1fr; gap:10px; margin:14px 0}
@media(min-width:760px){.legenda{grid-template-columns:1fr 1fr}}
.legenda > div{display:flex; gap:12px; align-items:flex-start; border:1px solid var(--border); border-radius:12px; padding:12px 14px; background:var(--raised)}
.legenda .ic{font-size:22px; line-height:1}
.legenda > div > div > b{font-family:'Archivo',sans-serif; display:block; font-size:14.5px}
.legenda span.d{font-size:14px; color:var(--ink-soft)}
.q .resp-lbl{font-family:'Archivo',sans-serif; font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:var(--verde); margin-right:6px}
.sumario{display:none}

@media print{
  @page { size: A4; margin: 14mm 13mm 16mm 13mm; }
  :root, :root[data-theme="dark"], :root:not([data-theme="light"]){
    --paper:#ffffff !important; --surface:#ffffff !important; --raised:#f4f2ed !important;
    --ink:#1a1d1e !important; --ink-soft:#4a4f52 !important; --ink-faint:#7a8084 !important;
    --accent:#1f4b8f !important; --accent-soft:#e8eefa !important;
    --verde:#1c8a5b !important; --verde-soft:#e4f5ec !important;
    --ambar:#b4790a !important; --ambar-soft:#fbeed9 !important;
    --vermelho:#c33b3b !important; --vermelho-soft:#fbe7e7 !important;
    --roxo:#6b3fa0 !important; --roxo-soft:#efe6f8 !important;
    --border:#e3e0d8 !important; --code-bg:#1e2124 !important; --code-ink:#e6e6e6 !important;
    --shadow:none !important; color-scheme:light;
  }
  html{ -webkit-print-color-adjust:exact; print-color-adjust:exact }
  html, body{ margin:0; padding:0; background:#fff; font-size:13.5px; line-height:1.5 }
  .themebtn,.pdfbtn,nav.toc,button,.cpy{ display:none !important }

  /* capa */
  header.top{ padding:70mm 0 12mm !important; background:none !important; border-bottom:3px solid var(--accent) !important }
  header.top .inner{ max-width:100% !important; padding:0 !important }
  header.top h1{ font-size:34px !important; margin:14px 0 10px !important }
  header.top p.sub{ font-size:16px !important; max-width:none !important }

  /* sumário */
  .sumario{ display:block; break-before:page; page-break-before:always; break-after:page; page-break-after:always; font-family:'Archivo',sans-serif }
  .sumario h2{ font-size:19px; margin:0 0 2mm; padding-bottom:2mm; border-bottom:2px solid var(--accent) }
  .sumario .sg{ font-weight:800; font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--accent); margin:3mm 0 .5mm }
  .sumario .si{ display:flex; align-items:baseline; gap:6px; font-size:11.8px; line-height:1.35; padding:.35mm 0; color:var(--ink) }
  .sumario .si .n{ min-width:20px; color:var(--ink-faint) }
  .sumario .si .dots{ flex:1; border-bottom:1px dotted #b9b6ae; transform:translateY(-3px) }
  .sumario .si .pg{ min-width:18px; text-align:right; font-weight:700 }

  .wrap.shell{ display:block !important; max-width:100% !important; margin:0 !important; padding:0 !important }
  main{ overflow:visible !important }

  /* seções correm uma após a outra (sem páginas em branco); cada PARTE abre página nova */
  main section{
    background:#fff !important; box-shadow:none !important; border:none !important; border-radius:0 !important;
    padding:0 !important; margin:0 0 8mm !important; break-before:auto; page-break-before:auto;
  }
  main section:not(.inicio-parte){ border-top:1px solid var(--border) !important; padding-top:5mm !important }
  main section.inicio-parte{ break-before:page; page-break-before:always }
  .parte{ margin:0 0 6mm !important; padding:6mm 7mm !important; break-inside:avoid }
  .parte .pt{ font-size:22px !important }
  main section h2{ font-size:18.5px !important; margin:1mm 0 4mm !important }
  main section h3{ font-size:14.8px !important; margin:10px 0 5px !important }
  main section p{ margin:0 0 9px }

  h1, h2, h3, h4, .secnum, .phead, ol.step .stitle{ break-after:avoid; page-break-after:avoid; break-inside:avoid }
  h2 + *, h3 + *, h4 + *, .phead + *, .shead + *{ break-before:avoid; page-break-before:avoid }
  .shead{ break-inside:avoid; page-break-inside:avoid; break-after:avoid; page-break-after:avoid }
  .parte{ break-after:avoid; page-break-after:avoid }
  .ficha, .callout, .q, ul.f, .sprint, .card, .aplicab > div, .kpi, .kpi .k, .flow, ol.step li,
  tr, dt, dd, .antesdepois > div, .legenda > div, .uimock, img, svg{ break-inside:avoid; page-break-inside:avoid }
  dt{ break-after:avoid }
  thead{ display:table-header-group }
  p, li{ orphans:3; widows:3 }
  .tbl{ overflow:visible !important }

  /* código: quebra linha em vez de cortar na margem */
  ul.f{ overflow:visible !important; font-size:10.4px !important; padding:22px 10px 8px !important; margin:10px 0 !important; line-height:1.45 }
  ul.f li{ white-space:pre-wrap !important; overflow-wrap:anywhere }
  ul.f::before{ top:6px !important }
  ul.f.longo{ break-inside:auto; page-break-inside:auto }
  .phead{ margin:12px 0 -6px !important }

  table{ font-size:11.3px !important } table th, table td{ padding:5px 8px !important }
  .ficha, .callout{ padding:8px 11px !important; margin:8px 0 !important; font-size:12.8px !important }
  .card{ padding:10px 12px !important; font-size:12.8px }
  .aplicab, .grid2, .legenda{ gap:8px !important; margin:10px 0 !important }
  .aplicab{ grid-template-columns:1fr 1fr 1fr !important }
  .grid2, .legenda, .antesdepois{ grid-template-columns:1fr 1fr !important }
  .aplicab > div{ padding:8px 10px !important; font-size:12.4px }
  .kpi{ grid-template-columns:repeat(4,1fr) !important; gap:8px !important }
  .kpi .k{ padding:8px !important } .kpi .k .val{ font-size:22px !important }

  /* fluxos: todos os passos numa linha só */
  .flow{ flex-wrap:nowrap !important; margin:10px 0 !important }
  .flow .fnode{ flex:1 1 0 !important; padding:6px 3px !important; min-width:0 }
  .flow .fnode .circ{ width:44px !important; height:44px !important; font-size:18px !important; margin-bottom:6px !important }
  .flow .fnode .lbl{ font-size:10.6px !important; line-height:1.25 }
  .flow .fnode:not(:last-child)::after{ right:-7px !important; top:15px !important; font-size:15px !important }

  ol.step li{ padding-bottom:9px !important }
  /* quiz: respostas visíveis no PDF */
  .q details summary{ display:none }
  footer.pagefoot{ padding:4mm 0 0 !important; break-before:avoid }
}
"""

CSS = CSS_BASE + CSS_EXTRA

# =================================================================
# HELPERS
# =================================================================
def p(txt):
    return f"<p>{txt}</p>"

def h3(txt):
    return f"<h3>{txt}</h3>"

def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def checklist(items):
    return "<ul class='check'>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def ficha(kind, label, body):
    return f'<div class="ficha {kind}"><b class="lbl">{label}</b>{body}</div>'

def callout(kind, label, body):
    return f'<div class="callout {kind}"><b class="lbl">{label}</b>{body}</div>'

def tbl(headers, rows):
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'

def _lines(text):
    lns = text.strip("\n").split("\n")
    ind = min((len(l) - len(l.lstrip(" ")) for l in lns if l.strip()), default=0)
    return [l[ind:].rstrip() for l in lns]

def code(text, lang="bash"):
    """Bloco de código. O texto é escapado (pode conter <, >, &, chaves)."""
    linhas = _lines(text)
    lis = "".join(f"<li>{html.escape(l) if l else ' '}</li>" for l in linhas)
    longo = " longo" if len(linhas) > 45 else ""
    return f'<ul class="f{longo}" data-lang="{lang}">{lis}</ul>'

PH = re.compile(r"(\[[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9][^\]\n]{1,70}\])")

def prompt(text, titulo="", onde="Painel Agent do Antigravity"):
    """Prompt pronto para copiar. [CAMPOS] em destaque amarelo; linha longa quebra."""
    lis = ""
    for l in _lines(text):
        esc = html.escape(l) if l else " "
        lis += "<li>" + PH.sub(r'<span class="ph">\1</span>', esc) + "</li>"
    head = f'<div class="phead">💬 {titulo}<span class="onde">{onde}</span></div>' if titulo else ""
    return head + f'<ul class="f pr" data-lang="prompt">{lis}</ul>'

def step(items):
    out = "<ol class='step'>"
    for it in items:
        out += f"<li><div class='stitle'>{it[0]}</div><div>{it[1]}</div>"
        if len(it) > 2 and it[2]:
            out += f"<div class='snote'>{it[2]}</div>"
        out += "</li>"
    return out + "</ol>"

def q(stem, options, ans_idx, hint=""):
    opts = "".join(f"<li>{o}</li>" for o in options)
    letra = "abcd"[ans_idx]
    hint_html = f" {hint}" if hint else ""
    return (f'<div class="q"><div class="stem">{stem}</div><ol type="a">{opts}</ol>'
            f'<details><summary>Ver resposta</summary><p><span class="resp-lbl">Resposta</span>'
            f'<b>({letra}) {options[ans_idx]}.</b>{hint_html}</p></details></div>')

def aplicab(quando, porque, exemplo):
    return (f'<div class="aplicab"><div><div class="lbl">Quando</div>{quando}</div>'
            f'<div><div class="lbl">Por que</div>{porque}</div>'
            f'<div><div class="lbl">Exemplo no MVP</div>{exemplo}</div></div>')

def grid2(cards):
    return '<div class="grid2">' + "".join(f'<div class="card"><h4>{t}</h4>{b}</div>' for t, b in cards) + '</div>'

def flow_h(nodes):
    return '<div class="flow">' + "".join(
        f'<div class="fnode"><div class="circ">{e}</div><div class="lbl">{l}</div></div>' for e, l in nodes) + '</div>'

def kpi(items):
    return '<div class="kpi">' + "".join(
        f'<div class="k"><div class="val">{v}</div><div class="lbl">{l}</div></div>' for v, l in items) + '</div>'

def sprint(n, titulo, meta, itens):
    return (f'<div class="sprint"><div class="n">{n}</div><div><h4>{titulo}</h4>'
            f'<div class="meta">{meta}</div>{ul(itens)}</div></div>')

def antesdepois(ruim, bom):
    return (f'<div class="antesdepois"><div class="ruim"><div class="lbl">✗ Prompt vago</div><p>{ruim}</p></div>'
            f'<div class="bom"><div class="lbl">✓ Prompt técnico</div><p>{bom}</p></div></div>')

def legenda(items):
    return '<div class="legenda">' + "".join(
        f'<div><span class="ic">{i}</span><div><b>{t}</b><span class="d">{d}</span></div></div>' for i, t, d in items) + '</div>'

def glossary(items):
    return "<dl class='glossary'>" + "".join(f"<dt>{t}</dt><dd>{d}</dd>" for t, d in items) + "</dl>"

# =================================================================
# ESTADO / TOC
# =================================================================
sections = []          # (anchor, titulo, body, grupo_idx)
grupos = []            # (titulo, descricao)

def grp(titulo, descricao=""):
    grupos.append((titulo, descricao))

def section(anchor, titulo, body_html):
    sections.append((anchor, titulo, body_html, len(grupos) - 1))

REPO = "mvp-pedidos-compra"

# =================================================================
# ABERTURA
# =================================================================
grp("Abertura", "O que vamos construir hoje, como usar este caderno e a conferência dos arquivos que vieram do NotebookLM.")

section("agenda", "Onde estamos e o que vamos construir hoje",
    p("Na Aula 7 vocês planejaram o projeto: definiram a dor, os usuários, os dados, o BPMN, a arquitetura, "
      "o uso da IA e as sprints. Depois levaram tudo do <b>NotebookLM</b> para o <b>Antigravity</b> em dois arquivos: "
      "o <code>contexto.md</code> (o resumo do projeto) e o <code>sprint.md</code> (as sprints técnicas). "
      "Hoje esses dois arquivos viram <b>software de verdade</b>: um MVP instalável no celular, versionado no GitHub "
      "e publicado na internet pelo GitHub Pages.") +
    flow_h([("🧠", "NotebookLM<br>(ideação)"), ("📄", "contexto.md<br>+ sprint.md"), ("🤖", "Agente do<br>Antigravity"),
            ("💾", "Commit e push<br>no GitHub"), ("⚙️", "GitHub Actions<br>(build)"), ("🌐", "GitHub Pages<br>(PWA no ar)")]) +
    kpi([("5", "sprints para entregar o MVP"), ("3", "linguagens: TS, JS e Python"), ("1", "link público no GitHub Pages"),
         ("50+", "prompts prontos neste caderno")]) +
    h3("O que vocês levam do Dia 8") +
    ul(["Um repositório no GitHub com o código do MVP, histórico de commits e README;",
        "o MVP publicado em <code>https://SEU-USUARIO.github.io/NOME-DO-REPO/</code>, instalável como aplicativo (PWA);",
        "deploy automático: cada <code>push</code> na branch <code>main</code> atualiza o site sozinho;",
        "uma biblioteca de prompts para continuar desenvolvendo nas próximas aulas."]) +
    ficha("", "Exemplo usado neste caderno",
      "Para os exemplos ficarem concretos, usamos o <b>Portal de Pedidos de Compra</b>, o To-Be do exemplo da Aula 7 "
      "(Solicitante abre o pedido → Sistema valida → Cotação → Controladoria audita → Secretário aprova no painel). "
      f"O repositório de exemplo se chama <code>{REPO}</code>. Troquem sempre pelo projeto de vocês.")
)

section("como-usar", "Como usar este caderno",
    p("O caderno é um <b>roteiro para seguir em ordem</b>: cada Parte termina com algo funcionando e um commit no GitHub. "
      "Estes são os elementos que se repetem:") +
    legenda([
        ("💬", "Bloco de prompt", "Texto para copiar e colar no <b>painel Agent</b> do Antigravity (ou no chat do NotebookLM, quando indicado). No HTML há um botão <b>Copiar</b> em cada bloco."),
        ("🟨", "[CAMPOS EM AMARELO]", "Dentro dos prompts, o que está entre colchetes é para <b>substituir</b> pelos dados do projeto de vocês antes de enviar."),
        ("⌨️", "Bloco de terminal", "Comandos para digitar no terminal do Antigravity (<b>Terminal → New Terminal</b>). Uma linha por vez; o que vem depois de <code>#</code> é comentário."),
        ("📄", "Bloco de arquivo", "Conteúdo de um arquivo do projeto (o nome aparece no canto do bloco). Serve de gabarito para conferir o que o agente gerou."),
        ("🔴", "Caixa vermelha", "Armadilha ou regra que não pode ser quebrada (LGPD, comandos que apagam arquivos, chaves secretas)."),
        ("🟢", "Caixa verde", "Dica, boa prática ou a mensagem de commit sugerida para aquela etapa."),
    ]) +
    tbl(["Parte", "O que vocês fazem", "Termina com"],
        [["1 · O que dá para publicar", "Entender o que \"full stack\" vira num site estático", "A arquitetura e a estrutura de pastas definidas"],
         ["2 · Trabalhando com o agente", "Aprender o formato de prompt e o ciclo de cada tarefa", "Regras de segurança combinadas no grupo"],
         ["3 · Sprint 0", "Instalar, criar o projeto e publicar o repositório", "Repositório no GitHub + agente conhecendo o projeto"],
         ["4 · Sprints 1 a 5", "Dados, regras, telas, PWA, testes e deploy", "MVP no ar em <code>github.io</code>"],
         ["5 · Biblioteca de prompts", "Consultar quando precisar", "—"],
         ["Fechamento", "Resolver problemas e conferir a entrega", "Checklist completo"]])
)

section("conferir-arquivos", "Antes de começar: vocês rodaram estes dois prompts no NotebookLM?",
    p("Tudo o que vem depois depende da qualidade do <code>contexto.md</code> e do <code>sprint.md</code>. "
      "O agente do Antigravity <b>não conhece o projeto de vocês</b>: ele só sabe o que está escrito nesses arquivos. "
      "Confirmem primeiro que os dois existem e foram gerados com estes prompts:") +
    tbl(["Arquivo", "Prompt usado no NotebookLM", "Para que serve no Antigravity"],
        [["<code>contexto.md</code>", "<i>\"Anote todo o contexto fornecido até aqui para a ideação e prototipagem do projeto\"</i>",
          "A \"memória\" do projeto: problema, usuários, dados, regras. O agente consulta antes de cada tarefa."],
         ["<code>sprint.md</code>", "<i>\"Gere sprints de execução do projeto de forma técnica em (JS, TS, Python em PWA)\"</i>",
          "O roteiro de construção: o que fazer em cada sprint. O agente executa uma tarefa por vez."]]) +
    h3("Teste rápido: os arquivos de vocês estão bons o suficiente?") +
    p("Abram os dois arquivos no Antigravity e marquem o que eles contêm:") +
    checklist(["<b>contexto.md</b> descreve a dor com número (ex.: \"10 dias para consolidar\")",
               "<b>contexto.md</b> lista os papéis de usuário (Admin, Editor, Leitor, Aprovador) e o que cada um faz",
               "<b>contexto.md</b> lista as entidades de dados com seus campos (ex.: Pedido: protocolo, unidade, valor…)",
               "<b>contexto.md</b> diz quais campos são sensíveis (LGPD) e como mascarar",
               "<b>contexto.md</b> descreve o fluxo To-Be passo a passo",
               "<b>sprint.md</b> tem sprints numeradas, cada uma com tarefas e um critério de \"pronto\"",
               "<b>sprint.md</b> diz em qual linguagem fica cada parte (TS, JS, Python)",
               "<b>sprint.md</b> considera que o site será <b>estático</b>, no GitHub Pages"]) +
    callout("tip", "Resultado do teste",
      "<b>7 ou 8 marcados:</b> sigam em frente. <b>4 a 6:</b> usem os prompts melhorados da próxima seção para "
      "complementar. <b>3 ou menos:</b> gerem os arquivos de novo com os prompts melhorados antes de escrever código. "
      "Os 20 minutos que isso leva economizam horas de retrabalho com o agente.")
)

section("prompts-notebooklm", "Os prompts do NotebookLM, versão técnica",
    p("Os prompts originais funcionam, mas deixam o NotebookLM decidir sozinho o formato e o nível de detalhe. "
      "As versões abaixo pedem uma <b>estrutura fixa</b>, com as informações que o agente de código mais usa. "
      "Rodem no <b>mesmo notebook</b> do grupo, onde estão as fontes da Aula 7, e salvem a resposta como arquivo <code>.md</code>.") +
    prompt("""
        Atue como analista de requisitos de software do setor público. Com base em TODAS as fontes e conversas deste notebook,
        escreva o documento "contexto.md" do projeto [NOME DO SISTEMA] em Markdown, com EXATAMENTE estas seções:

        1. Visão geral: o problema (dor) em 1 frase com número, o setor da SESP-MT e a solução proposta.
        2. Objetivos e KPIs: 2 a 4 KPIs, cada um com baseline (hoje), meta e como medir.
        3. Usuários e papéis: tabela Papel | Quem é na SESP | O que pode fazer | O que NÃO pode fazer (papéis A, E, L, X).
        4. Fluxo To-Be: passos numerados, indicando qual papel executa cada passo e o que o sistema faz sozinho.
        5. Entidades de dados: para cada entidade, tabela Campo | Tipo (texto, número, data, lista) | Obrigatório | Exemplo.
        6. Regras de negócio: lista numerada RN01, RN02... (ex.: "RN03 - pedido acima de R$ 50 mil exige auditoria").
        7. Dados sensíveis (LGPD): quais campos, classificação (pessoal/sensível) e técnica de proteção (máscara, hash, omitir).
        8. Telas do MVP: nome da tela, objetivo, papel que usa, elementos principais (KPIs, gráfico, tabela, formulário).
        9. Restrições técnicas: site estático no GitHub Pages, sem servidor e sem banco real, apenas dados sintéticos.
        10. Fora do escopo do MVP: o que fica para depois.
        11. Dúvidas em aberto: o que ainda não foi decidido pelo grupo.

        Não invente informação: se algo não estiver nas fontes, escreva "A DEFINIR" no lugar.
        """, "Prompt 1 melhorado — contexto.md", "Chat do NotebookLM") +
    prompt("""
        Atue como tech lead de um projeto de software. Com base no contexto do projeto [NOME DO SISTEMA] neste notebook,
        gere o documento "sprint.md" em Markdown com o plano técnico de construção do MVP.

        Stack obrigatória:
        - Front-end: TypeScript + Vite, como PWA (vite-plugin-pwa), com rotas por hash (#/tela).
        - JavaScript: apenas onde o Vite/PWA gerar (service worker, arquivos de configuração).
        - Python 3.12: scripts de geração de dados sintéticos (saída em public/data/*.json), mascaramento LGPD e testes (pytest).
        - Testes do front-end: Vitest.
        - Hospedagem: GitHub Pages (site estático), com deploy automático por GitHub Actions a cada push na main.
        - Sem servidor e sem banco de dados real: dados em JSON + armazenamento local no navegador (IndexedDB ou localStorage).

        Gere 5 sprints (1 Fundação e dados, 2 Regras de negócio e papéis, 3 Telas, 4 PWA e homologação, 5 Deploy e documentação).
        Para CADA sprint escreva:
        - Objetivo (1 frase) e entregável demonstrável.
        - Tarefas numeradas (S1.1, S1.2...), cada uma com: arquivos a criar ou alterar, linguagem, e critério de aceite testável.
        - Testes da sprint (o que o Vitest ou o pytest deve verificar).
        - Mensagem de commit sugerida no padrão Conventional Commits (feat:, fix:, test:, docs:, chore:).
        Termine com uma "Definição de Pronto" do MVP em checklist.
        """, "Prompt 2 melhorado — sprint.md", "Chat do NotebookLM") +
    callout("note", "Já têm um sprint.md que pede servidor e banco de dados?",
      "Muitos grupos receberam sprints com FastAPI/Flask, PostgreSQL ou login com senha. Não joguem fora: "
      "a próxima Parte mostra como isso vira um site estático, e no Passo 4 da Sprint 0 há um prompt que pede "
      "ao agente para reescrever o sprint.md para o GitHub Pages sem perder o que foi planejado.") +
    callout("err", "LGPD vale aqui também",
      "O NotebookLM é um serviço externo. Se alguma fonte do notebook tiver nome, CPF ou matrícula reais, "
      "removam antes de gerar os arquivos. Os dois <code>.md</code> vão para um repositório <b>público</b> no GitHub.")
)

# =================================================================
# PARTE 1
# =================================================================
grp("Parte 1 · O que dá para publicar",
    "O GitHub Pages só entrega arquivos prontos. Aqui vocês veem como cada peça \"full stack\" do sprint.md vira um site estático, "
    "qual o papel de cada linguagem e como organizar as pastas.")

section("pages-estatico", "A verdade sobre \"full stack\" no GitHub Pages",
    p("O GitHub Pages é gratuito e simples, mas tem uma regra que muda tudo: <b>ele só entrega arquivos prontos</b> "
      "(HTML, CSS, JavaScript, imagens, JSON). Ele não executa Python, não tem banco de dados e não guarda nada "
      "que o usuário digita. Cada parte \"full stack\" do sprint.md precisa ter um equivalente estático:") +
    tbl(["O que o sprint.md pede", "Como fica no MVP do GitHub Pages", "Linguagem"],
        [["Backend / API (FastAPI, Flask, Node)", "Uma camada <code>src/services/</code> em TypeScript que lê JSON, com a mesma \"cara\" de uma API", "TS"],
         ["Banco de dados (PostgreSQL, MySQL)", "Arquivos <code>public/data/*.json</code> gerados por script Python, mais IndexedDB/localStorage para o que o usuário cadastra", "Python + TS"],
         ["Geração de dados, ETL, relatórios", "Scripts em <code>scripts/*.py</code>, executados no computador e no GitHub Actions antes do build", "Python"],
         ["Login e senha", "Seletor \"Ver como: Admin / Editor / Leitor / Aprovador\" (RBAC simulado, como combinado na Aula 7)", "TS"],
         ["Logs de auditoria", "Registro local (quem, papel, ação, antes/depois, data/hora) com exportação em CSV", "TS"],
         ["Mascaramento LGPD", "Feito no script Python <b>antes</b> de gerar o JSON: o dado completo nunca chega ao site", "Python"],
         ["App de celular", "PWA: instalável pelo navegador e funcionando offline", "TS + JS (service worker)"],
         ["Servidor de deploy", "GitHub Actions compila e publica sozinho a cada push", "YAML"]]) +
    callout("err", "Regra de ouro: tudo no GitHub Pages é público",
      "Qualquer pessoa pode abrir o código-fonte do site e baixar os JSON. Por isso: <b>nenhum dado real</b>, "
      "<b>nenhuma senha</b>, <b>nenhuma chave de API</b> (nem de IA) no repositório. Se o agente sugerir colocar "
      "uma chave no código, recusem.") +
    ficha("p", "E o código de backend que vocês planejaram?",
      "Ele pode continuar existindo como <b>evolução futura</b>. A camada <code>src/services/</code> é escrita contra uma "
      "interface (ex.: <code>listarPedidos()</code>). Hoje ela lê JSON; amanhã, quando a SESP hospedar uma API de verdade, "
      "troca-se só a implementação, e as telas não mudam. Isso se chama <b>padrão adaptador</b>.")
)

section("arquitetura", "A arquitetura do MVP: quem faz o quê",
    p("Cada linguagem tem um papel claro. Guardem este quadro: ele responde metade das dúvidas sobre onde colocar cada código.") +
    grid2([
        ("🐍 Python: a \"fábrica de dados\"",
         ul(["Gera dados sintéticos realistas (<code>scripts/gerar_dados.py</code>);",
             "mascara campos sensíveis (LGPD) antes de salvar;",
             "valida os dados com testes (<code>pytest</code>);",
             "roda <b>antes</b> do build, nunca no navegador."])),
        ("🔷 TypeScript: o aplicativo",
         ul(["Tipos das entidades (<code>src/domain/tipos.ts</code>);",
             "regras de negócio RN01, RN02… (<code>src/domain/regras.ts</code>);",
             "papéis e permissões, auditoria, telas;",
             "testado com <code>Vitest</code>."])),
        ("🟨 JavaScript: a cola do PWA",
         ul(["Service worker (gerado pelo <code>vite-plugin-pwa</code>);",
             "arquivos de build em <code>dist/</code>;",
             "o TypeScript vira JavaScript no build: o navegador só executa JS."])),
        ("⚙️ GitHub: versão e publicação",
         ul(["Repositório: histórico de tudo (commits);",
             "Actions: roda Python, testes e build a cada push;",
             "Pages: entrega o site em <code>https://usuario.github.io/repo/</code>."])),
    ]) +
    flow_h([("🐍", "gerar_dados.py<br>→ public/data"), ("🔷", "TypeScript<br>lê os JSON"), ("🧪", "Vitest + pytest<br>testam"),
            ("📦", "vite build<br>→ dist/"), ("🌐", "GitHub Pages<br>publica dist/")])
)

section("estrutura-pastas", "A estrutura de pastas do repositório",
    p("Peçam ao agente para seguir esta estrutura desde o primeiro dia. Com ela, qualquer colega (e o próprio agente) "
      "sabe onde procurar cada coisa.") +
    code(f"""
        {REPO}/
        ├── docs/
        │   ├── contexto.md            ← vindo do NotebookLM
        │   ├── sprint.md              ← vindo do NotebookLM
        │   └── REGRAS-DO-PROJETO.md   ← regras que o agente segue sempre
        ├── scripts/                   ← PYTHON
        │   ├── gerar_dados.py         ← dados sintéticos → public/data/*.json
        │   └── test_gerar_dados.py    ← pytest: LGPD e consistência
        ├── public/
        │   ├── data/                  ← JSON gerados (não editar à mão)
        │   ├── icon.svg               ← ícone-fonte do PWA
        │   └── pwa-192x192.png ...    ← ícones gerados
        ├── src/                       ← TYPESCRIPT
        │   ├── domain/                ← tipos.ts, regras.ts (+ regras.test.ts)
        │   ├── auth/                  ← papeis.ts (RBAC simulado)
        │   ├── services/              ← api.ts, auditoria.ts, armazenamento.ts
        │   ├── pages/                 ← uma tela por arquivo (painel.ts, pedidos.ts...)
        │   ├── components/            ← pedaços reutilizáveis (kpiCard.ts...)
        │   ├── router.ts              ← rotas por hash: #/painel, #/pedidos
        │   ├── main.ts
        │   └── style.css
        ├── .github/workflows/deploy.yml   ← GitHub Actions → GitHub Pages
        ├── index.html
        ├── vite.config.ts             ← base: '/{REPO}/' + PWA
        ├── package.json               ← scripts: dev, build, test
        ├── requirements.txt           ← dependências Python
        ├── .gitignore                 ← node_modules, dist, .venv
        └── README.md
        """, "estrutura") +
    callout("note", "O que NUNCA vai para o GitHub",
      "<code>node_modules/</code> (centenas de MB, reinstalável com <code>npm ci</code>), <code>dist/</code> (gerado pelo build), "
      "<code>.venv/</code> (ambiente Python local) e qualquer arquivo com dado real. O <code>.gitignore</code> cuida disso: "
      "confiram que ele existe <b>antes</b> do primeiro commit.")
)

# =================================================================
# PARTE 2
# =================================================================
grp("Parte 2 · Trabalhando com o agente",
    "Como escrever um prompt que o agente acerta de primeira, o ciclo curto de cada tarefa e as regras de segurança do grupo.")

section("anatomia-prompt", "Anatomia de um bom prompt de desenvolvimento",
    p("Na Aula 8 vocês viram os 4 princípios de prompt (papel, contexto, formato, iteração). Para programar, "
      "acrescentem mais dois: <b>restrições</b> e <b>critério de pronto</b>. Todo prompt deste caderno segue esta receita:") +
    tbl(["Parte", "O que escrever", "Exemplo"],
        [["1. Contexto", "Citar os arquivos com <code>@</code> para o agente ler", "\"Leia @docs/contexto.md e @docs/sprint.md\""],
         ["2. Tarefa", "UMA tarefa, com o código da sprint", "\"Execute a tarefa S2.3 (cálculo do status do pedido)\""],
         ["3. Onde", "Arquivos a criar ou alterar", "\"Crie src/domain/regras.ts; não altere outros arquivos\""],
         ["4. Restrições", "Stack, estilo, o que é proibido", "\"TypeScript estrito, sem bibliotecas novas, sem dados reais\""],
         ["5. Pronto quando", "Como verificar que funcionou", "\"npm test passa e a tela #/painel mostra 4 KPIs\""],
         ["6. Formato da resposta", "O que o agente deve devolver", "\"Primeiro o plano; espere meu OK antes de codar\""]]) +
    prompt("""
        Contexto: leia @docs/contexto.md, @docs/sprint.md e @docs/REGRAS-DO-PROJETO.md.
        Tarefa: execute a tarefa [S?.?] do sprint.md: [DESCRIÇÃO CURTA].
        Onde: crie/altere somente [ARQUIVOS]. Não mexa em outros arquivos.
        Restrições: TypeScript estrito; sem bibliotecas novas sem me perguntar; somente dados sintéticos.
        Pronto quando: [CRITÉRIO VERIFICÁVEL, ex.: npm test passa e a tela X mostra Y].
        Resposta: primeiro me mostre o plano em tópicos e a lista de arquivos. Só escreva código depois do meu "OK".
        """, "Modelo universal (copie e preencha)") +
    ficha("a", "O @ é o superpoder",
      "Ao digitar <code>@</code> na caixa do painel Agent, o Antigravity lista os arquivos do projeto. Mencionar o "
      "arquivo garante que o agente leia a versão atual dele, em vez de adivinhar. Sempre mencionem o "
      "<code>contexto.md</code> quando a tarefa envolver regra de negócio ou dado.")
)

section("ciclo-tarefa", "O ciclo de cada tarefa: planejar → gerar → testar → commitar",
    p("O erro nº 1 com agentes de IA é pedir a sprint inteira de uma vez. O agente gera 30 arquivos, algo quebra, e "
      "ninguém sabe onde. Trabalhem em <b>ciclos curtos</b>: uma tarefa do sprint.md por ciclo, com um commit no final.") +
    flow_h([("📋", "1. Pedir<br>o plano"), ("✅", "2. Aprovar ou<br>corrigir"), ("🤖", "3. Agente<br>gera o código"),
            ("▶️", "4. Rodar<br>e testar"), ("🔍", "5. Revisar<br>o diff"), ("💾", "6. Commit<br>+ push")]) +
    step([
        ("Pedir o plano", "Use o modelo universal. Se o seu Antigravity mostrar os modos <b>Planning</b> e <b>Fast</b> no painel do agente, "
         "use <b>Planning</b> em tarefas novas: ele devolve um plano para você aprovar antes de mexer nos arquivos."),
        ("Aprovar ou corrigir", "Leiam o plano em grupo. Ele cita arquivos que não deveria? Inventou uma regra que não está no contexto.md? Corrijam antes."),
        ("Gerar", "O agente escreve o código. Quando ele pedir para rodar um comando no terminal, <b>leiam o comando antes de aprovar</b>."),
        ("Rodar e testar", "<code>npm run dev</code> para ver a tela, <code>npm test</code> para os testes. Se der erro, copiem o erro inteiro para o agente (ver prompts de depuração)."),
        ("Revisar o diff", "No painel Source Control (Aula 6), cliquem em cada arquivo alterado: verde = linha nova, vermelho = linha removida. Algo estranho? Perguntem ao agente \"por que você mudou isto?\"."),
        ("Commit + push", "Uma mensagem por tarefa: <code>feat(pedidos): calcula status do pedido (S2.3)</code>. Depois, <b>Sync/Push</b>."),
    ]) +
    callout("tip", "Regra dos 3 testes (Aula 7) antes do commit",
      "<b>R</b>oda? (sem erro no terminal e no console do navegador) · <b>C</b>olega entende? (alguém do grupo explica o que o "
      "código faz) · <b>T</b>este? (existe pelo menos um teste que prova que funciona). Faltou um: não commitem ainda.")
)

section("regras-agente", "Regras de segurança ao trabalhar com o agente",
    tbl(["Situação", "O que fazer"],
        [["O agente quer rodar <code>rm</code>, <code>del</code>, <code>git reset --hard</code>, <code>--force</code> ou <code>--overwrite</code>", "<b>Recusem</b> e perguntem por quê. Esses comandos apagam trabalho."],
         ["O agente alterou arquivos que não tinham nada a ver com a tarefa", "No Source Control, descartem as mudanças desses arquivos (<b>Discard Changes</b>) e repitam o pedido dizendo \"altere somente X\"."],
         ["O agente quer instalar uma biblioteca nova", "Perguntem: \"para que serve, qual a alternativa sem biblioteca, e ela funciona em site estático?\""],
         ["O agente sugere colocar uma chave de API, senha ou token no código", "Recusem. No GitHub Pages tudo é público."],
         ["Vocês precisam de um exemplo com dados", "Usem só dados sintéticos. Nunca colem planilha real da SESP no chat."],
         ["A conversa ficou longa e o agente começou a \"esquecer\" coisas", "Abram uma conversa nova (<b>+</b> no painel Agent) e comecem citando os arquivos com @."],
         ["O agente entrou em loop (erra, corrige, erra de novo)", "Parem. Voltem ao último commit bom (Discard Changes) e peçam uma abordagem diferente, mais simples."]]) +
    ficha("r", "Tarefas grandes em branch separada",
      "Antes de uma tarefa que mexe em muitos arquivos, criem uma branch (ex.: <code>sprint-3-telas</code>). Se der errado, "
      "a <code>main</code> e o site no ar continuam intactos. Detalhes na seção de versionamento.")
)

# =================================================================
# PARTE 3 — SPRINT 0
# =================================================================
grp("Parte 3 · Sprint 0 — preparar o terreno",
    "Instalar as ferramentas, criar o projeto sem perder o contexto.md e o sprint.md, publicar o repositório e fazer o agente "
    "provar que entendeu o projeto.")

section("instalar", "Passo 1 — Instalar Node.js e Python (e conferir o Git)",
    p("O Git vocês instalaram na Aula 6. Agora faltam duas ferramentas: o <b>Node.js</b>, que roda o TypeScript, o Vite e os "
      "testes, e o <b>Python</b>, que roda os scripts de dados.") +
    step([
        ("Node.js (versão LTS)", "Baixe em <b>nodejs.org</b> o instalador <b>LTS</b> para Windows e avance com as opções padrão. "
         "Ele instala junto o <code>npm</code>, o gerenciador de pacotes."),
        ("Python 3.12 ou mais novo", "Baixe em <b>python.org/downloads</b>. Na primeira tela do instalador, <b>marque \"Add python.exe to PATH\"</b> "
         "antes de clicar em Install Now.", "Esqueceu de marcar? Rode o instalador de novo, escolha Modify e marque a opção."),
        ("Feche e reabra o Antigravity", "O terminal só \"enxerga\" os programas novos depois de reaberto."),
        ("Confira no terminal", "Abra o terminal do Antigravity (<b>Terminal → New Terminal</b>) e rode os comandos abaixo. Cada um deve responder com um número de versão."),
    ]) +
    code("""
        node -v            # ex.: v22.x ou v24.x
        npm -v             # ex.: 10.x ou 11.x
        python --version   # ex.: Python 3.12.x
        git --version      # ex.: git version 2.x
        """, "terminal") +
    callout("err", "Erro: \"npm.ps1 não pode ser carregado porque a execução de scripts foi desabilitada\"",
      "É uma proteção do PowerShell no Windows. Rode uma vez só o comando abaixo e responda <b>S</b>. Depois feche e reabra o terminal." +
      code("Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned", "powershell")) +
    callout("err", "Erro: \"python\" abre a Microsoft Store",
      "O Windows tem um atalho falso do Python. Vá em <b>Configurações → Aplicativos → Configurações avançadas de aplicativos → "
      "Aliases de execução de aplicativo</b> e desligue <i>python.exe</i> e <i>python3.exe</i>. Ou use <code>py</code> no lugar de <code>python</code>.")
)

section("criar-projeto", "Passo 2 — Criar o projeto e trazer o contexto.md e o sprint.md",
    p("Vamos criar o esqueleto do aplicativo com o <b>Vite</b>, a ferramenta que roda o TypeScript no navegador durante o desenvolvimento "
      "e gera a versão final para publicar. O nome da pasta será o nome do repositório e o final do endereço do site, então escolham bem: "
      "<b>minúsculas, sem espaço, sem acento</b>, palavras separadas por hífen.") +
    step([
        ("Abra o terminal na pasta onde ficam seus projetos", "Ex.: <code>D:\\Dev</code>. No terminal: <code>cd D:\\Dev</code>"),
        ("Crie o projeto", "Rode o comando abaixo, trocando pelo nome do projeto de vocês. <code>vanilla-ts</code> = TypeScript puro, sem framework.",
         "Se o sprint.md de vocês definiu React, troquem por <code>react-ts</code>. Todo o resto do caderno funciona igual."),
        ("Instale as dependências", "Entre na pasta e rode <code>npm install</code>. Demora 1 a 2 minutos na primeira vez."),
        ("Traga os dois arquivos do NotebookLM", "Crie a pasta <code>docs</code> dentro do projeto e <b>mova</b> para ela o <code>contexto.md</code> e o <code>sprint.md</code>."),
        ("Abra a pasta no Antigravity", "<b>File → Open Folder</b> e escolham a pasta do projeto. Na barra lateral devem aparecer <code>docs/</code>, <code>src/</code>, <code>index.html</code>, <code>package.json</code>."),
        ("Teste", "Rode <code>npm run dev</code> e abram o endereço que aparecer (ex.: <code>http://localhost:5173/</code>). Apareceu a página de boas-vindas do Vite? O terreno está pronto. <code>Ctrl+C</code> no terminal para parar."),
    ]) +
    code(f"""
        cd D:\\Dev
        npm create vite@latest {REPO} -- --template vanilla-ts
        cd {REPO}
        npm install
        mkdir docs
        # mova contexto.md e sprint.md para a pasta docs/ (no Explorer do Antigravity: arrastar e soltar)
        npm run dev
        """, "terminal") +
    callout("err", "Não criem o projeto Vite dentro da pasta onde já estão o contexto.md e o sprint.md",
      "Numa pasta que já tem arquivos, o criador do Vite cancela. Se o agente sugerir a opção <code>--overwrite</code>, <b>ela apaga "
      "os arquivos que já estão lá</b>, incluindo os dois .md. Por isso o caminho seguro é: criar o projeto numa pasta nova e só "
      "depois mover os arquivos para dentro dela.") +
    prompt(f"""
        Estou no Windows, com o terminal na pasta D:\\Dev. Quero criar um projeto Vite com TypeScript chamado {REPO}.
        Me diga os comandos, um por vez, e explique em 1 linha o que cada um faz. Não use --overwrite e não apague nenhum arquivo.
        """, "Prefere que o agente conduza?")
)

section("publicar-repo", "Passo 3 — Versionar e publicar o repositório no GitHub",
    p("Agora que a pasta existe, ela vira um repositório Git publicado no GitHub, com o mesmo fluxo do Laboratório 1 da Aula 6.") +
    step([
        ("Confira o .gitignore", "O Vite já cria um <code>.gitignore</code> com <code>node_modules</code> e <code>dist</code>. Acrescentem no final as linhas do bloco abaixo, para o Python."),
        ("Inicialize e publique", "No painel <b>Source Control</b>, clique em <b>Publish to GitHub</b> e escolha <b>Public repository</b>. "
         "O GitHub Pages gratuito exige repositório público.", "Se aparecer \"Initialize Repository\" primeiro, clique nele, faça o primeiro commit e depois publique."),
        ("Primeiro commit", "Mensagem: <code>chore: estrutura inicial do projeto (Vite + TS) e documentos do NotebookLM</code>."),
        ("Confira no GitHub", f"Abra <code>https://github.com/SEU-USUARIO/{REPO}</code>: devem aparecer <code>docs/</code>, <code>src/</code> e os arquivos do Vite, mas <b>não</b> a pasta <code>node_modules</code>."),
    ]) +
    code("""
        # Python
        .venv/
        __pycache__/
        *.pyc
        .pytest_cache/
        """, ".gitignore (acrescentar)") +
    callout("note", "Um repositório por grupo",
      "Um integrante cria e publica. Os demais entram como colaboradores: <b>Settings → Collaborators → Add people</b> no GitHub. "
      "Depois cada um clona (Aula 6, Cenário A) e roda <code>npm install</code> na própria máquina.")
)

section("primeiro-prompt", "Passo 4 — O primeiro prompt: o agente lê o contexto e o sprint.md",
    p("Antes de escrever qualquer linha de código, façam o agente <b>provar que entendeu</b> o projeto. Esse prompt não gera código: "
      "gera um diagnóstico para vocês conferirem.") +
    prompt("""
        Leia com atenção @docs/contexto.md e @docs/sprint.md. NÃO escreva código ainda.
        Me devolva, em Markdown:
        1. O problema e a solução em 3 linhas, com as suas palavras.
        2. A lista de telas do MVP e qual papel (Admin, Editor, Leitor, Aprovador) usa cada uma.
        3. As entidades de dados com seus campos e tipos, em formato de tabela.
        4. As regras de negócio que você identificou, numeradas (RN01, RN02...).
        5. Os campos sensíveis (LGPD) e como devem ser mascarados.
        6. Uma tabela "item do sprint.md | como fica num site estático no GitHub Pages", apontando o que precisa ser adaptado.
        7. Contradições ou lacunas entre os dois arquivos e as perguntas que você faria ao grupo antes de começar.
        """, "Prompt 0.1 — Diagnóstico do projeto") +
    p("Leiam a resposta em grupo. Respondam às perguntas do item 7 e, se o item 6 apontou adaptações, peçam a versão ajustada do plano:") +
    prompt("""
        Com as respostas abaixo, reescreva o @docs/sprint.md adaptado para o GitHub Pages (site estático):
        - Backend/API vira a camada src/services em TypeScript lendo public/data/*.json.
        - Banco de dados vira JSON gerado por scripts/gerar_dados.py (Python) + IndexedDB/localStorage para cadastros.
        - Login vira seletor de papel (RBAC simulado).
        Mantenha a numeração das tarefas (S1.1, S1.2...) e acrescente em cada tarefa: arquivos, linguagem e critério de aceite.
        Salve em docs/sprint.md e me mostre um resumo do que mudou.
        Respostas do grupo: [COLE AQUI AS RESPOSTAS ÀS PERGUNTAS DO ITEM 7]
        """, "Prompt 0.2 — Adaptar o sprint.md ao GitHub Pages") +
    callout("tip", "Commit desta etapa", "<code>docs: diagnóstico do agente e sprint.md adaptado ao GitHub Pages</code>")
)

section("regras-projeto", "Passo 5 — O arquivo de regras do projeto (a \"memória\" do agente)",
    p("O agente não lembra das conversas anteriores quando vocês abrem uma nova. A solução é um arquivo com as regras "
      "permanentes do projeto, mencionado com <code>@</code> nos prompts. Peçam para o agente criá-lo:") +
    prompt("""
        Crie o arquivo docs/REGRAS-DO-PROJETO.md com as regras permanentes deste projeto, baseadas em @docs/contexto.md e @docs/sprint.md.
        Inclua, em tópicos curtos:
        - Stack: Vite + TypeScript estrito, PWA com vite-plugin-pwa, Python 3.12 só em scripts/, testes com Vitest e pytest.
        - Hospedagem: GitHub Pages, site estático. Base do Vite: '/[NOME-DO-REPO]/'. Rotas por hash (#/tela).
        - Caminhos de dados sempre com import.meta.env.BASE_URL, nunca "/data/..." fixo.
        - Estrutura de pastas: src/domain, src/auth, src/services, src/pages, src/components, scripts, public/data.
        - Dados: somente sintéticos; CPF e nomes sempre mascarados no Python antes de gerar o JSON.
        - Proibido: dados reais, senhas, chaves de API, bibliotecas novas sem aprovação, apagar arquivos sem pedir.
        - Código e comentários em português; nomes de variáveis em português sem acento (ex.: valorEstimado).
        - Cada tarefa termina com testes passando e uma sugestão de mensagem de commit (Conventional Commits).
        - Glossário do domínio: [TERMOS DO PROJETO, ex.: pedido, cotação, auditoria].
        Máximo de 1 página.
        """, "Prompt 0.3 — Criar as regras do projeto") +
    ficha("a", "Como usar daqui para frente",
      "Comecem toda conversa nova com: <i>\"Leia @docs/REGRAS-DO-PROJETO.md e @docs/contexto.md antes de qualquer coisa.\"</i> "
      "Se o agente desobedecer uma regra, respondam citando a regra. Se o Antigravity de vocês tiver a opção de "
      "<b>regras do workspace</b> nas configurações do agente, podem colar o conteúdo lá também.")
)

section("config-base", "Passo 6 — Configurar o Vite para o GitHub Pages (o \"base\")",
    p(f"O site de vocês não vai ficar na raiz do domínio, mas numa subpasta: <code>https://usuario.github.io/<b>{REPO}</b>/</code>. "
      "Se o Vite não souber disso, o site publicado abre <b>em branco</b>, porque procura os arquivos no lugar errado. É o erro mais comum de todos.") +
    code(f"""
        import {{ defineConfig }} from 'vite'

        // Troque pelo nome EXATO do seu repositório no GitHub (maiúsculas e minúsculas importam)
        const REPO = '{REPO}'

        export default defineConfig({{
          base: `/${{REPO}}/`,
        }})
        """, "vite.config.ts") +
    p("E, em todo lugar que o código buscar um arquivo de dados, usem o <code>BASE_URL</code> que o Vite preenche sozinho:") +
    code("""
        // ✗ ERRADO: funciona no computador, quebra no GitHub Pages
        const resp = await fetch('/data/pedidos.json')

        // ✓ CERTO: vira /mvp-pedidos-compra/data/pedidos.json no site publicado
        const resp = await fetch(`${import.meta.env.BASE_URL}data/pedidos.json`)
        """, "ts") +
    prompt("""
        Crie o arquivo vite.config.ts com base: '/[NOME-DO-REPO]/' para publicar no GitHub Pages.
        Depois procure em todo o src/ qualquer fetch ou caminho que comece com "/" e troque para usar import.meta.env.BASE_URL.
        Me mostre a lista do que alterou.
        """, "Prompt 0.4 — Configurar o base") +
    callout("tip", "Commit", "<code>chore: configura base do Vite para o GitHub Pages</code>")
)

# =================================================================
# PARTE 4 — SPRINTS
# =================================================================
grp("Parte 4 · Construindo sprint a sprint",
    "Dados sintéticos em Python, regras de negócio em TypeScript, telas, PWA, homologação e deploy automático. "
    "Cada sprint tem os prompts prontos, o gabarito do que conferir e as mensagens de commit.")

section("mapa-sprints", "O mapa das 5 sprints do MVP",
    p("As sprints abaixo seguem a sugestão da Aula 7, adaptadas para TS + Python + PWA no GitHub Pages. "
      "Se o sprint.md de vocês tem outra divisão, vale o de vocês: usem os prompts das próximas seções como modelo, "
      "trocando os códigos das tarefas.") +
    sprint(1, "Sprint 1 · Fundação e dados", "Python + TS · entregável: JSON sintéticos gerados e tipos definidos",
           ["Tipos das entidades em <code>src/domain/tipos.ts</code>;", "<code>scripts/gerar_dados.py</code> com dados sintéticos e máscara LGPD;",
            "testes pytest garantindo que nenhum dado sensível sai sem máscara."]) +
    sprint(2, "Sprint 2 · Regras de negócio, papéis e auditoria", "TS · entregável: regras testadas com Vitest",
           ["Camada <code>src/services/api.ts</code> lendo os JSON;", "regras RN01, RN02… em <code>src/domain/regras.ts</code>;",
            "RBAC simulado (<code>src/auth/papeis.ts</code>) e log de auditoria local."]) +
    sprint(3, "Sprint 3 · Telas e navegação", "TS + CSS · entregável: telas navegáveis no npm run dev",
           ["Rotas por hash, layout responsivo;", "painel com KPIs e gráfico, lista com filtros, formulário com validação;",
            "teste dos 5 segundos (o KPI principal salta aos olhos)."]) +
    sprint(4, "Sprint 4 · PWA e homologação", "TS + JS · entregável: app instalável, offline e revisado",
           ["<code>vite-plugin-pwa</code>, manifesto e ícones;", "testes por papel, varredura LGPD, Lighthouse;",
            "revisão de código pelo agente e pelo grupo."]) +
    sprint(5, "Sprint 5 · Deploy e documentação", "YAML + Markdown · entregável: link público funcionando",
           ["GitHub Actions publicando no GitHub Pages a cada push;", "README com roadmap, transparência de IA e LGPD;",
            "tag <code>v1.0.0</code> e o pitch de 3 minutos."])
)

section("s1-dados", "Sprint 1 — Modelagem e dados sintéticos com Python",
    aplicab("Primeira sprint: antes de qualquer tela.",
            "Tela sem dado não se testa. Com dados sintéticos realistas, vocês veem o painel \"vivo\" desde o início.",
            "120 pedidos de compra com protocolo, unidade, valor, status e CPF do solicitante mascarado.") +
    h3("1.1 · Tipos das entidades (TypeScript)") +
    prompt("""
        Leia @docs/REGRAS-DO-PROJETO.md e a seção de entidades de @docs/contexto.md.
        Tarefa S1.1: crie src/domain/tipos.ts com uma interface TypeScript para cada entidade (ex.: Pedido, Unidade, Cotacao).
        - Use tipos union para campos de lista fechada (ex.: status: 'rascunho' | 'enviado' | 'aprovado').
        - Datas como string ISO (AAAA-MM-DD).
        - Comente cada campo em 1 linha, em português.
        Pronto quando: npx tsc --noEmit roda sem erros.
        """, "Prompt S1.1 — Tipos") +
    h3("1.2 · Ambiente Python (uma vez por computador)") +
    code("""
        python -m venv .venv
        .venv\\Scripts\\Activate.ps1     # o terminal passa a mostrar (.venv) no começo da linha
        pip install pytest
        pip freeze > requirements.txt
        """, "terminal") +
    h3("1.3 · Script gerador de dados sintéticos") +
    prompt("""
        Leia @docs/REGRAS-DO-PROJETO.md, @docs/contexto.md e @src/domain/tipos.ts.
        Tarefa S1.2: crie scripts/gerar_dados.py (Python 3.12, somente biblioteca padrão) que gera dados SINTÉTICOS
        e grava um JSON por entidade em public/data/ (ex.: public/data/pedidos.json).
        Requisitos:
        - random.seed(42) para os dados serem sempre os mesmos (reprodutível).
        - Os campos do JSON devem ter EXATAMENTE os mesmos nomes das interfaces de tipos.ts.
        - Volume: [QUANTIDADE, ex.: 120 pedidos] distribuídos ao longo de 2026.
        - Realismo de Mato Grosso: unidades e municípios reais (Cuiabá, Várzea Grande, Rondonópolis...), valores plausíveis.
        - Inclua casos de borda: [EX.: 5 pedidos acima de R$ 50 mil, 3 devolvidos, 2 com campo opcional vazio].
        - CPF: gere CPF matematicamente válido e grave SOMENTE mascarado no formato ***.123.***-** (LGPD).
        - Nomes de pessoas: use nomes fictícios ou só a função (ex.: "Solicitante 014").
        - json.dumps com ensure_ascii=False e encoding utf-8.
        - No final, imprima quantos registros gerou por arquivo.
        Pronto quando: python scripts/gerar_dados.py roda e os arquivos aparecem em public/data/.
        """, "Prompt S1.2 — Gerador de dados") +
    p("Um trecho do que o script deve ter, para vocês conferirem na revisão:") +
    code("""
        random.seed(42)  # mesma semente = mesmos dados sempre

        def mascarar_cpf(cpf: str) -> str:
            return f"***.{cpf[3:6]}.***-**"

        pedidos.append({
            "protocolo": f"PC-2026-{i:04d}",
            "unidade": random.choice(UNIDADES),
            "solicitante_cpf": mascarar_cpf(cpf_valido()),   # nunca o CPF completo
            "valor_estimado": round(random.uniform(800, 95000), 2),
            "status": random.choice(STATUS),
        })
        """, "python") +
    h3("1.4 · Teste de LGPD com pytest") +
    prompt("""
        Tarefa S1.3: crie scripts/test_gerar_dados.py com pytest que:
        1. executa scripts/gerar_dados.py;
        2. falha se encontrar em qualquer arquivo de public/data/ um CPF completo (regex de 11 dígitos, com ou sem pontuação);
        3. confere a quantidade de registros e que todo registro tem os campos obrigatórios de @src/domain/tipos.ts;
        4. confere as regras de borda que pedi (ex.: existem pedidos acima de R$ 50 mil).
        Pronto quando: python -m pytest -q scripts mostra todos os testes passando.
        """, "Prompt S1.3 — Teste LGPD") +
    code("""
        python scripts/gerar_dados.py
        python -m pytest -q scripts
        """, "terminal") +
    callout("tip", "Commits da Sprint 1",
      "<code>feat(dominio): tipos das entidades (S1.1)</code> · <code>feat(dados): gerador de dados sintéticos (S1.2)</code> · "
      "<code>test(lgpd): garante CPF mascarado nos JSON (S1.3)</code>")
)

section("s2-logica", "Sprint 2 — Regras de negócio, papéis e auditoria em TypeScript",
    p("Esta sprint é o \"backend\" do MVP, rodando no navegador. A regra de ouro: <b>regra de negócio não fica dentro de tela</b>. "
      "Ela fica em funções puras em <code>src/domain/</code>, fáceis de testar.") +
    h3("2.1 · A camada de serviços (a \"API\" do MVP)") +
    prompt("""
        Leia @docs/REGRAS-DO-PROJETO.md e @src/domain/tipos.ts.
        Tarefa S2.1: crie src/services/api.ts com funções assíncronas que imitam uma API REST:
        listarPedidos(), obterPedido(id), listarUnidades() [AJUSTE PARA AS ENTIDADES DO PROJETO].
        - Leia os JSON com fetch(`${import.meta.env.BASE_URL}data/<arquivo>.json`).
        - Trate erro de rede com mensagem clara em português.
        - Guarde em memória o que já foi carregado (não buscar o mesmo JSON duas vezes).
        - Escreva as funções contra uma interface FonteDeDados, para no futuro trocar JSON por uma API real sem mudar as telas.
        """, "Prompt S2.1 — Serviços") +
    h3("2.2 · Regras de negócio com teste") +
    prompt("""
        Leia as regras de negócio (RN01, RN02...) em @docs/contexto.md.
        Tarefa S2.2: implemente cada regra como função pura em src/domain/regras.ts (sem acessar tela nem fetch).
        Crie src/domain/regras.test.ts com Vitest: pelo menos 2 testes por regra, incluindo o caso de limite
        (ex.: exatamente R$ 50.000,00 NÃO exige auditoria; R$ 50.000,01 exige).
        Adicione ao package.json o script "test": "vitest run" e instale o vitest como devDependency.
        Pronto quando: npm test mostra todos os testes passando. Me mostre a saída.
        """, "Prompt S2.2 — Regras + Vitest") +
    code("""
        export const LIMITE_AUDITORIA = 50000

        /** RN03 — pedido acima de R$ 50 mil exige auditoria da Controladoria */
        export function exigeAuditoria(p: Pedido): boolean {
          return p.valor_estimado > LIMITE_AUDITORIA
        }
        """, "ts") +
    h3("2.3 · Papéis e permissões (RBAC simulado)") +
    prompt("""
        Leia a tabela de papéis em @docs/contexto.md.
        Tarefa S2.3: crie src/auth/papeis.ts com:
        - type Papel = 'ADMIN' | 'EDITOR' | 'LEITOR' | 'APROVADOR' e type Acao = 'ver' | 'criar' | 'editar' | 'excluir' | 'aprovar' | 'ver_log';
        - uma tabela de permissões por papel, igual à do contexto.md;
        - função pode(papel, acao): boolean;
        - papel atual guardado no localStorage, com getPapelAtual() e setPapelAtual().
        Crie testes Vitest que conferem cada linha da tabela de permissões.
        Deixe claro em comentário que isto é uma SIMULAÇÃO para demonstração, não segurança real.
        """, "Prompt S2.3 — Papéis") +
    h3("2.4 · Log de auditoria e armazenamento local") +
    prompt("""
        Tarefa S2.4: crie src/services/auditoria.ts que registra cada ação relevante
        (criar, editar, excluir, aprovar) com: dataHora ISO, papel, acao, entidade, id, valorAntes, valorDepois.
        - Guarde no IndexedDB (sem biblioteca externa) ou, se for mais simples, no localStorage. Explique a escolha.
        - Função exportarCsv() que baixa o log como arquivo .csv (separador ;, UTF-8 com BOM para abrir certo no Excel).
        - O log não pode ser apagado pelo papel que gerou a ação (regra da Aula 7).
        Crie também src/services/armazenamento.ts para salvar os pedidos criados/editados pelo usuário,
        mesclando com os dados do JSON na hora de listar.
        """, "Prompt S2.4 — Auditoria") +
    callout("tip", "Commits da Sprint 2",
      "<code>feat(api): camada de serviços sobre JSON (S2.1)</code> · <code>feat(regras): RN01–RN0X com testes (S2.2)</code> · "
      "<code>feat(auth): RBAC simulado (S2.3)</code> · <code>feat(auditoria): log local com exportação CSV (S2.4)</code>")
)

section("s3-telas", "Sprint 3 — Telas, painel e navegação",
    p("Agora o MVP ganha cara. Lembrem das aulas de visualização: <b>título que diz a conclusão</b>, eixo começando no zero, "
      "cor com significado (vermelho = crítico, verde = meta), nada de pizza 3D.") +
    h3("3.1 · Rotas e layout") +
    prompt("""
        Leia @docs/REGRAS-DO-PROJETO.md e a lista de telas em @docs/contexto.md.
        Tarefa S3.1: crie src/router.ts com rotas por hash (#/painel, #/pedidos, #/pedidos/novo, #/auditoria) [AJUSTE ÀS TELAS].
        - Rota inicial: #/painel. Rota desconhecida: tela "Página não encontrada" com link para o painel.
        - Layout com cabeçalho (nome do sistema + seletor "Ver como: [papel]"), menu e área de conteúdo.
        - Cada tela em um arquivo de src/pages/ exportando uma função render(container).
        - Esconder do menu as telas que o papel atual não pode ver (use pode() de src/auth/papeis.ts).
        - CSS em src/style.css, mobile first, cores com variáveis CSS, contraste AA.
        Por que hash: o GitHub Pages não conhece rotas como /pedidos e devolveria erro 404 ao recarregar a página.
        """, "Prompt S3.1 — Rotas e layout") +
    h3("3.2 · O painel do gestor") +
    prompt("""
        Tarefa S3.2: crie src/pages/painel.ts, a tela principal para o [PAPEL, ex.: Secretário].
        - 4 cartões de KPI no topo, com os KPIs de @docs/contexto.md (valor grande + rótulo + comparação com a meta).
        - 1 gráfico de barras com Chart.js (instale chart.js) mostrando [MÉTRICA POR CATEGORIA], eixo Y começando em zero,
          título que afirma a conclusão (ex.: "Compras concentra 40% dos pedidos em atraso").
        - 1 tabela com os 10 itens que exigem atenção (ex.: aguardando auditoria há mais de 5 dias).
        - Tudo calculado com as funções de src/domain/regras.ts (nada de cálculo solto na tela).
        Pronto quando: em até 5 segundos alguém de fora do grupo diz qual é o indicador principal.
        """, "Prompt S3.2 — Painel") +
    h3("3.3 · Lista com filtros e formulário") +
    prompt("""
        Tarefa S3.3: crie src/pages/pedidos.ts com a lista de [ENTIDADE]:
        busca por texto, filtros por [CAMPOS, ex.: unidade e status], ordenação por coluna e paginação de 20 em 20.
        Os filtros ficam na URL (ex.: #/pedidos?status=aprovado) para o link poder ser compartilhado.
        Botões Editar/Excluir/Aprovar aparecem somente se pode(papelAtual, acao) for verdadeiro.
        """, "Prompt S3.3 — Lista") +
    prompt("""
        Tarefa S3.4: crie src/pages/formulario.ts para criar e editar [ENTIDADE].
        - Validação em português ao sair do campo e ao salvar (obrigatórios, valores mínimos, datas coerentes).
        - Campos sensíveis com máscara visual (ex.: CPF exibido como ***.123.***-**).
        - Ao salvar: grava via src/services/armazenamento.ts e registra no log de auditoria.
        - Acessibilidade: label em todo campo, navegação completa por teclado, mensagem de erro ligada ao campo (aria-describedby).
        """, "Prompt S3.4 — Formulário") +
    callout("note", "Viu algo feio? Mostre para o agente",
      "Tirem um print da tela (<code>Win+Shift+S</code>) e colem no painel Agent com o pedido: <i>\"Nesta tela, o cartão de KPI está "
      "cortado no celular. Corrija somente o CSS em src/style.css.\"</i> Imagem + pedido específico funcionam muito melhor que descrever.") +
    callout("tip", "Commits da Sprint 3",
      "<code>feat(ui): rotas por hash e layout (S3.1)</code> · <code>feat(painel): KPIs e gráfico (S3.2)</code> · "
      "<code>feat(pedidos): lista com filtros (S3.3)</code> · <code>feat(pedidos): formulário com validação (S3.4)</code>")
)

section("pwa", "Sprint 4a — Transformar em PWA (instalável e offline)",
    p("PWA (<i>Progressive Web App</i>) é um site que se comporta como aplicativo: tem ícone na tela inicial do celular, abre em "
      "tela cheia e funciona sem internet. Duas peças fazem isso: o <b>manifesto</b> (nome, ícones, cores) e o <b>service worker</b> "
      "(um JavaScript que guarda os arquivos no aparelho). O plugin <code>vite-plugin-pwa</code> gera os dois.") +
    step([
        ("Instale o plugin e o gerador de ícones", "Comandos no bloco logo abaixo."),
        ("Crie o ícone-fonte", "Um arquivo <code>public/icon.svg</code> quadrado (peçam ao agente um SVG simples com as iniciais do sistema)."),
        ("Gere os ícones PNG", "O gerador cria os tamanhos 64, 192, 512, o ícone \"maskable\" (Android), o do iPhone e o favicon."),
        ("Configure o vite.config.ts", "Com o bloco completo abaixo."),
        ("Teste", "<code>npm run build</code> e depois <code>npm run preview</code>. Abram o endereço mostrado, depois <b>F12 → Application → Manifest</b> "
         "(ícones sem erro) e <b>Service Workers</b> (status <i>activated</i>). Na barra de endereço deve aparecer o botão de instalar."),
    ]) +
    code("""
        npm install -D vite-plugin-pwa @vite-pwa/assets-generator
        npx pwa-assets-generator --preset minimal-2023 public/icon.svg
        """, "terminal") +
    code(f"""
        import {{ defineConfig }} from 'vite'
        import {{ VitePWA }} from 'vite-plugin-pwa'

        const REPO = '{REPO}'   // nome EXATO do repositório

        export default defineConfig({{
          base: `/${{REPO}}/`,
          plugins: [
            VitePWA({{
              registerType: 'autoUpdate',
              includeAssets: ['favicon.ico', 'apple-touch-icon-180x180.png'],
              manifest: {{
                name: 'Portal de Pedidos de Compra — SESP/MT (MVP)',
                short_name: 'Pedidos SESP',
                description: 'MVP acadêmico com dados sintéticos — Curso SESP/MT',
                lang: 'pt-BR',
                theme_color: '#1f4b8f',
                background_color: '#ffffff',
                display: 'standalone',
                start_url: '.',
                scope: '.',
                icons: [
                  {{ src: 'pwa-64x64.png', sizes: '64x64', type: 'image/png' }},
                  {{ src: 'pwa-192x192.png', sizes: '192x192', type: 'image/png' }},
                  {{ src: 'pwa-512x512.png', sizes: '512x512', type: 'image/png' }},
                  {{ src: 'maskable-icon-512x512.png', sizes: '512x512',
                    type: 'image/png', purpose: 'maskable' }},
                ],
              }},
              workbox: {{
                // inclui os JSON de public/data: o app abre offline com os dados
                globPatterns: ['**/*.{{js,css,html,svg,png,ico,json}}'],
              }},
            }}),
          ],
        }})
        """, "vite.config.ts (completo)") +
    callout("note", "Por que start_url e scope são \".\"",
      f"O ponto significa \"a pasta onde está o manifesto\", ou seja, <code>/{REPO}/</code>. Se colocarem <code>\"/\"</code>, "
      "o app instalado abre a raiz de <code>github.io</code> e dá erro 404.") +
    prompt("""
        Leia @vite.config.ts e @docs/REGRAS-DO-PROJETO.md.
        Tarefa S4.1: transforme o projeto em PWA com vite-plugin-pwa:
        - manifest com name "[NOME COMPLETO]", short_name "[NOME CURTO até 12 letras]", lang pt-BR, theme_color [COR],
          display standalone, start_url "." e scope "." (o site fica em subpasta do GitHub Pages);
        - crie public/icon.svg (quadrado 512x512, fundo [COR], iniciais "[SIGLA]" em branco) e gere os PNG com
          npx pwa-assets-generator --preset minimal-2023 public/icon.svg;
        - service worker com registerType autoUpdate, cacheando também os JSON de public/data para funcionar offline;
        - quando houver versão nova, mostrar um aviso discreto "Nova versão disponível — recarregar".
        Pronto quando: npm run build && npm run preview abre o site, o DevTools mostra o manifesto sem erros e,
        com a rede desligada (DevTools → Network → Offline), a página recarrega com os dados.
        """, "Prompt S4.1 — PWA completo") +
    callout("err", "Durante o desenvolvimento o service worker pode \"prender\" versões antigas",
      "Se a tela não mudar depois de um build novo: <b>F12 → Application → Service Workers → Unregister</b> e <code>Ctrl+Shift+R</code>. "
      "No celular com o app instalado: fechem e abram o app duas vezes (o <i>autoUpdate</i> troca a versão na segunda abertura).")
)

section("s4-testes", "Sprint 4b — Homologação: testes, LGPD e revisão",
    p("Homologar é provar, antes do público ver, que o sistema faz o que o contexto.md promete. Quatro frentes:") +
    tbl(["Frente", "Como verificar", "Ferramenta"],
        [["Regras de negócio", "Todos os testes passando", "<code>npm test</code> (Vitest)"],
         ["Dados e LGPD", "Nenhum dado sensível sem máscara nos JSON nem no site compilado", "<code>pytest</code> + prompt de varredura"],
         ["Papéis", "Cada papel vê e faz só o que pode", "Roteiro manual (prompt abaixo)"],
         ["Qualidade da página", "Desempenho, acessibilidade, boas práticas", "<b>F12 → Lighthouse</b> (meta: acima de 90)"]]) +
    prompt("""
        Leia @docs/contexto.md e @src/auth/papeis.ts.
        Gere um roteiro de teste manual em docs/roteiro-homologacao.md: para cada papel (Admin, Editor, Leitor, Aprovador),
        uma tabela Passo | Ação | Resultado esperado, cobrindo: telas visíveis, botões visíveis, criar, editar, aprovar,
        excluir e ver o log. Inclua 3 casos de erro (ex.: Leitor tentando acessar #/pedidos/novo pela URL).
        """, "Prompt S4.2 — Roteiro de testes por papel") +
    prompt("""
        Faça uma varredura de LGPD no projeto:
        1. Rode npm run build e procure em dist/ e em public/data/ qualquer CPF completo, e-mail, telefone ou nome que pareça real.
        2. Procure no código chaves de API, tokens, senhas ou URLs internas da SESP.
        3. Confira se o README avisa que os dados são sintéticos.
        Me devolva uma tabela Achado | Arquivo | Linha | Gravidade | Correção sugerida. Não corrija nada ainda.
        """, "Prompt S4.3 — Varredura LGPD") +
    prompt("""
        Atue como revisor de código sênior. Revise os arquivos alterados nesta sprint (@src/domain, @src/pages, @src/services).
        Procure: bugs, regra de negócio implementada diferente do @docs/contexto.md, cálculo feito dentro de tela,
        texto sem acento ou em inglês para o usuário, acessibilidade (labels, contraste, teclado) e código duplicado.
        Responda em tabela Problema | Arquivo:linha | Por que importa | Correção. Ordene do mais grave ao menos grave.
        Não altere nada: eu escolho o que corrigir.
        """, "Prompt S4.4 — Code review pelo agente") +
    callout("tip", "Commits da Sprint 4",
      "<code>feat(pwa): manifesto, ícones e offline (S4.1)</code> · <code>docs: roteiro de homologação (S4.2)</code> · "
      "<code>fix: correções da revisão e da varredura LGPD (S4.3/S4.4)</code>")
)

section("s5-deploy", "Sprint 5 — Deploy automático no GitHub Pages com GitHub Actions",
    p("O GitHub Actions é um computador do GitHub que, a cada <code>push</code>, baixa o código, gera os dados com Python, roda os "
      "testes, faz o build e publica no Pages. Se um teste falhar, <b>nada é publicado</b>, e o site no ar continua na última versão boa.") +
    flow_h([("⬆️", "push na<br>main"), ("🐍", "Python gera<br>dados + pytest"), ("🧪", "npm ci<br>+ npm test"),
            ("📦", "npm run<br>build"), ("🌐", "deploy no<br>Pages")]) +
    step([
        ("Ative o Pages com Actions (uma vez)", "No GitHub: repositório → <b>Settings → Pages → Build and deployment → Source: GitHub Actions</b>."),
        ("Crie o arquivo do workflow", "Caminho exato: <code>.github/workflows/deploy.yml</code> (com o ponto no começo de .github)."),
        ("Confira requirements.txt e package-lock.json", "Os dois precisam estar commitados: o Actions instala exatamente o que está neles."),
        ("Commit e push na main", "<code>ci: deploy automático no GitHub Pages</code>"),
        ("Acompanhe", "Aba <b>Actions</b> do repositório: bolinha amarela = rodando, verde = publicado, vermelha = falhou (cliquem para ver o passo que quebrou)."),
        ("Abra o site", f"<code>https://SEU-USUARIO.github.io/{REPO}/</code>. O endereço também aparece em Settings → Pages e no resumo do workflow."),
    ]) +
    code("""
        # Publica o MVP no GitHub Pages a cada push na branch main.
        # Pré-requisito (uma vez só): Settings → Pages → Source: "GitHub Actions".
        name: Deploy no GitHub Pages

        on:
          push:
            branches: [main]
          workflow_dispatch:        # botão "Run workflow" na aba Actions

        permissions:
          contents: read
          pages: write
          id-token: write

        concurrency:
          group: pages
          cancel-in-progress: true

        jobs:
          build:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v7

              - name: Python — gerar dados sintéticos e testar LGPD
                uses: actions/setup-python@v7
                with:
                  python-version: '3.12'
              - run: pip install -r requirements.txt
              - run: python scripts/gerar_dados.py
              - run: python -m pytest -q scripts

              - name: Node — instalar, testar e compilar o front-end
                uses: actions/setup-node@v7
                with:
                  node-version: '22'
              - run: npm ci
              - run: npm test
              - run: npm run build

              - uses: actions/configure-pages@v6
              - uses: actions/upload-pages-artifact@v5
                with:
                  path: dist

          deploy:
            needs: build
            runs-on: ubuntu-latest
            environment:
              name: github-pages
              url: ${{ steps.deployment.outputs.page_url }}
            steps:
              - id: deployment
                uses: actions/deploy-pages@v5
        """, ".github/workflows/deploy.yml") +
    ficha("g", "Validado",
      "Este workflow e o <code>vite.config.ts</code> da Sprint 4a foram testados num projeto de referência: build, testes Python e "
      "Vitest, site servido na subpasta do repositório, navegação por hash e funcionamento offline. As versões das actions "
      "(<code>checkout@v7</code>, <code>deploy-pages@v5</code>…) eram as mais recentes em setembro de 2026. Se o agente sugerir "
      "uma versão mais nova, podem aceitar.") +
    prompt("""
        Leia @docs/REGRAS-DO-PROJETO.md, @package.json e @vite.config.ts.
        Tarefa S5.1: crie .github/workflows/deploy.yml para publicar no GitHub Pages a cada push na main:
        job build (checkout; Python 3.12 com pip install -r requirements.txt, python scripts/gerar_dados.py e pytest;
        Node 22 com npm ci, npm test e npm run build; upload-pages-artifact com path dist) e job deploy com deploy-pages.
        Permissões: contents read, pages write, id-token write. Use as versões mais recentes das actions oficiais.
        Depois me diga, passo a passo, o que devo configurar em Settings → Pages no GitHub.
        """, "Prompt S5.1 — Workflow de deploy") +
    prompt("""
        O workflow do GitHub Actions falhou. Abaixo está o log do passo que ficou vermelho.
        Explique a causa em linguagem simples, diga em qual arquivo está o problema e proponha a correção mínima.
        Log: [COLE AQUI O TRECHO DO LOG, a partir da primeira linha com "Error"]
        """, "Prompt S5.2 — Quando o deploy falhar") +
    callout("err", "O site abriu em branco?",
      "Em 9 de cada 10 casos é o <code>base</code> do <code>vite.config.ts</code> diferente do nome do repositório (atenção a maiúsculas). "
      "Abram <b>F12 → Console</b>: erros 404 em arquivos <code>/assets/...</code> confirmam o diagnóstico.")
)

section("versionamento", "Versionamento profissional: branches, commits, PRs e tags",
    p("Com o deploy automático, a <code>main</code> é o que está no ar. Por isso ela só recebe código testado. O trabalho do dia a dia "
      "acontece em <b>branches</b>.") +
    flow_h([("🌿", "Criar branch<br>sprint-3-telas"), ("💾", "Commits<br>por tarefa"), ("⬆️", "Push da<br>branch"),
            ("🔀", "Pull Request<br>para a main"), ("👀", "Colega<br>revisa"), ("🚀", "Merge =<br>deploy")]) +
    tbl(["Prática", "Como fazer no Antigravity/GitHub", "Exemplo"],
        [["Branch por sprint ou tarefa grande", "Barra inferior (nome da branch) → <b>Create new branch</b>", "<code>sprint-2-regras</code>, <code>fix-grafico-mobile</code>"],
         ["Conventional Commits", "Prefixo que diz o tipo da mudança", "<code>feat:</code> nova função · <code>fix:</code> correção · <code>test:</code> · <code>docs:</code> · <code>ci:</code> · <code>chore:</code>"],
         ["Pull Request (PR)", "GitHub → aba <b>Pull requests → New</b> (ou o botão que aparece após o push da branch)", "\"Sprint 2: regras de negócio e papéis\""],
         ["Revisão em dupla", "Outro integrante lê o PR, testa localmente e aprova", "Comentário: \"testei como Leitor, OK\""],
         ["Tag de versão", "Ao fim de cada sprint: GitHub → <b>Releases → Draft a new release</b>", "<code>v0.1.0</code> (Sprint 1) … <code>v1.0.0</code> (MVP)"],
         ["Issues", "Uma issue por tarefa do sprint.md; o commit cita o número", "<code>feat(painel): KPIs (S3.2) #12</code>"]]) +
    prompt("""
        Analise as mudanças ainda não commitadas (git diff) e sugira:
        1. se devem virar 1 commit ou vários (agrupe por assunto);
        2. a mensagem de cada commit no padrão Conventional Commits, em português, citando o código da tarefa do sprint.md.
        Não faça o commit: só me mostre as sugestões.
        """, "Prompt V1 — Mensagens de commit") +
    prompt("""
        Leia @docs/sprint.md e gere a descrição de um Pull Request da branch atual para a main, com:
        Resumo (3 linhas), Tarefas concluídas (com códigos S?.?), Como testar (passos para o revisor), Prints sugeridos,
        Checklist (testes passando, LGPD verificada, sem dados reais).
        """, "Prompt V2 — Descrição de Pull Request") +
    prompt("""
        Leia @docs/sprint.md e transforme cada tarefa em uma issue do GitHub:
        título "[S?.?] descrição curta", corpo com critério de aceite em checklist e rótulo (sprint-1, sprint-2...).
        Entregue em Markdown para eu colar uma a uma no GitHub.
        """, "Prompt V3 — Issues a partir do sprint.md")
)

section("readme", "README e transparência: documentando o que a IA fez",
    p("Na Aula 7 ficou combinado: o README lista o que a IA gerou, quais prompts foram usados e o que foi revisado por pessoas. "
      "Isso é <b>maturidade técnica</b>, não confissão. Numa auditoria, é o que prova que houve controle humano.") +
    prompt("""
        Leia @docs/contexto.md, @docs/sprint.md e a estrutura do projeto.
        Escreva o README.md do repositório, em português, com as seções:
        1. Nome do sistema + link do site no GitHub Pages + print da tela principal (deixe o marcador da imagem).
        2. O problema e a solução (3 linhas) e os KPIs.
        3. Como usar: papéis disponíveis no seletor "Ver como" e o que cada um faz.
        4. Tecnologias: TypeScript + Vite, PWA, Python (dados sintéticos), Vitest, pytest, GitHub Actions/Pages.
        5. Como rodar localmente: pré-requisitos e comandos (npm install, python scripts/gerar_dados.py, npm run dev, npm test).
        6. Estrutura de pastas.
        7. Roadmap: as 5 sprints com status (✅/🚧) e link para a release de cada uma.
        8. Privacidade e LGPD: dados 100% sintéticos, campos mascarados, o que o sistema real precisaria (servidor, autenticação, logs em banco).
        9. Transparência sobre IA: tabela Parte do sistema | Gerado por IA? | Revisado por | Prompt principal usado.
        10. Equipe: [NOMES E PAPÉIS DO GRUPO].
        """, "Prompt R1 — README completo") +
    callout("note", "Print da tela no README",
      "Salvem o print em <code>docs/img/painel.png</code> e usem <code>![Painel](docs/img/painel.png)</code>. Conferiram que o print não "
      "mostra nenhum dado que pareça real?")
)

# =================================================================
# PARTE 5 — BIBLIOTECA DE PROMPTS
# =================================================================
grp("Parte 5 · Biblioteca de prompts",
    "Prompts prontos para consultar quando precisar: planejar, construir cada camada, depurar erros e revisar o código.")

section("prompts-planejamento", "Prompts de planejamento e entendimento",
    p("Para usar no início de cada sprint ou quando o grupo estiver travado.") +
    prompt("""
        Leia @docs/sprint.md e @docs/REGRAS-DO-PROJETO.md. Estamos começando a Sprint [N].
        Liste as tarefas desta sprint na ordem em que devem ser feitas (dependências primeiro),
        estime cada uma em P/M/G e aponte quais podem ser feitas em paralelo por pessoas diferentes do grupo.
        """, "P1 — Planejar a sprint") +
    prompt("""
        Explique, como para alguém que nunca programou, o que faz o arquivo @[ARQUIVO].
        Use no máximo 10 linhas, e depois liste as 3 partes mais importantes do código com o número da linha.
        """, "P2 — Entender um arquivo") +
    prompt("""
        Desenhe em Mermaid (flowchart LR) a arquitetura atual do projeto: pastas src/, scripts/, public/data/,
        o fluxo de dados do Python até a tela e o deploy pelo GitHub Actions. Salve em docs/arquitetura.md.
        """, "P3 — Diagrama da arquitetura") +
    prompt("""
        Compare o que já foi implementado com @docs/sprint.md. Monte uma tabela Tarefa | Status (feito/parcial/não iniciado) |
        Evidência (arquivo ou teste) | O que falta. Seja rigoroso: sem teste, é "parcial".
        """, "P4 — Onde estamos?") +
    prompt("""
        Tenho [N HORAS] de aula para terminar o MVP. Olhando @docs/sprint.md e o que já existe, proponha o corte de escopo:
        o que é essencial para a demonstração, o que pode ser simplificado e o que fica para depois. Justifique cada item.
        """, "P5 — Cortar escopo com critério")
)

section("prompts-codigo", "Prompts de construção por camada",
    h3("Dados (Python)") +
    prompt("""
        Acrescente ao scripts/gerar_dados.py a entidade [ENTIDADE] com os campos de @src/domain/tipos.ts,
        ligada a [OUTRA ENTIDADE] pelo campo [CHAVE]. Toda chave estrangeira deve existir (sem órfãos).
        Adicione um teste pytest que prova isso.
        """, "C1 — Nova entidade relacionada") +
    prompt("""
        Os dados estão "bonitos demais". Ajuste o gerador para ter padrões realistas:
        sazonalidade (mais pedidos em [MESES]), [UNIDADE] com o dobro de devoluções, e 3% de registros com campo opcional vazio.
        Documente esses padrões em docs/dados.md para usarmos no pitch.
        """, "C2 — Dados com história para contar") +
    h3("Regras e serviços (TypeScript)") +
    prompt("""
        Implemente a regra [RN0X: DESCRIÇÃO] como função pura em src/domain/regras.ts.
        Antes do código, escreva os testes Vitest (incluindo casos de limite) e me mostre. Depois implemente até passarem.
        """, "C3 — Regra nova, testes primeiro") +
    prompt("""
        Crie a função calcularKpis(pedidos) em src/domain/kpis.ts que devolve [LISTA DE KPIs DO CONTEXTO.MD],
        cada um com valor, meta, variação percentual e status ('ok' | 'atencao' | 'critico'). Com testes.
        """, "C4 — Cálculo de KPIs") +
    h3("Telas (TypeScript + CSS)") +
    prompt("""
        Crie o componente src/components/kpiCard.ts: recebe {titulo, valor, meta, status} e devolve o HTML do cartão.
        Cor pelo status (verde/âmbar/vermelho) com texto além da cor (acessibilidade). Use em src/pages/painel.ts.
        """, "C5 — Componente reutilizável") +
    prompt("""
        Adicione em src/pages/[TELA].ts um botão "Exportar CSV" que baixa os dados filtrados na tela,
        separador ;, UTF-8 com BOM (abre certo no Excel), nome do arquivo com a data. Registre a exportação no log de auditoria.
        """, "C6 — Exportar CSV") +
    prompt("""
        Deixe a tela [TELA] responsiva: no celular (até 480px) a tabela vira lista de cartões e os filtros ficam
        num painel recolhível. Altere somente o CSS e o mínimo de HTML necessário.
        """, "C7 — Versão celular") +
    prompt("""
        Adicione um modo escuro ao app: variáveis CSS para as cores, respeitando prefers-color-scheme,
        com botão para alternar e a escolha salva no localStorage. Garanta contraste AA nos dois temas.
        """, "C8 — Tema escuro") +
    h3("PWA") +
    prompt("""
        Mostre um aviso "Você está offline — exibindo os últimos dados salvos" quando navigator.onLine for falso,
        e esconda quando a conexão voltar. Não bloqueie o uso do app.
        """, "C9 — Aviso de offline")
)

section("prompts-depuracao", "Prompts de depuração: quando algo dá errado",
    p("O segredo é dar ao agente o <b>erro completo</b>, <b>o que vocês fizeram</b> e <b>o que esperavam</b>. \"Não funciona\" não é um relato de erro.") +
    prompt("""
        Rodei [COMANDO, ex.: npm run build] e deu o erro abaixo. Eu esperava [RESULTADO ESPERADO].
        Explique a causa em linguagem simples, mostre o arquivo e a linha, e proponha a MENOR correção possível.
        Não altere outros arquivos.
        Erro completo:
        [COLE O ERRO INTEIRO DO TERMINAL]
        """, "D1 — Erro no terminal") +
    prompt("""
        A tela [TELA] abre em branco. No console do navegador (F12 → Console) aparece:
        [COLE AS MENSAGENS VERMELHAS]
        Investigue a causa antes de mudar código: me diga as hipóteses em ordem de probabilidade e como confirmar cada uma.
        """, "D2 — Tela em branco") +
    prompt("""
        Localmente funciona, mas no GitHub Pages (https://[USUARIO].github.io/[REPO]/) [O QUE ACONTECE].
        Verifique: base do vite.config.ts, caminhos com "/" fixo, uso de import.meta.env.BASE_URL,
        rotas sem hash, start_url/scope do manifesto e maiúsculas no nome do repositório.
        """, "D3 — Funciona local, quebra no Pages") +
    prompt("""
        O teste [NOME DO TESTE] está falhando. Antes de mexer: me diga se o erro está no TESTE ou no CÓDIGO,
        comparando com a regra em @docs/contexto.md. Não altere o teste só para ele passar.
        """, "D4 — Teste falhando") +
    prompt("""
        Você já tentou corrigir isto 3 vezes sem sucesso. Pare. Resuma o que tentou, por que cada tentativa falhou,
        e proponha uma abordagem diferente e mais simples. Espere meu OK.
        """, "D5 — Agente em loop") +
    prompt("""
        Depois de publicar uma versão nova, o app instalado no celular continua mostrando a versão antiga.
        Verifique a configuração do vite-plugin-pwa (registerType, aviso de atualização) e me explique como forçar a atualização.
        """, "D6 — PWA preso na versão antiga")
)

section("prompts-revisao", "Prompts de revisão, refatoração e documentação",
    prompt("""
        Revise @[ARQUIVO] procurando código duplicado, funções com mais de 40 linhas e nomes pouco claros.
        Proponha a refatoração em passos pequenos, cada um mantendo os testes passando. Não mude comportamento.
        """, "R1 — Refatorar com segurança") +
    prompt("""
        Rode npm test e python -m pytest -q scripts e me diga quais funções de src/domain e scripts NÃO têm teste.
        Escreva os testes que faltam para as 3 mais importantes para o negócio.
        """, "R2 — Cobrir o que falta") +
    prompt("""
        Audite a acessibilidade das telas: labels, ordem de tabulação, foco visível, contraste, textos alternativos,
        uso de cor como única informação. Tabela Problema | Tela | Correção. Depois corrija os 5 mais graves.
        """, "R3 — Acessibilidade") +
    prompt("""
        Rodei o Lighthouse (F12 → Lighthouse) e o resultado foi: [COLE AS NOTAS E OS ITENS APONTADOS].
        Explique cada item em linguagem simples e corrija os que mais tiram ponto, um por vez, sem mudar o visual.
        """, "R4 — Melhorar a nota do Lighthouse") +
    prompt("""
        Gere o roteiro do pitch de 3 minutos do MVP: Minuto 1 — o problema com número; Minuto 2 — a demonstração
        (qual tela mostrar, em qual papel, qual clique); Minuto 3 — a recomendação e o próximo passo para a SESP.
        Use os dados de public/data e os KPIs de @docs/contexto.md.
        """, "R5 — Roteiro do pitch")
)

section("prompts-antipadroes", "Prompts ruins × prompts bons",
    p("Os mesmos pedidos, antes e depois. A diferença está no contexto, no escopo e no critério de pronto.") +
    antesdepois("Faz o sistema.",
                "Leia @docs/sprint.md e execute só a tarefa S1.2 (gerador de dados). Mostre o plano antes. Pronto quando o pytest passar.") +
    antesdepois("Arruma o erro.",
                "npm run build falhou com o erro abaixo. Explique a causa e proponha a menor correção, sem mexer em outros arquivos. [erro completo]") +
    antesdepois("Deixa o painel bonito.",
                "No painel, os KPIs estão sem hierarquia. Aumente o valor para 32px, rótulo em cinza 13px, cor pelo status. Só src/style.css.") +
    antesdepois("Coloca login no sistema.",
                "Implemente o seletor 'Ver como' com os 4 papéis de @docs/contexto.md, usando pode() de src/auth/papeis.ts. Sem senha: é simulação.") +
    antesdepois("Usa os dados da planilha da secretaria.",
                "Gere dados sintéticos com a mesma estrutura de colunas abaixo, sem nenhum valor real. [só os nomes das colunas]") +
    antesdepois("Melhora o código.",
                "Revise @src/pages/pedidos.ts: aponte duplicações e cálculos que deveriam estar em src/domain. Tabela de achados, sem alterar nada.")
)

# =================================================================
# FECHAMENTO
# =================================================================
grp("Fechamento", "Os problemas mais comuns e como resolver, o checklist de entrega, o glossário e um quiz para revisar.")

section("problemas", "Problemas comuns e como resolver",
    tbl(["Sintoma", "Causa provável", "Solução"],
        [["Site publicado em branco", "<code>base</code> do Vite diferente do nome do repositório", "Corrigir <code>vite.config.ts</code> (maiúsculas importam), commit e push"],
         ["404 ao carregar <code>/data/*.json</code>", "Caminho com \"/\" fixo", "Usar <code>import.meta.env.BASE_URL</code>"],
         ["404 ao recarregar numa tela", "Rota sem hash (<code>/pedidos</code>)", "Usar rotas por hash (<code>#/pedidos</code>)"],
         ["Actions: erro no job <code>deploy</code> dizendo que o Pages não está configurado", "Pages não configurado para Actions", "Settings → Pages → Source: <b>GitHub Actions</b>"],
         ["Actions: <code>npm ci</code> falhou", "<code>package-lock.json</code> não commitado ou desatualizado", "Rodar <code>npm install</code> e commitar o lock"],
         ["Actions: <code>pip install</code> falhou", "Falta o <code>requirements.txt</code>", "<code>pip freeze > requirements.txt</code> e commitar"],
         ["\"npm.ps1 não pode ser carregado\"", "Política de scripts do PowerShell", "<code>Set-ExecutionPolicy -Scope CurrentUser RemoteSigned</code>"],
         ["<code>python</code> abre a Microsoft Store", "Alias do Windows", "Desligar os aliases ou usar <code>py</code>"],
         ["Push rejeitado (<i>rejected, fetch first</i>)", "Um colega enviou antes", "<b>Pull</b> (Sync) primeiro, depois push"],
         ["Conflito de merge", "Duas pessoas editaram a mesma linha", "Abrir o arquivo e escolher <i>Accept Current/Incoming/Both</i>; na dúvida, pedir ao agente para explicar o conflito"],
         ["App não atualiza após o deploy", "Service worker com versão antiga", "F12 → Application → Unregister + <code>Ctrl+Shift+R</code>"],
         ["<code>node_modules</code> apareceu no GitHub", "<code>.gitignore</code> ausente no primeiro commit", "<code>git rm -r --cached node_modules</code> (tira do Git sem apagar do disco) e commit"],
         ["O agente mexeu em arquivos demais", "Prompt sem limite de escopo", "Source Control → Discard Changes nos arquivos indevidos; repetir com \"altere somente X\""]])
)

section("checklist", "Checklist de entrega do Dia 8 (Definição de Pronto)",
    h3("Repositório") +
    checklist(["Repositório público no GitHub com todos os integrantes como colaboradores",
               "<code>docs/contexto.md</code>, <code>docs/sprint.md</code> e <code>docs/REGRAS-DO-PROJETO.md</code> commitados",
               "<code>.gitignore</code> funcionando: sem <code>node_modules</code>, <code>dist</code> e <code>.venv</code> no repositório",
               "Commits pequenos, com mensagens no padrão Conventional Commits"]) +
    h3("Código") +
    checklist(["<code>scripts/gerar_dados.py</code> gera os JSON sintéticos; <code>pytest</code> passa (LGPD garantida)",
               "Regras de negócio em <code>src/domain</code> com testes; <code>npm test</code> passa",
               "Seletor de papel funcionando; cada papel vê só o que pode",
               "Painel com os KPIs do contexto.md, passando no teste dos 5 segundos",
               "PWA: instalável, com ícone e abrindo offline"]) +
    h3("Publicação") +
    checklist(["Workflow do GitHub Actions verde na aba Actions",
               "Site abrindo em <code>https://SEU-USUARIO.github.io/NOME-DO-REPO/</code>, inclusive no celular",
               "README com link, como rodar, roadmap, LGPD e transparência sobre IA",
               "Release/tag da última sprint concluída",
               "Pitch de 3 minutos ensaiado com o site publicado"])
)

section("glossario", "Glossário rápido",
    grid2([
        ("Construção", glossary([
            ("Vite", "Ferramenta que roda o projeto em desenvolvimento (<code>npm run dev</code>) e gera a versão final (<code>npm run build</code>)."),
            ("TypeScript (TS)", "JavaScript com tipos. Aponta erros antes de rodar. Vira JS no build."),
            ("Build / dist/", "O processo de compilar o projeto e a pasta com o resultado, que é o que vai para o Pages."),
            ("npm / package.json", "Gerenciador de pacotes do Node e o arquivo que lista dependências e scripts."),
            ("venv / pip", "Ambiente isolado do Python e o instalador de pacotes Python."),
            ("Vitest / pytest", "Ferramentas de teste automatizado para TypeScript e para Python."),
            ("Função pura", "Função que só depende das entradas e não mexe em tela nem rede. Fácil de testar."),
        ])),
        ("Publicação", glossary([
            ("PWA", "Site que se instala como app, com ícone, tela cheia e modo offline."),
            ("Service worker", "JavaScript que roda em segundo plano e guarda arquivos para o modo offline."),
            ("Manifesto", "Arquivo com nome, ícones e cores do app instalado."),
            ("GitHub Pages", "Hospedagem gratuita de sites estáticos a partir de um repositório."),
            ("GitHub Actions / workflow", "Automação do GitHub; o workflow é o arquivo YAML com os passos."),
            ("base", "Subpasta onde o site fica publicado (<code>/nome-do-repo/</code>)."),
            ("Rota por hash", "Endereço de tela depois do # (<code>#/painel</code>); funciona em hospedagem estática."),
            ("Pull Request / Tag", "Pedido de revisão para juntar uma branch na main; marco de versão (<code>v1.0.0</code>)."),
        ])),
    ])
)

section("quiz", "Quiz rápido",
    q("O site publicado abre em branco, mas no <code>npm run dev</code> funciona. Qual a primeira coisa a conferir?",
      ["O token do GitHub", "O <code>base</code> do <code>vite.config.ts</code>", "A versão do Python", "O tema escuro"], 1,
      "O Pages publica em <code>/nome-do-repo/</code>; sem o base certo, o navegador procura os arquivos na raiz.") +
    q("Onde deve ficar o mascaramento do CPF?",
      ["No CSS da tela", "No script Python, antes de gerar o JSON", "No README", "No service worker"], 1,
      "Se o dado completo chega ao JSON, ele é público no GitHub Pages, mesmo que a tela esconda.") +
    q("Por que usar rotas como <code>#/pedidos</code> em vez de <code>/pedidos</code>?",
      ["É mais bonito", "O GitHub Pages não conhece as rotas do app e daria 404 ao recarregar", "O TypeScript exige", "Para o PWA ter ícone"], 1) +
    q("O agente quer rodar <code>npm create vite . --overwrite</code> na pasta com o contexto.md. O que fazer?",
      ["Aprovar, é rápido", "Recusar: --overwrite apaga os arquivos existentes", "Aprovar e recuperar depois pelo Pages", "Rodar como administrador"], 1) +
    q("Qual é o tamanho ideal de um pedido ao agente?",
      ["A sprint inteira", "Uma tarefa do sprint.md, com critério de pronto", "O projeto todo de uma vez", "Uma linha de código"], 1) +
    q("Um teste falhou. O agente propõe mudar o teste para ele passar. Qual a atitude correta?",
      ["Aceitar", "Verificar no contexto.md se o erro está no teste ou no código", "Apagar o teste", "Desligar o Vitest no workflow"], 1)
)

# =================================================================
# BUILD
# =================================================================
def build_toc():
    out = ""
    for gi, (gtitle, _) in enumerate(grupos):
        out += f'<div class="grp">{gtitle}</div>'
        for anchor, titulo, _, g in sections:
            if g == gi:
                out += f'<a href="#{anchor}" data-anchor="{anchor}">{titulo}</a>'
    return out

def build_sumario():
    out = '<div class="sumario"><h2>Sumário</h2>'
    for gi, (gtitle, _) in enumerate(grupos):
        out += f'<div class="sg">{gtitle}</div>'
        for i, (anchor, titulo, _, g) in enumerate(sections, start=1):
            if g == gi:
                pg = PAGINAS.get(anchor, "")
                out += (f'<div class="si"><span class="n">{i}</span><span>{titulo}</span>'
                        f'<span class="dots"></span><span class="pg">{pg}</span></div>')
    return out + "</div>"

def build_sections():
    out = ""
    visto = set()
    for i, (anchor, titulo, body, g) in enumerate(sections, start=1):
        banner, cls = "", ""
        if g not in visto:
            visto.add(g)
            cls = ' class="inicio-parte"'
            gtitle, gdesc = grupos[g]
            nomes = "".join(f"<li>{t}</li>" for _, t, _, gg in sections if gg == g)
            kicker, _, resto = gtitle.partition(" · ")
            banner = (f'<div class="parte"><div class="pk">{kicker}</div>'
                      f'<div class="pt">{resto or kicker}</div><p class="pd">{gdesc}</p><ol>{nomes}</ol></div>')
        out += (f'<section id="{anchor}"{cls}>{banner}<div class="shead"><span class="secnum">§ {i}</span>'
                f'<h2>{titulo}</h2></div>{body}</section>')
    return out

TEMPLATE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Caderno do Dia 8 · SESP/MT</title>
<meta name="description" content="Caderno do Dia 8 do Curso SESP/MT: do contexto.md e sprint.md ao MVP publicado — TypeScript, Python e PWA no Antigravity, versionado no GitHub e publicado no GitHub Pages, com biblioteca de prompts.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>__CSS__</style>
</head>
<body>
<header class="top">
  <div class="inner">
    <span class="kicker">Aula 8 · Construindo o MVP</span>
    <h1>Do sprint.md ao MVP no ar</h1>
    <p class="sub">Passo a passo e biblioteca de prompts para construir o MVP do grupo no Antigravity:
      TypeScript e Python num PWA, versionado no GitHub e publicado automaticamente no GitHub Pages.</p>
    <div class="meta">Curso de Capacitação SESP/MT · Professor Renato Rosa · Dia 8</div>
  </div>
</header>
__SUMARIO__
<div class="wrap shell">
  <nav class="toc">
    <input type="text" id="tocsearch" placeholder="Buscar no índice...">
    <div id="tocgroups">__TOC__</div>
  </nav>
  <main>
    __SECTIONS__
  </main>
</div>
<footer class="pagefoot">Caderno do Dia 8 · Curso de Capacitação SESP/MT · Professor Renato Rosa</footer>
<button class="themebtn" id="themebtn">🌗 Tema</button>
<button class="pdfbtn" id="pdfbtn">🖨️ Imprimir / PDF</button>
<script>
(function(){
  var btnT = document.getElementById('themebtn');
  var root = document.documentElement;
  var saved = null;
  try { saved = localStorage.getItem('caderno-theme'); } catch(e) {}
  if (saved) root.setAttribute('data-theme', saved);
  btnT.addEventListener('click', function(){
    var cur = root.getAttribute('data-theme');
    var next = cur === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('caderno-theme', next); } catch(e) {}
  });
  document.getElementById('pdfbtn').addEventListener('click', function(){ window.print(); });

  // ao imprimir, abre as respostas do quiz
  var abertos = [];
  window.addEventListener('beforeprint', function(){
    document.querySelectorAll('details:not([open])').forEach(function(d){ d.open = true; abertos.push(d); });
  });
  window.addEventListener('afterprint', function(){ abertos.forEach(function(d){ d.open = false; }); abertos = []; });

  // botão "Copiar" em cada bloco de código/prompt
  document.querySelectorAll('ul.f').forEach(function(block){
    var b = document.createElement('button');
    b.className = 'cpy'; b.type = 'button'; b.textContent = 'Copiar';
    b.addEventListener('click', function(){
      var txt = Array.prototype.map.call(block.querySelectorAll('li'), function(li){ return li.textContent; }).join('\\n');
      var done = function(){ b.textContent = 'Copiado ✓'; setTimeout(function(){ b.textContent = 'Copiar'; }, 1500); };
      if (navigator.clipboard) { navigator.clipboard.writeText(txt).then(done, function(){}); }
      else { var t = document.createElement('textarea'); t.value = txt; document.body.appendChild(t); t.select();
             try { document.execCommand('copy'); done(); } catch(e) {} document.body.removeChild(t); }
    });
    block.appendChild(b);
  });

  var links = Array.prototype.slice.call(document.querySelectorAll('nav.toc a'));
  var secs = Array.prototype.slice.call(document.querySelectorAll('main section'));
  function onScroll(){
    var pos = window.scrollY + 120;
    var current = secs[0];
    secs.forEach(function(s){ if (s.offsetTop <= pos) current = s; });
    links.forEach(function(a){ a.classList.toggle('active', a.getAttribute('data-anchor') === current.id); });
  }
  window.addEventListener('scroll', onScroll);
  onScroll();

  var search = document.getElementById('tocsearch');
  search.addEventListener('input', function(){
    var term = search.value.toLowerCase();
    links.forEach(function(a){
      var show = a.textContent.toLowerCase().indexOf(term) !== -1;
      a.style.display = show ? '' : 'none';
    });
    document.querySelectorAll('#tocgroups .grp').forEach(function(g){
      var next = g.nextElementSibling, any = false;
      while (next && !next.classList.contains('grp')) {
        if (next.style.display !== 'none') any = true;
        next = next.nextElementSibling;
      }
      g.style.display = any ? '' : 'none';
    });
  });
})();
</script>
</body>
</html>
"""

HTML = (TEMPLATE.replace("__CSS__", CSS)
                .replace("__SUMARIO__", build_sumario())
                .replace("__TOC__", build_toc())
                .replace("__SECTIONS__", build_sections()))
OUT.write_text(HTML, encoding="utf-8")
print("Gerado:", OUT.name, "-", len(sections), "secoes -", len(HTML) // 1024, "KB")
