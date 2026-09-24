# Aula 8 — Do sprint.md ao MVP no ar

**Curso de Capacitação SESP/MT · Professor Renato Rosa**

Caderno para os grupos construírem o MVP no Antigravity a partir do `contexto.md` e do `sprint.md`
gerados no NotebookLM: TypeScript + Python num PWA, versionado no GitHub e publicado no GitHub Pages
com deploy automático (GitHub Actions). São 34 seções e 54 prompts prontos. O PDF tem 44 páginas A4.

## Conteúdo

| Parte | Seções |
|---|---|
| **Abertura** | O que vamos construir · Como usar o caderno · Conferência dos dois arquivos · Prompts do NotebookLM em versão técnica |
| **1 · O que dá para publicar** | O que "full stack" vira no GitHub Pages · Arquitetura (Python / TS / JS / GitHub) · Estrutura de pastas |
| **2 · Trabalhando com o agente** | Anatomia do prompt · Ciclo planejar → gerar → testar → commitar · Regras de segurança |
| **3 · Sprint 0** | Instalar Node e Python · Criar o projeto sem perder os .md · Publicar o repositório · Diagnóstico pelo agente · REGRAS-DO-PROJETO.md · `base` do Vite |
| **4 · Sprints 1 a 5** | Dados sintéticos + LGPD (Python/pytest) · Regras, papéis e auditoria (TS/Vitest) · Telas · PWA · Homologação · Deploy com Actions · Versionamento · README |
| **5 · Biblioteca de prompts** | Planejamento · Construção por camada · Depuração · Revisão · Prompts ruins × bons |
| **Fechamento** | Problemas comuns · Checklist de entrega · Glossário · Quiz com respostas |

## Arquivos

```
Aula 8/
├── caderno-dia8.html          # fonte viva: índice, busca, tema claro/escuro, botão Copiar nos prompts
├── Caderno Dia 8 - SESP.pdf   # versão para imprimir (capa, sumário com páginas, marcadores)
├── gerar_caderno_aula8.py     # gerador do HTML (conteúdo + CSS)
├── exportar_pdf.py            # gera HTML + PDF em duas passadas (números de página do sumário)
└── Dia-8-Sesp.pdf             # slides legados do professor
```

Para regerar tudo depois de editar o conteúdo:

```
python exportar_pdf.py
```

Requer `pip install playwright pymupdf` e `playwright install chromium`.

## Como o PDF é paginado

- A capa fica sozinha, e o sumário ocupa uma página com o número de página de cada seção.
- Cada **Parte** começa em página nova, com uma faixa de abertura. Dentro de uma Parte, as seções
  seguem em sequência, então não sobram páginas em branco.
- Prompts, caixas, cartões, linhas de tabela e passos nunca se dividem entre páginas. Códigos com
  mais de 45 linhas podem continuar na página seguinte.
- Código e prompts quebram linha em vez de cortar na margem.
- A impressão sempre usa o tema claro, e as respostas do quiz aparecem abertas.

## O que foi validado antes de entrar no caderno

Um projeto de referência (Vite 8 + TypeScript, vite-plugin-pwa 1.3, Vitest 5, Python 3.12) foi testado com:
- `python scripts/gerar_dados.py`: gera 120 pedidos sintéticos com CPF mascarado; o `pytest` passa;
- `npm test`: 3 testes do Vitest passando;
- `npm run build`: o service worker é gerado e 21 arquivos ficam em cache;
- site servido em `/nome-do-repo/`, como no GitHub Pages: rotas por hash e JSON carregados com `BASE_URL`,
  e o app funciona **offline**;
- os passos do `deploy.yml` foram repetidos localmente (`npm ci`, testes, build); o workflow **não** foi
  executado no GitHub. As actions usam as versões mais recentes em set/2026: `checkout@v7`,
  `setup-node@v7`, `setup-python@v7`, `configure-pages@v6`, `upload-pages-artifact@v5`, `deploy-pages@v5`;
- `npm create vite` numa pasta que já tem arquivos cancela, e a opção `--overwrite` apaga esses arquivos.
  Por isso o caderno manda criar o projeto numa pasta nova e só depois mover os `.md`.
