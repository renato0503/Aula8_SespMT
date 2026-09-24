# -*- coding: utf-8 -*-
"""Gerador do caderno HTML da Aula 8 - SESP/MT.
Foco: do contexto/notebooklm ao MVP no ar — prompts de exemplo,
stack técnica validada, GitHub Pages + Actions.
"""
import pathlib
OUT = pathlib.Path(r"D:\Dev\Aula Sesp\Aula 8\caderno-dia8.html")

# =================================================================
# CSS — reaproveitado do caderno da Aula 6 (mesmo design system)
# =================================================================
CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --paper:#faf9f6; --surface:#ffffff; --raised:#f3f1ec;
  --ink:#1a1d1e; --ink-soft:#4a4f52; --ink-faint:#82888c;
  --border:#ddd9d0; --accent:#1f4b8f; --verde:#2e9e6b; --ambar:#c47f00; --vermelho:#c0392b; --roxo:#7b5ea7;
  --code-bg:#1e2127; --code-ink:#abb2bf; --code-lang:#5c6370;
  --mono:'JetBrains Mono',monospace; --serif:'Source Serif 4',Georgia,serif; --sans:'Archivo',system-ui,sans-serif;
  --radius:10px; --shadow:0 2px 8px rgba(0,0,0,.08)
}
[data-theme=dark]{--paper:#171a1e;--surface:#1e2127;--raised:#252a33;--ink:#e8e6e3;--ink-soft:#9da3ae;--ink-faint:#5c6370;--border:#333842;--code-bg:#15181e;--code-ink:#abb2bf}
html{scroll-behavior:smooth}
body{margin:0;font-family:var(--sans);background:var(--paper);color:var(--ink);line-height:1.65;font-size:15px}
::selection{background:var(--accent);color:#fff}
::-webkit-scrollbar{width:6px;height:6px}::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}

header.top{background:linear-gradient(135deg,#0d2b6e 0%,#1f4b8f 55%,#2980b9 100%);color:#fff;padding:44px 24px 36px}
header.top .inner{max-width:1160px;margin:0 auto}
header.top .kicker{font-size:11.5px;text-transform:uppercase;letter-spacing:.1em;opacity:.75;display:block;margin-bottom:8px}
header.top h1{margin:0 0 10px;font-size:clamp(1.6rem,3.5vw,2.4rem);font-weight:800;line-height:1.2}
header.top .sub{opacity:.88;max-width:680px;margin:0 0 14px;font-size:14.5px;line-height:1.6}
header.top .meta{font-size:12.5px;opacity:.65;font-family:var(--mono)}

.wrap.shell{display:grid;grid-template-columns:240px 1fr;max-width:1400px;margin:0 auto;min-height:calc(100vh - 160px)}
nav.toc{position:sticky;top:0;height:100vh;overflow-y:auto;padding:20px 16px;border-right:1px solid var(--border);background:var(--raised);font-size:13px}
nav.toc input{width:100%;padding:7px 10px;border:1px solid var(--border);border-radius:7px;background:var(--surface);color:var(--ink);font-family:var(--sans);font-size:12.5px;margin-bottom:12px}
nav.toc .grp{font-size:10px;text-transform:uppercase;letter-spacing:.09em;color:var(--ink-faint);font-weight:700;margin:14px 0 4px;padding-top:10px;border-top:1px solid var(--border)}
nav.toc a{display:block;padding:3px 6px;border-radius:5px;color:var(--ink-soft);transition:background .15s}
nav.toc a:hover,nav.toc a.active{background:var(--accent);color:#fff;text-decoration:none}
main{flex:1;padding:36px 40px 60px;min-width:0}
section{margin-bottom:48px;break-inside:avoid;padding-bottom:28px;border-bottom:1px dashed var(--border)}
section:last-child{border:none}
.secnum{font-family:var(--mono);font-size:11px;color:var(--ink-faint);margin-right:8px}
h2{margin:0 0 16px;font-size:1.35rem;font-weight:700;border-left:4px solid var(--accent);padding-left:12px}
h3{margin:20px 0 8px;font-size:1.05rem;font-weight:700;color:var(--ink-soft)}
p{margin:0 0 12px}
ul,ol{margin:0 0 12px;padding-left:22px}
li{margin-bottom:4px}
code{font-family:var(--mono);font-size:.875em;background:var(--raised);padding:1px 5px;border-radius:4px}
pre{background:var(--code-bg);color:var(--code-ink);padding:14px 16px;border-radius:var(--radius);overflow:auto;font-size:13px;line-height:1.55;margin:12px 0}
pre code{background:none;padding:0}

.ficha,.callout{border-radius:var(--radius);padding:14px 16px;margin:16px 0;font-size:14px}
.ficha .lbl,.callout .lbl{font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:.08em;display:block;margin-bottom:6px}
.ficha.g{background:#eaf4ea;border-left:4px solid var(--verde)}
.ficha.g .lbl{color:var(--verde)}
.ficha.a{background:#eaf0fb;border-left:4px solid var(--accent)}
.ficha.a .lbl{color:var(--accent)}
.ficha.r{background:#fdf0ee;border-left:4px solid var(--vermelho)}
.ficha.r .lbl{color:var(--vermelho)}
.ficha.p{background:#f3eeff;border-left:4px solid var(--roxo)}
.ficha.p .lbl{color:var(--roxo)}
.callout.note{background:#eaf0fb;border-left:4px solid var(--accent)}
.callout.tip{background:#eaf4ea;border-left:4px solid var(--verde)}
.callout.err{background:#fdf0ee;border-left:4px solid var(--vermelho)}
.callout.purple{background:#f3eeff;border-left:4px solid var(--roxo)}
.callout .lbl{color:var(--ink-soft)}

.tbl{overflow-x:auto;margin:12px 0}
table{width:100%;border-collapse:collapse;font-size:13.8px}
th{text-align:left;padding:8px 12px;background:var(--raised);border-bottom:2px solid var(--border);font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-soft)}
td{padding:8px 12px;border-bottom:1px solid var(--border)}
tr:last-child td{border:none}
td.num,th.num{text-align:right;font-family:var(--mono);white-space:nowrap}

ul.f{list-style:none;margin:16px 0;padding:14px 16px;border-radius:12px;background:var(--code-bg);color:var(--code-ink);position:relative;font-family:var(--mono);font-size:13px;line-height:1.6}
ul.f li{white-space:pre;margin:0;padding:1px 0}
ul.f::before{content:attr(data-lang);position:absolute;top:8px;right:14px;font-family:var(--sans);font-size:10.5px;color:var(--code-lang);text-transform:uppercase;letter-spacing:.07em}
ul.f[data-lang]::before{content:attr(data-lang)}

ol.step{list-style:none;margin:16px 0;padding:0;counter-reset:step}
ol.step li{counter-increment:step;display:flex;flex-direction:column;gap:6px;padding:14px 16px 14px 56px;margin-bottom:10px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);position:relative;break-inside:avoid}
ol.step li::before{content:counter(step);position:absolute;left:14px;top:14px;width:30px;height:30px;background:var(--accent);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px}
ol.step li .stitle{font-weight:700;color:var(--ink)}
ol.step li .snote{font-size:13px;color:var(--ink-soft);padding-left:2px;border-left:2px solid var(--border);padding-left:10px}

.q{margin:16px 0;padding:14px 16px;background:var(--raised);border-radius:var(--radius)}
.q .stem{font-weight:600;margin-bottom:8px}
.q ol{margin:0;padding-left:20px}
.q li{padding:3px 0}
.q details{margin-top:10px;font-size:13.5px;color:var(--ink-soft)}
.q summary{cursor:pointer;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-faint)}

.aplicab{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:16px 0}
.aplicab>div{padding:12px 14px;border-radius:var(--radius);background:var(--surface);border:1px solid var(--border)}
.aplicab .lbl{font-size:10.5px;text-transform:uppercase;letter-spacing:.08em;color:var(--ink-faint);font-weight:700;display:block;margin-bottom:4px}

.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:16px 0}
.grid2 .card{padding:14px;border-radius:var(--radius);background:var(--surface);border:1px solid var(--border)}
.grid2 .card h4{margin:0 0 6px;font-size:14px}

.flow{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:16px 0}
.fnode{display:flex;flex-direction:column;align-items:center;gap:4px}
.flow .circ{width:42px;height:42px;background:var(--accent);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px}
.flow .lbl{font-size:11px;color:var(--ink-soft);text-align:center;max-width:70px}
.flow .arrow{font-size:18px;color:var(--ink-faint)}

.kpi{display:flex;flex-wrap:wrap;gap:12px;margin:16px 0}
.kpi .k{flex:1;min-width:100px;padding:14px;border-radius:var(--radius);background:var(--surface);border:1px solid var(--border);text-align:center}
.kpi .val{font-size:1.9rem;font-weight:800;color:var(--accent);font-family:var(--mono);line-height:1}
.kpi .lbl{font-size:11.5px;color:var(--ink-soft);margin-top:4px}

.btnref{display:inline-block;padding:4px 10px;background:var(--raised);border:1px solid var(--border);border-radius:6px;font-size:12.5px;font-family:var(--mono);color:var(--ink-soft)}

.uimock{border:1px solid var(--border);border-radius:12px;overflow:hidden;margin:16px 0;background:var(--surface)}
.uimock .bar{background:var(--raised);padding:8px 14px;display:flex;gap:7px;align-items:center;border-bottom:1px solid var(--border)}
.uimock .dot{width:9px;height:9px;border-radius:50%;background:var(--ink-faint);opacity:.5}
.uimock .barlabel{font-family:var(--sans);font-size:12px;color:var(--ink-faint);margin-left:6px}
.uimock .body{display:grid;grid-template-columns:44px 200px 1fr;min-height:230px}
@media(max-width:700px){.uimock .body{grid-template-columns:34px 1fr}.uimock .body .panel-side{display:none}}
.uimock .rail{background:var(--raised);border-right:1px solid var(--border);display:flex;flex-direction:column;align-items:center;padding:10px 0;gap:16px}
.uimock .rail .ico{width:22px;height:22px;border-radius:6px;background:var(--border)}
.uimock .rail .ico.on{background:var(--accent)}
.uimock .panel-side{background:var(--surface);border-right:1px solid var(--border);padding:12px}
.uimock .panel-side .ttl{font-family:var(--sans);font-weight:700;font-size:12.5px;margin-bottom:8px;color:var(--ink-faint);text-transform:uppercase;letter-spacing:.05em}
.uimock .fileline{font-family:var(--mono);font-size:12.6px;padding:3px 6px;border-radius:5px;color:var(--ink-soft)}
.uimock .fileline.mod{color:var(--ambar)}
.uimock .fileline.new{color:var(--verde)}
.uimock .canvas{padding:16px}
.actbar{display:flex;flex-wrap:wrap;gap:0;border:1px solid var(--border);border-radius:12px;overflow:hidden;margin:16px 0;background:var(--surface)}
.actbar .rail2{background:var(--code-bg);padding:18px 22px 18px 14px;display:flex;flex-direction:column;gap:13px;align-items:flex-start}
.actbar .rail2 .aicon{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;background:rgba(255,255,255,.07);position:relative;color:#e6e6e6}
.actbar .rail2 .aicon.on{background:var(--accent)}
.actbar .rail2 .aicon .num{position:absolute;left:-18px;top:50%;transform:translateY(-50%);font-family:var(--mono);font-size:10.5px;color:#9aa0a6}
.actbar .legend{flex:1 1 280px;padding:14px 18px;font-family:var(--sans);font-size:13.2px;min-width:240px}
.actbar .legend .li{display:flex;gap:10px;padding:6px 0;border-bottom:1px dashed var(--border)}
.actbar .legend .li:last-child{border:none}
.actbar .legend .li .n{min-width:20px;font-family:var(--mono);color:var(--accent);font-weight:700}
.actbar .legend .li b{display:block}
.actbar .legend .li span.d{color:var(--ink-soft);font-size:12.6px}
.welcomemock{padding:30px 20px;text-align:center}
.welcomemock .wlogo{font-size:30px;margin-bottom:6px}
.welcomemock .wtitle{font-family:var(--sans);font-weight:700;font-size:17px;margin-bottom:20px}
.welcomemock .wbtns{display:flex;flex-direction:column;gap:10px;max-width:260px;margin:0 auto}
.welcomemock .wbtn{padding:10px 16px;border-radius:8px;border:1px solid var(--border);font-family:var(--sans);font-size:13.6px;font-weight:600;text-align:left}
.welcomemock .wbtn.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
.welcomemock .wspaces{text-align:left;max-width:300px;margin:26px auto 0}
.welcomemock .wlbl{font-family:var(--sans);font-size:10.8px;color:var(--ink-faint);text-transform:uppercase;letter-spacing:.07em;margin-bottom:8px}
.welcomemock .wsitem{font-family:var(--sans);font-size:13px;padding:6px 10px;border-radius:7px;color:var(--ink-soft);border:1px solid var(--border);margin-bottom:6px}
.welcomemock .wsitem small{display:block;font-size:11px;color:var(--ink-faint)}
.agentmock{display:flex;flex-direction:column;min-height:270px}
.agentmock .ahead{background:var(--raised);padding:8px 14px;display:flex;justify-content:space-between;align-items:center;font-family:var(--sans);font-size:12.5px;font-weight:600;border-bottom:1px solid var(--border)}
.agentmock .ahead .aicons{color:var(--ink-faint);font-size:13px;display:flex;gap:8px}
.agentmock .abody{flex:1;padding:16px;display:flex;flex-direction:column;gap:12px}
.agentmock .alogo{font-size:28px}
.agentmock .aname{font-family:var(--sans);font-size:14px;font-weight:700}
.agentmock .ainput{border:1px solid var(--border);border-radius:8px;overflow:hidden}
.agentmock .ph{padding:8px 12px;font-size:12.5px;color:var(--ink-faint);background:var(--surface)}
.agentmock .arow{display:flex;justify-content:space-between;align-items:center;padding:7px 12px;background:var(--raised);font-size:12px;color:var(--ink-soft)}
.agentmock .adisc{padding:0 4px;font-size:11.5px;color:var(--ink-faint);line-height:1.5}
.lab{border:1px solid var(--border);border-radius:var(--radius);padding:18px;margin:16px 0;background:var(--surface)}
.lab-title{font-weight:700;font-size:1rem;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.lab-title::before{content:'LAB';font-size:10px;background:var(--verde);color:#fff;padding:2px 7px;border-radius:5px;letter-spacing:.06em}
.passolab{display:flex;gap:14px;margin:14px 0;padding:12px 14px;background:var(--raised);border-radius:var(--radius);font-size:14px}
.passolab .pnum{font-family:var(--mono);font-size:18px;font-weight:700;color:var(--accent);flex-shrink:0;line-height:1.2}
.passolab .ptitle{font-weight:700;margin-bottom:4px}
.passolab .pbody{color:var(--ink-soft);font-size:13.5px}
.cenario{border-left:4px solid var(--ambar);padding:14px 16px;margin:16px 0;background:#fffdf5;border-radius:0 var(--radius) var(--radius) 0}
.cenario-title{font-weight:700;font-size:.95rem;margin-bottom:10px;color:var(--ambar)}
.vcard{border:1px solid var(--border);border-radius:var(--radius);padding:14px;margin:8px 0;display:flex;gap:14px;align-items:flex-start}
.vcard-icon{font-size:26px;flex-shrink:0;line-height:1}
.vcard h4{margin:0 0 4px;font-size:14px}
.vcard p{margin:0;font-size:13.5px;color:var(--ink-soft)}
dl.glossary{margin:12px 0}
dl.glossary dt{font-weight:700;color:var(--accent);font-family:var(--mono);font-size:13px}
dl.glossary dd{margin:0 0 8px 16px;font-size:14px;color:var(--ink-soft)}
@media print{.themebtn,.pdfbtn,nav.toc{display:none}.wrap.shell{grid-template-columns:1fr;display:block}main section{break-inside:avoid;box-shadow:none}section{padding-bottom:20px}}
footer.pagefoot{max-width:1160px;margin:0 auto;padding:0 24px 60px;color:var(--ink-faint);font-family:var(--sans);font-size:12.5px;text-align:center}
"""

# =================================================================
# HELPERS
# =================================================================
def p(txt): return f"<p>{txt}</p>"
def h3(txt): return f"<h3>{txt}</h3>"
def ficha(kind, label, body): return f'<div class="ficha {kind}"><b class="lbl">{label}</b>{body}</div>'
def callout(kind, label, body): return f'<div class="callout {kind}"><b class="lbl">{label}</b>{body}</div>'
def tbl(headers, rows, num_cols=None):
    num_cols = num_cols or []
    th = "".join(f'<th class="{"num" if i in num_cols else ""}">{h}</th>' for i, h in enumerate(headers))
    trs = ""
    for r in rows:
        tds = "".join(f'<td class="{"num" if i in num_cols else ""}">{c}</td>' for i, c in enumerate(r))
        trs += f"<tr>{tds}</tr>"
    return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'
def code(lines, lang="bash"):
    html_lines = ""
    for ln in lines: html_lines += f"<li>{ln}</li>"
    return f'<ul class="f" data-lang="{lang}">{html_lines}</ul>'
def step(items):
    out = "<ol class='step'>"
    for it in items:
        titulo, acao = it[0], it[1]
        nota = it[2] if len(it) > 2 else ""
        out += f"<li><div class='stitle'>{titulo}</div><div>{acao}</div>"
        if nota: out += f"<div class='snote'>{nota}</div>"
        out += "</li>"
    out += "</ol>"
    return out
def q(stem, options, ans_idx, hint=""):
    opts = "".join(f"<li>{o}</li>" for o in options)
    ans = options[ans_idx]
    hint_html = f"<p style='margin-top:6px;color:var(--ink-faint);font-size:13.6px'>{hint}</p>" if hint else ""
    return (f'<div class="q"><div class="stem">{stem}</div><ol>{opts}</ol>'
            f'<details><summary>Ver resposta</summary><p><b>{ans}</b></p>{hint_html}</details></div>')
def aplicab(quando, porque, exemplo):
    return (f'<div class="aplicab"><div><div class="lbl">Quando usar</div>{quando}</div>'
            f'<div><div class="lbl">Por que</div>{porque}</div>'
            f'<div><div class="lbl">Exemplo real</div>{exemplo}</div></div>')
def grid2(cards):
    out = '<div class="grid2">'
    for titulo, body in cards: out += f'<div class="card"><h4>{titulo}</h4>{body}</div>'
    out += '</div>'
    return out
def flow_h(nodes):
    out = '<div class="flow">'
    for i, (emo, lbl) in enumerate(nodes):
        out += f'<div class="fnode"><div class="circ">{emo}</div><div class="lbl">{lbl}</div></div>'
        if i < len(nodes) - 1: out += '<div class="arrow">\u27a4</div>'
    out += '</div>'
    return out
def kpi(items):
    out = '<div class="kpi">'
    for v, l in items: out += f'<div class="k"><div class="val">{v}</div><div class="lbl">{l}</div></div>'
    out += '</div>'
    return out
def btn(txt): return f'<span class="btnref">{txt}</span>'
def ui_welcome(): return (f'<div class="uimock"><div class="bar"><div class="dot"></div><div class="dot"></div>'
    f'<div class="dot"></div><span class="barlabel">Antigravity IDE \u2014 tela inicial</span></div>'
    f'<div class="welcomemock"><div class="wlogo">\U0001f5a5</div><div class="wtitle">Antigravity IDE</div>'
    f'<div class="wbtns"><div class="wbtn primary">\U0001f4c1&nbsp;&nbsp;Open Folder</div>'
    f'<div class="wbtn">\U0001f517&nbsp;&nbsp;Clone Repository</div></div>'
    f'<div class="wspaces"><div class="wlbl">Workspaces</div>'
    f'<div class="wsitem">contexto.md &amp; sprint.md<small>Aula 8</small></div>'
    f'<div class="wsitem">mvp-pedidos-sesp<small>D:\\Dev</small></div></div></div></div>')
def ui_agent(): return (f'<div class="uimock"><div class="bar"><div class="dot"></div><div class="dot"></div>'
    f'<div class="dot"></div><span class="barlabel">Painel Agent</span></div>'
    f'<div class="agentmock"><div class="ahead">Agent<span class="aicons">+ \U0001f559 \u22ef \u2715</span></div>'
    f'<div class="abody"><div class="alogo">\U0001f916</div><div class="aname">Antigravity Agent</div>'
    f'<div class="ainput"><div class="ph">Ask anything, @ to mention, / for actions</div>'
    f'<div class="arow"><span>GPT-OSS 120B (Medium) \u25be</span><span>\u27a4</span></div></div>'
    f'<div class="adisc">AI may make mistakes. Double-check all generated code.</div></div></div>')
def glossary(items):
    dl = "<dl class='glossary'>"
    for term, defi in items: dl += f"<dt>{term}</dt><dd>{defi}</dd>"
    dl += "</dl>"
    return dl
def lab(title, body): return f'<div class="lab"><div class="lab-title">{title}</div>{body}</div>'
def passolab(num, title, body): return f'<div class="passolab"><div class="pnum">{num}</div><div><div class="ptitle">{title}</div><div class="pbody">{body}</div></div></div>'
def cenario(title, body): return f'<div class="cenario"><div class="cenario-title">{title}</div>{body}</div>'
def vcard(icon, title, body): return f'<div class="vcard"><div class="vcard-icon">{icon}</div><div><h4>{title}</h4>{body}</div></div>'

# =================================================================
# ESTADO / TOC
# =================================================================
sections = []
toc_groups = []
cur_group, cur_items = None, []

def grp(titulo):
    global cur_group, cur_items
    if cur_group: toc_groups.append((cur_group, cur_items))
    cur_group, cur_items = titulo, []
def section(anchor, titulo, body_html):
    sections.append((anchor, titulo, body_html))
    cur_items.append((anchor, titulo))

# =================================================================
# SEÇÕES DO CADERNO
# =================================================================
grp("Abertura")
section("agenda", "Agenda do Dia 8 — Do NotebookLM ao MVP no Ar",
    p("Hoje é o dia em que o projeto sai do papel e começa a virar código. "
      "Você vai aprender a transformar o contexto e as sprints que o NotebookLM "
      "gerou em um MVP funcional, hospedado no GitHub Pages — tudo em TypeScript, "
      "com PWA e testes automatizados.") +
    tbl(["Bloco", "O que vamos fazer"],
        [["Manhã (08h–12h)", "Validar os prompts do NotebookLM · Configurar o projeto no Antigravity · Escrever as primeiras linhas de código do MVP"],
         ["Tarde (13h–17h)", "Publicar no GitHub · Configurar deploy automático · Próximos passos e prompts para cada sprint"]],
        num_cols=[])
)

section("checklist-confirmacao", "Checklist: você trouxe tudo?",
    step([
        ("Contexto importado do NotebookLM", "Abra o <b>contexto.md</b> que você gerou no NotebookLM e tenha-o visível no Antigravity (abra como arquivo)."),
        ("Sprints definidas no NotebookLM", "Abra o <b>sprint.md</b> com as sprints técnicas em JS/TS/Python PWA. Ele é o seu roteiro de execução."),
        ("Conta no GitHub", "Você precisa de uma conta em <b>github.com</b>. Sem ela não é possível publicar."),
        ("Antigravity conectado ao GitHub", "Se ainda não conectou, volte ao caderno do Dia 6 e siga a seção 'Conectar GitHub'.")
    ]) +
    callout("tip", "Dica", "Se você não tem certeza se o Antigravity está conectado ao GitHub, clique no ícone do painel de Controle do Código-Fonte (escaneie o QR code visual) e veja se aparece o nome do seu repositório.")
)

# ─── PARTE 1 ─────────────────────────────────────────────────────────────────
grp("Parte 1 · Do NotebookLM ao Antigravity")

section("prompt-contexto-melhorado", "O Prompt de Contexto — Versão Técnica Aprimorada",
    p("O prompt que você usou no NotebookLM provavelmente gerou um resumo amplo. "
      "Agora vamos torná-lo mais preciso para extrair informações que o agente de IA "
      "consegue transformar diretamente em código.") +
    callout("note", "Prompt melhorado para contexto", "Copie e cole no NotebookLM (nova conversa) para gerar um contexto mais técnico e estruturado:") +
    code(["Análise de Requisitos Técnicos — MVP", "", "# Contexto do Projeto", "# O problema que o sistema resolve", "# Personas principais e suas necessidades", "# Dados que o sistema manipula (entidades e campos)", "# Regras de negócio críticas", "# Interfaces principais (telas e fluxos)", "# Integração com sistemas externos", "# Requisitos não-funcionais (performance, segurança, acessibilidade)", "", "# Formato de saída", "Responda em português. Para cada seção, seja específico: nomes de entidades,", "tipos de dados, validações e critérios de aceite mensuráveis.", "Evite descrições vagas. Prefira tabelas e listas a parágrafos."], "txt") +
    callout("tip", "Por que recarregar?", "O NotebookLM original pode ter perdido o thread da conversa. "
      "Uma nova conversa com um prompt mais técnico gera um contexto mais útil para o agente de IA.")
)

section("prompt-sprints-melhorado", "O Prompt de Sprints — Versão Técnica com GitHub Pages",
    p("O sprint.md original pediu sprints em JS/TS/Python PWA. Vamos aprimorar para que "
      "cada sprint inclua também o target de publicação no GitHub Pages e a estrutura de branches.") +
    callout("note", "Prompt melhorado para sprints", "Cole no NotebookLM (mesma conversa do contexto, ou nova):") +
    code(['Gere sprints de execução técnica para o MVP com as seguintes características:', '', 'Stack: TypeScript (Vite) + JavaScript + Python (PWA com service worker)', 'Hospedagem: GitHub Pages (subcaminho /nome-do-repo/)', 'Versionamento: Git com branches (main + feature/*)', '', 'Formato para cada sprint:', '1. Nome e objetivo principal', '2. Entregas técnicas específicas (arquivos que serão criados/modificados)', '3. Critério de aceite (o que precisa estar funcionando ao final)', '4. Branch Git associada (ex: feature/setup-inicial)', '5. Target de deploy (ex: https://usuario.github.io/nome-repo/)', '', 'Considere: autenticação básica, CRUD de entidades principais,', 'dados sintéticos para mock, testes unitários com Vitest,'], "txt")
)

section("o-que-e-mvp", "O que é um MVP e por que PWA?",
    aplicab(
        "Quando você precisa validar uma ideia com dados reais e usuários de verdade, sem gastar meses em desenvolvimento.",
        "Um MVP (Minimum Viable Product) é a menor versão de um produto que entrega valor real. PWA (Progressive Web App) permite que rodem como app no celular sem passar por loja de aplicativos.",
        "O Portal de Pedidos de Compra da SESP: o MVP mostra os pedidos por status, com filtros e totais, em uma URL que qualquer servidor acessa pelo celular."
    ) +
    kpi([
        ("< 2 sem", "para subir o MVP"),
        ("PWA", "roda offline + home screen"),
        ("GitHub Pages", "hostagem gratuita"),
        ("Vitest", "testes em ms"),
    ])
)

# ─── PARTE 2 ─────────────────────────────────────────────────────────────────
grp("Parte 2 · A stack técnica — validada e explicada")

section("stack-escolhida", "A stack do MVP: por que cada peça?",
    tbl(["Tecnologia", "Papel no MVP", "Alternativa"],
        [["Vite (vanilla-ts)", "Build tool e dev server. Compila TS → JS e empacota para o navegador.", "webpack, parcel"],
         ["TypeScript", "Superconjunto de JS com tipos. Reduz erros em tempo de desenvolvimento.", "JS puro"],
         ["Vitest", "Framework de testes unitários. Roda no Node, rápido (subsegundo).", "Jest, Mocha"],
         ["vite-plugin-pwa", "Gera service worker, manifesto e ícones PWA automaticamente.", "workbox manual"],
         ["Python (scripts)", "Gera dados sintéticos (faker) e executa checks de LGPD.", "Nodefaker, chance"],
         ["GitHub Actions", "CI/CD: testa, compila e publica no GitHub Pages a cada push.", "CircleCI, Travis"]],
        num_cols=[0])
)

section("arquitetura-pwa", "Arquitetura do projeto — como tudo se conecta",
    flow_h([
        ("📄", "contexto.md\nsprint.md"), ("\u27a4", ""),
        ("🤖", "Antigravity\nAgent"), ("\u27a4", ""),
        ("📁", "src/\ndomain/"), ("\u27a4", ""),
        ("⚙️", "Vite\nbuild"), ("\u27a4", ""),
        ("🌐", "GitHub\nPages"),
    ]) +
    tbl(["Camada", "O que fica aqui", "Arquivos典型icos"],
        [["Dados", "JSON estático em public/data/. Gere com script Python.", "pedidos.json, usuarios.json"],
         ["Domínio", "Regras de negócio puras, sem dependência de framework.", "regras.ts, entidades.ts"],
         ["Serviços", "Chamadas à API (fetch), autenticação.", "api.ts, auth.ts"],
         ["UI", "Componentes de apresentação, rotas (hash-based).", "main.ts, dashboard.ts"],
         ["Infraestrutura", "Config de build, CI/CD, manifesto PWA.", "vite.config.ts, .github/workflows/"],
         ["Scripts", "Geração de dados sintéticos, verificações LGPD.", "scripts/gerar_dados.py"]],
        num_cols=[])
)

section("branch-model", "Modelo de branches — o fluxo Git que você vai seguir",
    callout("note", "Regra de ouro", "Cada sprint = uma branch feature. O merge na main só acontece após testes verdes no CI.") +
    flow_h([
        ("⬛", "main\n(produção)"),
        ("\u27a4", ""), ("🟢", "feature/\nsetup-inicial"),
        ("\u27a4", ""), ("🟡", "feature/\ndados-sinteticos"),
        ("\u27a4", ""), ("🔵", "feature/\ncrud-pedidos"),
        ("\u27a4", ""), ("🟣", "feature/\npwa-offline"),
        ("\u27a4", ""), ("⬛", "main\n(deploy)"),
    ]) +
    glossary([
        ("main", "Branch principal. Código que está em produção (no ar no GitHub Pages). Só recebe merge quando tudo está testado."),
        ("feature/*", "Branch para cada sprint. Ex: feature/setup-inicial, feature/crud-pedidos. Criada a partir da main."),
        ("workflow_dispatch", "Gatilho manual no GitHub Actions. Permite publicar mesmo sem push, usando o botão 'Run workflow'."),
    ])
)

# ─── PARTE 3 ─────────────────────────────────────────────────────────────────
grp("Parte 3 · Setup do projeto — passo a passo completo")

section("passo-criar-repositorio", "Passo 1 — Criar o repositório no GitHub",
    step([
        ("Acesse github.com/new", "Clique em <b>New repository</b>. Dê um nome curto e claro (ex: <code>mvp-pedidos-sesp</code>). Marque <b>Public</b> para ativar GitHub Pages gratuito."),
        ("Não inicialize", "Deixe todas as caixinhas de 'Add README', '.gitignore', etc. deschecadas. Vamos preencher na mão."),
        ("Copie a URL do repositório", "Guarde a URL HTTPS (ex: <code>https://github.com/seu-usuario/mvp-pedidos-sesp.git</code>) — você vai usá-la no Antigravity."),
    ]) +
    callout("tip", "Nome do repo = base path", "Se o repo se chama <code>mvp-pedidos-sesp</code>, a URL do site será "
      "<code>https://seu-usuario.github.io/mvp-pedidos-sesp/</code>. Anote o nome — você vai precisar dele no <code>vite.config.ts</code>.")
)

section("passo-scaffold", "Passo 2 — Scaffold do projeto (sem perder seus arquivos)",
    callout("r", "Atenção — pasta não vazia?", "Se a sua pasta já tem <code>contexto.md</code> e <code>sprint.md</code>, o Vite vai recusar criar o projeto nela. "
      "Siga o caminho alternativo abaixo.") +
    lab("Caminho normal (pasta vazia)", step([
        ("Crie o projeto", "No terminal (PowerShell) dentro da pasta do projeto:",
         "npm create vite@latest . -- --template vanilla-ts --overwrite"),
        ("Instale dependências", "npm install"),
        ("Instale os plugins PWA e testes", "npm i -D vite-plugin-pwa vitest"),
        ("Gere ícones PWA", "npm i -D @vite-pwa/assets-generator\nnpx pwa-assets-generator --preset minimal-2023 public/icon.svg"),
    ])) +
    lab("Caminho alternativo (pasta com contexto.md e sprint.md)", step([
        ("Crie em uma subpasta temporária", "cd ..\nnpm create vite@latest mvp-temp -- --template vanilla-ts\nmv mvp-temp/* mvp-temp/.* . 2>/dev/null; rmdir mvp-temp"),
        ("Mova seus arquivos de contexto", "Os arquivos <code>contexto.md</code> e <code>sprint.md</code> precisam existir. Se foram movidos, traga-os de volta."),
        ("Instale as dependências", "npm install\nnpm i -D vite-plugin-pwa vitest @vite-pwa/assets-generator"),
    ]))
)

section("passo-config-vite", "Passo 3 — Configurar o vite.config.ts",
    p("O <code>vite.config.ts</code> é o arquivo mais importante do projeto. "
      "Ele define o caminho base (o nome do seu repo) e ativa o PWA.") +
    code(["import { defineConfig } from 'vite'", "import { VitePWA } from 'vite-plugin-pwa'", "", "// \u270f  TROQUE PELO NOME DO SEU REPOSIT\u00d3RIO NO GITHUB", "const REPO = 'mvp-pedidos-sesp'", "", "export default defineConfig({",
         "  base: `/${REPO}/`,", "  plugins: [",
         "    VitePWA({", "      registerType: 'autoUpdate',",
         "      includeAssets: ['favicon.ico', 'apple-touch-icon-180x180.png'],",
         "      manifest: {",
         "        name: 'Portal de Pedidos \u2014 SESP/MT (MVP)',",
         "        short_name: 'Pedidos SESP',",
         "        description: 'MVP acad\u00eamico com dados sint\u00e9ticos \u2014 Curso SESP/MT',",
         "        lang: 'pt-BR',",
         "        theme_color: '#1f4b8f',",
         "        background_color: '#ffffff',",
         "        display: 'standalone',",
         "        start_url: '.',",
         "        scope: '.',",
         "        icons: [",
         "          { src: 'pwa-64x64.png', sizes: '64x64', type: 'image/png' },",
         "          { src: 'pwa-192x192.png', sizes: '192x192', type: 'image/png' },",
         "          { src: 'pwa-512x512.png', sizes: '512x512', type: 'image/png' },",
         "          { src: 'maskable-icon-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },",
         "        ],",
         "      },", "      workbox: { globPatterns: ['**/*.{js,css,html,svg,png,ico,json}'] },",
         "    }),", "  ],", "})"], "ts") +
    callout("err", "Erro mais comum", "Esquecer de trocar <code>REPO</code> faz o site abrir em branco no GitHub Pages. "
      "O caminho base precisa ser <b>exatamente</b> o nome do repositório.")
)

section("passo-config-scripts", "Passo 4 — Scripts npm e arquivo de ícone",
    p("Adicione os scripts de teste e geração de ícones ao <code>package.json</code>:") +
    code(["npm pkg set scripts.test='vitest run'", "npm pkg set scripts.icones='pwa-assets-generator --preset minimal-2023 public/icon.svg'"], "bash") +
    p("Crie o ícone SVG na pasta <code>public/</code> (exemplo com as iniciais do seu projeto):") +
    code(['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">',
         '<rect width="512" height="512" rx="96" fill="#1f4b8f"/>',
         '<text x="256" y="330" font-family="Arial" font-size="220" font-weight="700" fill="#fff" text-anchor="middle">PC</text>',
         '</svg>'], "xml") +
    p("Salve como <code>public/icon.svg</code>. Depois execute:") +
    code(["npm run icones"], "bash")
)

# ─── PARTE 4 ─────────────────────────────────────────────────────────────────
grp("Parte 4 · Estrutura de código e dados sintéticos")

section("estrutura-src", "Passo 5 — A estrutura de pastas src/",
    callout("note", "Regra结构性", "A pasta <code>src/</code> só tem código que roda no navegador. "
      "Dados estáticos vão sempre em <code>public/data/</code>. Scripts Python ficam em <code>scripts/</code>.") +
    code(["src/", "  domain/", "    regras.ts          # regras de neg\u00f3cio puras", "    regras.test.ts      # testes das regras",
         "    entidades.ts        # interfaces TypeScript",
         "  auth/", "    Papeis.ts             # Roles e permiss\u00f5es",
         "    auth.test.ts",
         "  services/", "    api.ts               # chamadas \u00e0 API (fetch)",
         "  main.ts              # ponto de entrada + router hash",
         "public/",
         "  data/", "    pedidos.json          # dados sint\u00e9ticos (gerados pelo Python)",
         "  icon.svg",
         "  pwa-*.png             # \u00edcones gerados",
         "scripts/",
         "  gerar_dados.py        # faker + verifica\u00e7\u00e3o LGPD",
         "  test_gerar_dados.py  # pytest"], "bash")
)

section("script-python-dados", "Passo 6 — Gerar dados sintéticos com verificação LGPD",
    p("O script Python cria dados realistas para o MVP. Ele mascara CPFs automaticamente "
      "e é executado tanto localmente quanto no CI do GitHub Actions.") +
    code(['"""Gera dados SINT\u00c9TICOS para o MVP. Nenhum dado real da SESP.\nCPF sempre mascarado antes de sair daqui (LGPD)."""',
         "import json, pathlib, random",
         "from datetime import date, timedelta",
         "from typing import NamedTuple",
         "",
         "random.seed(42)  # reprodut\u00edvel",
         "SAIDA = pathlib.Path(__file__).resolve().parent.parent / 'public' / 'data'",
         "SAIDA.mkdir(parents=True, exist_ok=True)",
         "",
         "UNIDADES = ['Setor de Compras', 'Controladoria', 'Gabinete', 'DIRETORIA de TI']",
         "STATUS = ['rascunho', 'enviado', 'em_cotacao', 'em_auditoria', 'aprovado', 'devolvido']",
         "",
         "def mascara_cpf(cpf: str) -> str:",
         "    return f\'***.{cpf[3:6]}.***-**\'",
         "",
         "pedidos = []",
         "for i in range(1, 121):",
         "    pedidos.append({",
         "        'id': i,",
         "        'protocolo': f\'PC-2026-{i:04d}\',",
         "        'unidade': random.choice(UNIDADES),",
         "        'solicitante_cpf': mascara_cpf(gerar_cpf_valido()),",
         "        'valor_estimado': round(random.uniform(800, 95_000), 2),",
         "        'status': random.choice(STATUS),",
         "        'aberto_em': (date(2026, 1, 2) + timedelta(days=random.randint(0, 240))).isoformat(),",
         "    })",
         "(SAIDA / 'pedidos.json').write_text(json.dumps(pedidos, ensure_ascii=False, indent=2))",
         "print(f\'OK: {len(pedidos)} pedidos em {SAIDA}\')"], "python") +
    callout("tip", "pytest no CI", "O workflow do GitHub Actions executa <code>python -m pytest -q scripts</code> "
      "para garantir que nenhum CPF foi exposto no JSON gerado.")
)

section("codigo-dominio", "Passo 7 — Regras de negócio em TypeScript (domínio puro)",
    code(["export interface Pedido {", "  id: number",
         "  protocolo: string", "  unidade: string",
         "  solicitante_cpf: string", "  valor_estimado: number",
         "  status: 'rascunho' | 'enviado' | 'em_cotacao' | 'em_auditoria' | 'aprovado' | 'devolvido'",
         "  aberto_em: string", "}",
         "", "/** Valor acima do qual o pedido exige auditoria da Controladoria */",
         "export const LIMITE_AUDITORIA = 50_000",
         "",
         "export function exigeAuditoria(pedido: Pedido): boolean {",
         "  return pedido.valor_estimado > LIMITE_AUDITORIA",
         "}",
         "",
         "export function totalPorStatus(pedidos: Pedido[]): Record<string, number> {",
         "  return pedidos.reduce<Record<string, number>>((acc, p) => {",
         "    acc[p.status] = (acc[p.status] ?? 0) + 1",
         "    return acc",
         "  }, {})",
         "}"], "ts") +
    callout("note", "Por que domínio separado?", "Isolar as regras permite testar sem precisar de um navegador, "
      "um servidor ou dados reais. Qualquer pessoa da equipe consegue rodar <code>npm test</code> e verificar se as regras estão corretas.")
)

section("testes-vitest", "Passo 8 — Testes unitários com Vitest",
    p("Os testes validam as regras de negócio em milissegundos, sem precisar abrir o navegador. "
      "O CI do GitHub Actions exige que todos os testes passem antes de publicar.") +
    code(["import { describe, it, expect } from 'vitest'", "import { exigeAuditoria, totalPorStatus, type Pedido } from './regras'",
         "", "const base: Pedido = { id: 1, protocolo: 'PC-2026-0001', unidade: 'Compras',",
         "  solicitante_cpf: '***.123.***-**', valor_estimado: 1000,",
         "  status: 'enviado', aberto_em: '2026-03-01',", "}",
         "", "describe('regras de neg\u00f3cio', () => {",
         "  it('pedido acima de R$ 50 mil exige auditoria', () => {",
         "    expect(exigeAuditoria({ ...base, valor_estimado: 50_000.01 })).toBe(true)",
         "    expect(exigeAuditoria({ ...base, valor_estimado: 50_000 })).toBe(false)",
         "  })",
         "  it('conta pedidos por status', () => {",
         "    const r = totalPorStatus([base, base, { ...base, status: 'aprovado' }])",
         "    expect(r).toEqual({ enviado: 2, aprovado: 1 })",
         "  })",
         "})"], "ts") +
    code(["npm test"], "bash") +
    callout("tip", "O que falha no CI?", "Se qualquer teste falhar, o GitHub Actions impede o deploy. "
      "Isso protege você de publicar código quebrado no ar.")
)

# ─── PARTE 5 ─────────────────────────────────────────────────────────────────
grp("Parte 5 · GitHub Actions — deploy automático")

section("workflow-deploy", "Passo 9 — O workflow .github/workflows/deploy.yml",
    p("O workflow é o 'fio terra' entre o seu código e o site no ar. "
      "A cada push na branch <code>main</code>, ele executa: Python (dados + pytest) → Node (testes + build) → GitHub Pages.") +
    code(["name: Deploy no GitHub Pages", "", "on:", "  push:", "    branches: [main]",
         "  workflow_dispatch:", "  # permite acionar manualmente na aba Actions", "",
         "permissions:", "  contents: read", "  pages: write", "  id-token: write", "",
         "concurrency:", "  group: pages", "  cancel-in-progress: true", "",
         "jobs:", "  build:", "    runs-on: ubuntu-latest",
         "    steps:", "      - uses: actions/checkout@v7",
         "",
         "      - name: Python \u2014 gerar dados e verificar LGPD",
         "        uses: actions/setup-python@v7",
         "        with: { python-version: '3.12' }",
         "      - run: pip install -r requirements.txt",
         "      - run: python scripts/gerar_dados.py",
         "      - run: python -m pytest -q scripts",
         "",
         "      - name: Node \u2014 instalar, testar e compilar",
         "        uses: actions/setup-node@v7",
         "        with: { node-version: '22' }",
         "      - run: npm ci",
         "      - run: npm test",
         "      - run: npm run build",
         "",
         "      - uses: actions/configure-pages@v6",
         "      - uses: actions/upload-pages-artifact@v5",
         "        with: { path: dist }",
         "",
         "  deploy:", "    needs: build",
         "    runs-on: ubuntu-latest",
         "    environment:",
         "      name: github-pages",
         "      url: ${{ steps.deployment.outputs.page_url }}",
         "    steps:",
         "      - id: deployment",
         "        uses: actions/deploy-pages@v5"], "yaml")
)

section("ativar-github-pages", "Passo 10 — Ativar GitHub Pages no repositório",
    step([
        ("Configurar no GitHub", "No seu repositório, vá em <b>Settings → Pages → Source</b> e selecione <b>GitHub Actions</b>. Não é mais necessário escolher branch — o workflow controla isso."),
        ("Adicionar requirements.txt", "Crie um arquivo <code>requirements.txt</code> na raiz do projeto com apenas: <code>pytest</code> (sem versão, para pegar a última)."),
    ]) +
    callout("tip", "workflow_dispatch", "Com esse gatilho, você pode acionar o deploy manualmente "
      "pela aba <b>Actions</b> do repositório, sem precisar dar push. Útil quando você quer verificar "
      "o build antes de abrir uma PR.")
)

section("primeiro-deploy", "Passo 11 — Seu primeiro deploy",
    step([
        ("Commit e push iniciais", "No Antigravity, painel Git: Stage All → Commit (mensagem: 'feat: setup inicial do MVP') → Push."),
        ("Acompanhe o Actions", "Acesse a aba <b>Actions</b> do repositório. Você verá o workflow rodando: amarela (running) → verde (sucesso)."),
        ("Acesse o site", "Quando o job 'deploy' terminar, o link aparecerá em <b>Settings → Pages</b>: <code>https://seu-usuario.github.io/mvp-pedidos-sesp/</code>."),
    ]) +
    callout("note", "Tempo de propagação", "Pode levar até 2 minutos para o site aparecer após o deploy terminar. "
      "Se der erro 404, aguarde e recarregue. Se persistir por mais de 5 minutos, verifique o log do Actions.")
)

# ─── PARTE 6 ─────────────────────────────────────────────────────────────────
grp("Parte 6 · Prompts de exemplo — um para cada sprint do MVP")

section("prompts-sprint0", "Sprint 0 (Setup) — Prompts para o agente",
    callout("note", "Como usar", "Cole cada prompt no painel Agent do Antigravity. "
      "Substitua os termos entre colchetes pelo que faz sentido para o seu projeto específico.") +
    ficha("g", "Prompt A — Configurar o projeto do zero",
      '<code>Crie uma estrutura de projeto Vite com vanilla TypeScript. Instale e configure o plugin PWA (vite-plugin-pwa) com manifest para PWA instalável. Configure o base path como "/nome-do-repo/" (substitua pelo nome real). Adicione Vitest como dependência de desenvolvimento.</code>') +
    ficha("a", "Prompt B — Gerar o ícone e ícones PWA",
      '<code>Usando a ferramenta pwa-assets-generator com preset minimal-2023, gere todos os ícones PWA (64x64, 192x192, 512x512 e maskable) a partir do arquivo public/icon.svg.</code>') +
    ficha("p", "Prompt C — Primeira estrutura de arquivos",
      '<code>Crie a seguinte estrutura de pastas dentro de src/: domain/ (com entidades.ts e regras.ts), auth/ (com Papeis.ts e uma função pode(acao, papel)), services/ (com api.ts usando fetch e BASE_URL do import.meta.env). Para o campo status use union type literal.</code>')
)

section("prompts-sprint1", "Sprint 1 (Dados) — Prompts para o agente",
    ficha("g", "Prompt A — Script Python de dados sintéticos",
      '<code>Escreva um script Python completo em scripts/gerar_dados.py que: (1) use pathlib e json da stdlib; (2) use random com seed 42 para reprodutibilidade; (3) gere 120 pedidos com campos: id, protocolo (formato PC-2026-XXXX), unidade (escolha entre 5 opções), solicitante_cpf (gere CPF válido e aplique máscara ***.XXX.***-**), valor_estimado (entre 800 e 95000), status (escolha aleatório entre 6 opções), aberto_em (data entre 2026-01-02 e 2026-09-01); (4) grave em public/data/pedidos.json com indent=2 e ensure_ascii=False.</code>') +
    ficha("a", "Prompt B — Teste de segurança LGPD",
      '<code>Escreva um teste pytest em scripts/test_gerar_dados.py que: (1) execute o script gerar_dados.py via subprocess; (2) leia o arquivo public/data/pedidos.json; (3) verifique com regex que nenhum CPF completo (formato XXX.XXX.XXX-XX) está presente no arquivo; (4) afirme que o JSON contém exatamente 120 registros.</code>') +
    ficha("p", "Prompt C — Interface TypeScript da entidade",
      '<code>Com base nos dados do JSON, escreva a interface TypeScript Pedido em src/domain/entidades.ts com todos os campos e seus tipos exatos. Em src/domain/regras.ts escreva: LIMITE_AUDITORIA = 50000, função exigeAuditoria(pedido: Pedido): boolean, e função totalPorStatus(pedidos: Pedido[]): Record&lt;string, number&gt;.</code>')
)

section("prompts-sprint2", "Sprint 2 (CRUD) — Prompts para o agente",
    ficha("g", "Prompt A — Serviço de API",
      '<code>Em src/services/api.ts escreva uma função assíncrona listarPedidos(): Promise&lt;Pedido[]&gt; que use fetch para carregar /data/pedidos.json (use BASE_URL do import.meta.env). Trate erros com throw new Error e texto em português.</code>') +
    ficha("a", "Prompt B — Renderização de lista",
      '<code>Em src/main.ts escreva uma função renderLista(pedidos: Pedido[]) que: (1) receba o array de pedidos; (2) monte uma tabela HTML com colunas Protocolo, Unidade, Status, Valor, Aberto em; (3) use Intl.NumberFormat para formatar valores em BRL; (4) use mapeamento de cor por status (rascunho=cinza, enviado=azul, em_cotacao=ambar, em_auditoria=roxo, aprovado=verde, devolvido=vermelho); (5) insira no #app.</code>') +
    ficha("p", "Prompt C — Router hash e integração",
      '<code>Em src/main.ts: (1) use window.addEventListener(\'hashchange\', render) para detectar navegação; (2) default para #/lista; (3) importe e chame listarPedidos, depois renderLista; (4) se fetch falhar, mostre mensagem de erro no #app; (5) exporte a função para poder ser testada.</code>')
)

section("prompts-sprint3", "Sprint 3 (Autenticação e Permissões) — Prompts para o agente",
    ficha("g", "Prompt A — Sistema de papéis",
      '<code>Em src/auth/Papeis.ts: (1) defina tipo Papel como \'ADMIN\' | \'EDITOR\' | \'LEITOR\' | \'APROVADOR\'; (2) tipo Acao como \'ver\' | \'criar\' | \'editar\' | \'excluir\' | \'aprovar\' | \'ver_log\'; (3) tabela PERMISSOES mapeando cada Papel ao array de Ações que pode executar; (4) função pode(papel: Papel, acao: Acao): boolean que retorna true se a ação está no array.</code>') +
    ficha("a", "Prompt B — Testes de permissão",
      '<code>Em src/auth/auth.test.ts escreva 4 testes com Vitest: (1) ADMIN pode tudo exceto ver_log? (não); (2) LEITOR não pode editar; (3) APROVADOR pode aprovar mas não pode editar; (4) EDITOR não pode excluir nem ver_log.</code>') +
    ficha("p", "Prompt C — Middleware de rota",
      '<code>Escreva uma função verificarPermissao(papel: Papel, acao: Acao): void que lance Error com mensagem \'Acesso negado: [acao] não permitida para [papel]\' se pode() retornar false. Exporte como verificar from \'../auth/Papeis.ts\'.</code>')
)

section("prompts-sprint4", "Sprint 4 (PWA Offline) — Prompts para o agente",
    callout("note", "Prerequisite", "O vite-plugin-pwa já foi configurado no Passo 3. "
      "Estes prompts ajustam o service worker para funcionar offline com os dados do projeto.") +
    ficha("g", "Prompt A — Cache de dados estáticos",
      '<code>No vite.config.ts, na seção workbox do VitePWA, configure: globPatterns para incluir public/data/*.json. Adicione runtimeCaching com Strategy: \'CacheFirst\' para URLs que terminam em .json, com cacheName: \'dados-json\', e expiration maxEntries: 50, maxAgeSeconds: 86400 (1 dia).</code>') +
    ficha("a", "Prompt B — Indicador de modo offline",
      '<code>Em src/main.ts: (1) escute window.addEventListener(\'offline\', ...) para adicionar classe \'offline\' ao body; (2) escute \'online\' para remover; (3) no CSS: body.offline #app::before { content: \'⚠️ Modo offline — dados em cache\'; display:block; background: var(--ambar); color: white; padding: 8px; text-align: center; font-size: 13px; }</code>') +
    ficha("p", "Prompt C — Registro manual do SW (se necessário)",
      '<code>Se o VitePWA não registrar automaticamente (alguns navegadores), escreva em src/sw-register.ts: if (\'serviceWorker\' in navigator) { window.addEventListener(\'load\', () => navigator.serviceWorker.register(\'/nome-do-repo/sw.js\')); } e importe no main.ts.</code>')
)

section("prompts-sprint5", "Sprint 5 (Visualização e Dashboard) — Prompts para o agente",
    ficha("g", "Prompt A — KPI cards",
      '<code>Em src/dashboard/kpis.ts: (1) função calcularKPIs(pedidos: Pedido[]) que retorna objeto com total de pedidos, total de valores (formatado BRL), quantidade que exige auditoria, percentual de aprovados; (2) função renderizarKPIs(kpis) que monte 4 cards HTML (classe .kpi-card) e insira no elemento passado como parâmetro.</code>') +
    ficha("a", "Prompt B — Gráfico de barras (vanilla JS + SVG)",
      '<code>Em src/dashboard/graficos.ts: (1) função renderizarBarras(dados: { label: string; valor: number }[], containerId: string) que: gere SVG inline com rects proporcionais ao valor máximo; (2)labels em texto abaixo das barras; (3) valores acima das barras; (4) use CSS vars para cores.</code>') +
    ficha("p", "Prompt C — Filtros por status",
      '<code>Em src/dashboard/filtros.ts: (1) função renderizarFiltros(onChange: (status: string[]) => void) que gere botões/toogle buttons para cada status único; (2) escute click para marcar/desmarcar; (3) chame onChange passando array de status ativos; (4) estilize com CSS .filtro-btn.active { background: var(--accent); color: white }.</code>')
)

# ─── PARTE 7 ─────────────────────────────────────────────────────────────────
grp("Parte 7 · Fluxo completo — do commit ao ar")

section("fluxo-diario", "O fluxo de trabalho que você vai repetir todo dia",
    flow_h([
        ("📋", "Criar/\nmudar branch"), ("\u27a4", ""), ("✏️", "Codar no\nAntigravity"),
        ("\u27a4", ""), ("🧪", "npm test\n(local)"), ("\u27a4", ""), ("📤", "Commit\ne Push"),
        ("\u27a4", ""), ("⚡", "CI roda\nautomático"), ("\u27a4", ""), ("🌐", "Site atualiza\nno ar"),
    ]) +
    step([
        ("Criar branch da sprint", "No painel Git do Antigravity: clique no nome da branch atual → 'Create branch' → nomeie como <code>feature/sprint-2-crud</code>."),
        ("Desenvolver e testar localmente", "Execute <code>npm run dev</code> para ver o site em tempo real no navegador. Execute <code>npm test</code> para rodar os testes."),
        ("Commitar com mensagem descritiva", "No painel Agent: 'Analise o que mudou e escreva uma mensagem de commit no conventional commits (feat:, fix:, docs:).' Revise e confirme."),
        ("Push e aguarde o CI", "No painel Git: Sync → empurra a branch. O GitHub Actions começa automaticamente."),
        ("Mergear na main (após aprovação)", "No GitHub: abra uma Pull Request, revise o diff, e clique em 'Merge'. O deploy acontece automaticamente após o merge."),
    ])
)

section("ativar-pages-settings", "Configurar GitHub Pages (via Settings)",
    step([
        ("Acesse Settings do repositório", "No github.com, entre no repositório do seu MVP."),
        ("Pages na barra lateral", "Clique em 'Pages' na barra lateral esquerda."),
        ("Source", "Em 'Build and deployment', em 'Source', selecione <b>GitHub Actions</b>."),
    ]) +
    callout("tip", "Isso é só uma vez", "Feito isso, o workflow controla 100% dos deploys. "
      "Você nunca mais precisa mexer nisso manualmente.")
)

section("debug-deploy", "Depurando erros de deploy",
    tbl(["Sintoma", "Causa mais provável", "Solução"],
        [["Site abre em branco", "base path errado no vite.config.ts", "Verifique se REPO = 'nome-exato-do-repo' (sem / no final)"],
         ["404 em /data/pedidos.json", "Falta gerar dados ou JSON vazio", "Execute python scripts/gerar_dados.py e commite o public/data/"],
         ["Testes falham no CI mas passam localmente", "Inconsistência entreWindows e Linux (quebras de linha)", "Adicione .gitattributes com '* text=auto eol=lf'"],
         ["workflow_dispatch não aparece", "Workflow não foi commitado na main ainda", "Faça push da branch main primeiro"],
         ["deploy-pages falhou com permissões", "Pages não foi ativado em Settings", "Settings → Pages → Source: GitHub Actions"]],
        num_cols=[])
)

# ─── PARTE 8 ─────────────────────────────────────────────────────────────────
grp("Encerramento")

section("checklist-final", "Checklist de entrega — o que você precisa ter ao final do dia",
    step([
        ("Repositório criado no GitHub", "Verifique em <b>github.com/seu-usuario</b> se o repo aparece."),
        ("Projeto scaffoldado no Antigravity", "Execute <code>npm run dev</code> e confirme que o site abre em <code>localhost:5173</code>."),
        ("vite.config.ts com base path correto", "Abra o arquivo e confirme: <code>base: '/nome-do-repo/'</code>."),
        ("Dados sintéticos gerados", "Confirme que <code>public/data/pedidos.json</code> existe e tem conteúdo."),
        ("Testes unitários passando", "Execute <code>npm test</code> — resultado: 'X passed'."),
        ("Primeiro commit na branch main", "No painel Git: stage, commit 'feat: setup inicial', push."),
        ("Workflow rodou no Actions", "Na aba Actions do repo: o workflow deve estar verde."),
        ("Site acessível no ar", "Acesse <code>https://seu-usuario.github.io/nome-do-repo/</code> e confirme que abre."),
    ]) +
    kpi([
        ("8/8", "itens completos?"), ("< 2 min", "tempo de deploy"),
        ("Vitest", "testes rodando"), ("PWA", "instalável offline"),
    ])
)

section("glossario", "Glossário rápido",
    glossary([
        ("PWA (Progressive Web App)", "Aplicação web que funciona offline e pode ser instalada na tela inicial do celular. Usa service worker para cache."),
        ("Service Worker", "Script que roda em segundo plano no navegador, fazendo cache de páginas e dados para funcionar offline."),
        ("Vite", "Build tool moderno (sucessor do webpack). Compila TypeScript e empacota assets rapidamente."),
        ("Vitest", "Framework de testes unitários em TypeScript, compatível com Vite, extremamente rápido."),
        ("CI/CD (Continuous Integration / Deploy)", "Pipeline automático que testa e publica código a cada mudança."),
        ("GitHub Actions", "Plataforma de CI/CD integrada ao GitHub. Roda scripts na nuvem a cada push."),
        ("workflow_dispatch", "Gatilho manual do GitHub Actions. Permite rodar o workflow pelo botão 'Run workflow'."),
        ("BASE_URL", "Variável do Vite que contém o caminho base do projeto (ex: '/mvp-pedidos-sesp/'). Usada para montar URLs de assets."),
        ("vite-plugin-pwa", "Plugin Vite que gera service worker, manifesto PWA e ícones automaticamente."),
        ("pytest", "Framework de testes Python. Usado no CI para verificar que os dados sintéticos não expõem CPFs."),
    ])
)

section("quiz-final", "Quiz rápido — teste seu conhecimento",
    q("Qual arquivo define o caminho base do projeto no GitHub Pages?",
      ["package.json", "vite.config.ts", "deploy.yml", "manifest.webmanifest"], 1,
      "O base path (/nome-do-repo/) é configurado no vite.config.ts, não no workflow.") +
    q("Por que usamos dados sintéticos no MVP?",
      ["Para o projeto parecer mais bonito", "Para não expor dados reais de cidadãos (LGPD)", "Porque não temos acesso à base de dados real", "Para o GitHub Actions funcionar"], 1,
      "A LGPD proíbe colocar dados pessoais de cidadãos em chatbots públicos e sistemas de demonstração.") +
    q("O que acontece quando você faz push na branch main?",
      ["Nada automático", "O GitHub Actions executa o workflow: testa, compila e publica", "O site cai", "O notebooklm atualiza"], 1,
      "O workflow dispara automaticamente: Python (dados), Node (testes + build), deploy-pages.") +
    q("O que é o workflow_dispatch?",
      ["Um bug do GitHub", "Um gatilho que permite rodar o workflow manualmente pelo botão", "Um tipo de branch", "Um script Python"], 1,
      "Útil para testar o build antes de fazer merge de uma PR.")
)

section("ate-proxima", "Até a próxima — e não pare de codar",
    p("Você terminou o Dia 8 com um MVP no ar. Isso significa que:") +
    grid2([
        ("Código versionado", "Tudo que você escreve está no Git, com histórico, branches e capacidade de reverter erros."),
        ("Testes automatizados", "Qualquer mudança que quebre algo vai aparecer no CI antes de chegar em produção."),
        ("Site acessível", "Qualquer pessoa com o link consegue acessar — sem instalar nada, direto do celular."),
        ("PWA offline", "Mesmo sem internet, o site continua funcionando com os dados em cache."),
    ]) +
    callout("purple", "Próximo passo", "Na próxima aula, vamos expandir o MVP com "
      "mais funcionalidades e aprofundar a engenharia de prompts para que o agente "
      "gere código de maior complexidade com menos retrabalho.") +
    p("Até lá: commite todo dia, rode os testes, e use o painel Agent para perguntar "
      "'como fazer isso?' antes de pesquisar no Google. O agente é o seu primeiro par de olhos técnicos.")
)

# =================================================================
# BUILD
# =================================================================
if cur_group:
    toc_groups.append((cur_group, cur_items))

def build_toc():
    out = ""
    for gtitle, items in toc_groups:
        out += f'<div class="grp">{gtitle}</div>'
        for anchor, titulo in items:
            out += f'<a href="#{anchor}" data-anchor="{anchor}">{titulo}</a>'
    return out

def build_sections():
    out = ""
    for i, (anchor, titulo, body) in enumerate(sections, start=1):
        out += (f'<section id="{anchor}"><span class="secnum">§ {i}</span>'
                f'<h2>{titulo}</h2>{body}</section>')
    return out

HTML = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Caderno do Dia 8 · SESP/MT</title>
<meta name="description" content="Caderno de aprofundamento do Dia 8: do NotebookLM ao MVP no ar — prompts, stack técnica, GitHub Pages e deploy automático.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>{CSS}</style>
</head>
<body>
<header class="top">
  <div class="inner">
    <span class="kicker">Dia 8 · SESP/MT</span>
    <h1>Do NotebookLM ao MVP no Ar — Prompt Engineering e Deploy Automático</h1>
    <p class="sub">Caderno de aprofundamento: transforme contexto e sprints do NotebookLM em um MVP
      funcional, versionado no GitHub e hospedado no GitHub Pages — com testes e PWA offline.</p>
    <div class="meta">Curso de Capacitação SESP/MT · Professor Renato Rosa · Módulo 8</div>
  </div>
</header>
<div class="wrap shell">
  <nav class="toc">
    <input type="text" id="tocsearch" placeholder="Buscar no índice...">
    <div id="tocgroups">{build_toc()}</div>
  </nav>
  <main>
    {build_sections()}
  </main>
</div>
<footer class="pagefoot">Caderno do Dia 8 · Curso de Capacitação SESP/MT · Professor Renato Rosa</footer>
<button class="themebtn" id="themebtn">🌗 Tema</button>
<button class="pdfbtn" id="pdfbtn">🖨️ Imprimir / PDF</button>
<script>
(function(){{
  var btnT = document.getElementById('themebtn');
  var root = document.documentElement;
  var saved = null;
  try {{ saved = localStorage.getItem('caderno-theme'); }} catch(e) {{}}
  if (saved) root.setAttribute('data-theme', saved);
  btnT.addEventListener('click', function(){{
    var cur = root.getAttribute('data-theme');
    var next = cur === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try {{ localStorage.setItem('caderno-theme', next); }} catch(e) {{}}
  }});
  document.getElementById('pdfbtn').addEventListener('click', function(){{ window.print(); }});

  var links = Array.prototype.slice.call(document.querySelectorAll('nav.toc a'));
  var secs = Array.prototype.slice.call(document.querySelectorAll('main section'));
  function onScroll(){{
    var pos = window.scrollY + 120;
    var current = secs[0];
    secs.forEach(function(s){{ if (s.offsetTop <= pos) current = s; }});
    links.forEach(function(a){{ a.classList.toggle('active', a.getAttribute('data-anchor') === current.id); }});
  }}
  window.addEventListener('scroll', onScroll);
  onScroll();

  var search = document.getElementById('tocsearch');
  search.addEventListener('input', function(){{
    var term = search.value.toLowerCase();
    links.forEach(function(a){{
      var show = a.textContent.toLowerCase().indexOf(term) !== -1;
      a.style.display = show ? '' : 'none';
    }});
    document.querySelectorAll('#tocgroups .grp').forEach(function(g){{
      var next = g.nextElementSibling, any = false;
      while (next && !next.classList.contains('grp')) {{
        if (next.style.display !== 'none') any = true;
        next = next.nextElementSibling;
      }}
      g.style.display = any ? '' : 'none';
    }});
  }});
}})();
</script>
</body>
</html>
"""

OUT.write_text(HTML, encoding="utf-8")
print(f"Gerado: {OUT}")
print(f"Seções: {len(sections)} | Grupos: {len(toc_groups)} | Tamanho: {len(HTML)//1024} KB")
