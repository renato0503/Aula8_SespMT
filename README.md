# Aula 8 — Do NotebookLM ao MVP no Ar

**Curso de Capacitação SESP/MT · Professor Renato Rosa**

---

## Conteúdo do caderno (32 seções em 9 partes)

| Parte | Conteúdo |
|---|---|
| **Abertura** | Agenda · Checklist de confirmação |
| **1 — Do NotebookLM ao Antigravity** | Prompts melhorados (contexto técnico + sprints com GitHub Pages), o que é MVP, por que PWA |
| **2 — Stack técnica validada** | Vite + TypeScript + Vitest + vite-plugin-pwa + Python + GitHub Actions — explicações e justificativas |
| **3 — Setup do projeto** | Criar repo no GitHub, scaffold (caminho normal e alternativo), vite.config.ts com base path, scripts npm, ícone SVG |
| **4 — Estrutura de código** | src/domain/ · scripts/gerar_dados.py · testes Vitest |
| **5 — GitHub Actions** | Workflow completo deploy.yml (Python + pytest → Node + Vitest → Pages) · Ativar GitHub Pages · Debug |
| **6 — Prompts por sprint** | 4 sprints × 3 prompts = 12 prompts de exemplo para usar no painel Agent do Antigravity |
| **7 — Fluxo completo** | Diagrama do fluxo diário · ativação do Pages · checklist de deploy |
| **Encerramento** | Glossário · Quiz · Próximos passos |

---

## Arquivos principais

```
Aula 8/
├── caderno-dia8.html        # Fonte viva (tema claro/escuro, índice navegável)
├── Caderno Dia 8 - SESP.pdf # Versão para imprimir (export via Playwright/Edge)
├── gerar_caderno_aula8.py   # Gerador do HTML
├── export_pdf.py            # Script de exportação PDF
└── Dia-8-Sesp.pdf          # Slides do professor (referência)
```

---

## O que foi validado antes de entrar no caderno

- Build Vite + TypeScript → dist/ com 21 entries precached
- Service worker registra e faz cache offline (testado com Playwright)
- `npm test` (Vitest): 3 testes passando em ~1.5s
- `python scripts/gerar_dados.py`: 120 pedidos sintéticos, CPFs mascarados
- `pytest -q scripts`: 1 teste passando (verificação LGPD)
- GitHub Actions `deploy.yml`: workflow testado com ações oficiais v7/v6/v5

---

## Referências das actions (versões used)

- `actions/checkout@v7`
- `actions/setup-node@v7`
- `actions/setup-python@v7`
- `actions/configure-pages@v6`
- `actions/upload-pages-artifact@v5`
- `actions/deploy-pages@v5`
