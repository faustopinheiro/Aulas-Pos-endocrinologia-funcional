# Padrão do capítulo Health Drops

O capítulo modelo é `assets/exemplo-capitulo-joelho.html`. Abra-o e copie os componentes de lá; este documento explica a ordem, o porquê e as regras.

## Sumário

1. Sequência de páginas
2. O formato de tratamento em seis partes
3. Componentes (classes CSS)
4. Regras de diagramação
5. Checklist antes de renderizar

## 1. Sequência de páginas (capítulo de lesão/doença)

| # | Página | Conteúdo |
|---|---|---|
| 1 | Abertura | Faixa "CAPÍTULO N · título", imagem larga (`.hero`) com título curto sobreposto em caixa alta, legenda, gancho clínico (um caso real em 4–6 linhas que cria tensão), parágrafo de escopo e caixa "Ao final deste capítulo, você vai saber" (`.rev`). |
| 2 | Exame: testes clínicos por estrutura | Tabela completa com estrutura, teste, como executar e positivo quando (todas as estruturas da região, não só a principal) + Pegadinha. |
| 3 | Testes funcionais e questionários | Tabela de testes funcionais (o que mede, como interpretar) + tabela de questionários validados + Dica com bateria mínima de consultório. |
| 4… | Uma seção por condição | Para cada condição: mecanismo e diagnóstico → decisão de tratamento → plano por fases → critérios → alta (formato de seis partes abaixo). Condições principais podem ocupar várias páginas. |
| | Prevenção | Evidência, componentes, dose mínima eficaz e exemplo de sessão. |
| | Analgesia e eletroterapia | Modelo de monitoramento da dor; tabela recurso → indicação → como usar (parâmetros) → evidência; medicamentos e infiltrações; Atenção "recurso não substitui exercício". |
| | O que há de novo e o futuro | Imagem + tabela tema → o que mostra → situação ("Já muda a prática", "Promissor", "Experimental") + Dica "como ler novidades". |
| | Biblioteca de exercícios (1–2 páginas) | Cartões `.exc`: imagem, nome numerado, fase, execução, dose, progressão. 4–5 por página. |
| | Protocolos detalhados (1–2 páginas) | Ex.: retorno à corrida por níveis, progressão de pliometria, semana-modelo, programa de 12 semanas. Tabelas com regra de progressão e de recuo. |
| | Na prática | Passos numerados do primeiro dia à alta + tabela de erros comuns. |
| | Caso clínico comentado | Caso com tabela de achados e um bloco "RACIOCÍNIO" que usa números e decide. |
| | Questões comentadas (2 páginas) | 5–6 questões no estilo de prova, cada uma com resposta comentada; uma Dica de prova. |
| | Para revisar em 5 minutos | Lista do essencial + diagrama-resumo (ex.: fases). |
| | Resumo visual | Blocos `.tiles` com 9–12 números-chave + um gráfico simples (ex.: semáforo da dor). |
| | Mapa mental | SVG com o tema no centro e 6–8 ramos. |
| | Referências (1–2 páginas) | Lista Vancouver numerada na ordem de aparição. |

Capítulos de base (atuação, avaliação geral, emergências) seguem a mesma lógica, sem o plano por fases; mantêm abertura, conteúdo, diagramas, Na prática, caso, questões, revisão, resumo visual e referências.

## 2. Formato de tratamento em seis partes (toda condição)

O usuário quer saber o que fazer "na segunda-feira de manhã". Para cada condição:

1. **Avaliação inicial** que define a fase de entrada (testes, linha de base mensurável).
2. **Plano por fases** com objetivo, exercícios e **dose** (séries × repetições, carga ou repetições em reserva, frequência, tempo).
3. **Critérios objetivos para avançar** (ex.: força ≥ 70% do lado sadio para correr) e o que fazer quando não forem atingidos.
4. **Recursos com evidência** que somam ao exercício, com parâmetros, e os que não valem o tempo.
5. **Erros comuns e sinais de alerta.**
6. **Critérios de alta** e ligação com retorno ao esporte/atividade.

Prazos são sempre "referência"; o critério é quem libera a fase.

## 3. Componentes (classes CSS em `assets/style.css`)

- Página: `<section class="page">` + `<!--RUN-->` + `<div class="inner">…</div>` + `<!--FOOT-->`. A abertura não usa RUN (tem topo próprio com `[[MINI]][[TITULO]]` e etiqueta da parte).
- Títulos: `<h2>` (seção, com barrinha dourada), `<h3>` (subseção, cor-tema).
- Texto: `<p>` justificado; citações `<sup>n</sup>`.
- Caixas: `.call.dica` (dourada, ícone `[[ICON_DICA]]`), `.call.peg` (azul, `[[ICON_PEG]]`), `.call.aten` (vermelha, `[[ICON_ATEN]]`). Estrutura: `<div class="call dica"><div class="ic">[[ICON_DICA]]</div><div><div class="lb">DICA</div><p>…</p></div></div>`. Rótulos possíveis: DICA, PEGADINHA, ATENÇÃO, DICA DE PROVA, PARA APROFUNDAR, COMO LER AS NOVIDADES.
- Critério/fórmula: `.formula` com `<h4>` e `<p>`.
- Cartões numerados de decisão: `.cards > .c` com `.num.n1..n4`.
- Passos: `.steps > .s` com `.num`.
- Tabelas: `<table>` padrão; `class="tt"` para tabelas densas; `class="tt ex"` + `td.es` quando houver coluna agrupada com rowspan. Logo abaixo, `.src` para fonte/observação.
- Figura: `<div class="fig" style="height:50mm;background:url(img/…) center/cover"></div>` + `<div class="cap"><b>Figura N.x.</b> …</div>`.
- Abertura: `.band` (faixa do capítulo) e `.hero` (imagem com degradê e título sobreposto).
- Raciocínio do caso: `.call.dica` com `display:block` e rótulo RACIOCÍNIO.
- Questões: `.q` com `.ql`, `.en`, `<ol>` (alternativas A–D sem marcador), `.ans` com `.badge`.
- Revisão: `.rev` com `<h4>` e `<ul>`.
- Biblioteca: `.exc` > `.exi` (imagem) + `.ext` (`.exn` com `<span>` da fase, e três `<p>`: Execução, Dose, Progressão).
- Resumo visual: `.tiles` > `.tile` (`.accent` dourado, `.red` vermelho) com `<b>número</b><span>texto</span>`.
- Referências: `<ol class="bib">` com `<li><span class="rn">n</span><span>referência</span></li>`.

## 4. Regras de diagramação

- Uma página A4 comporta ~450–550 palavras com uma tabela e uma caixa. Escreva por página, não em fluxo: cada `<section>` precisa caber.
- Toda página tem pelo menos um elemento visual (tabela, caixa, diagrama, imagem ou cartões). Página só de texto corrido parece apostila.
- Varie o ritmo: não coloque duas páginas seguidas com o mesmo tipo de elemento principal.
- Números de figura sequenciais no capítulo (Figura 12.1, 12.2…), incluindo diagramas SVG com legenda.
- Português do Brasil, frases diretas, termos técnicos explicados na primeira vez. Siglas por extenso na primeira menção.
- Sempre "fisioterapeuta"/profissional da área do e-book como leitor; não citar outras especialidades de forma competitiva.

## 5. Checklist antes de renderizar

- [ ] Cada condição tem as seis partes do tratamento.
- [ ] Testes clínicos de todas as estruturas da região + testes funcionais + questionários.
- [ ] Prevenção, analgesia/eletroterapia, novidades, biblioteca, protocolos, resumo visual e mapa mental presentes.
- [ ] Plano de imagens com estilos alternados e ≥ 4 diagramas SVG (ver `imagens-e-diagramas.md`).
- [ ] Toda afirmação com número tem `<sup>`; `refs_fix.py` rodado.
- [ ] Nenhum nome de pessoa; ano da edição correto.
