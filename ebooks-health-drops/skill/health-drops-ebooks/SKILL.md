---
name: health-drops-ebooks
description: >-
  Sistema de produção dos e-books Health Drops — e-books didáticos de saúde (fisioterapia, medicina, enfermagem, nutrição e áreas afins) em PDF A4 com padrão editorial próprio, capa com microscopia, capítulos com testes, tratamento por fases, biblioteca de exercícios, protocolos, diagramas, questões comentadas e referências. Use SEMPRE que o usuário pedir para criar, estruturar, continuar, revisar ou diagramar um e-book, livro, apostila, material completo, resumo em livro ou capítulo de livro da área da saúde — mesmo que não diga "Health Drops" nem "skill" (ex.: "faz o capítulo 13 de fisioterapia desportiva", "monta um e-book de enfermagem sobre feridas", "estrutura um livro de cardiologia", "quero um material no modelo daquele PDF", "próximo capítulo do livro"). Também usar para capas, sumários e logos dos e-books Health Drops.
---

# E-books Health Drops

Produz e-books de saúde no padrão aprovado pelo usuário: PDF A4 montado em HTML e renderizado com Playwright, com texto técnico e profundo, tratamento sempre explícito, imagens geradas no Gamma (em estilos alternados) e diagramas desenhados em SVG.

O usuário é profissional de saúde e professor. Ele julga pelo PDF renderizado, então **sempre entregue o PDF e confira as páginas visualmente antes de entregar**.

## Identidade (decisões já tomadas, não renegociar sem pedido)

- **Marca:** Health Drops (logo: gota em contorno com linha de batimento dourada + "health" fino + "drops" em serifa dourada). Não é "coleção"; são e-books da área.
- **Nenhum nome de pessoa** em lugar algum (capa, cabeçalho, rodapé, créditos). O usuário pediu explicitamente.
- **Capa** (modelo "faixa"): imagem de **microscopia** de um tecido ligado ao tema ocupando os 2/3 superiores; faixa escura embaixo com o título em serifa grande, segunda palavra em dourado, filete dourado. Logo no canto superior esquerdo e **"EDIÇÃO 2027"** no canto superior direito. Nada mais: sem número de capítulos, sem subtítulo, sem "material completo".
- **Cabeçalho:** gota + nome do e-book à esquerda; etiqueta com o **tema do capítulo** à direita (ex.: JOELHO).
- **Rodapé:** nome do e-book + número da página.
- **Paleta:** areia `#f1ebdf`, papel `#fcfaf5`, tinta `#1d2b3a`, ouro `#b8923f`, clay `#c23a32`; cor-tema por e-book (fisioterapia desportiva: azul-aço `#2d4a7a`). Fontes: Fraunces (títulos), Inter (corpo), JetBrains Mono (detalhes).
- **Tamanho:** não há meta de páginas; depende do tema. Capítulos de lesão/doença completos ficam com ~25–30 páginas; capítulos de base são mais enxutos.

## Fluxo de trabalho

1. **Entender o pedido:** área, tema, público (graduação, pós, prova de título), escopo (estrutura, um capítulo, o livro todo).
2. **Estrutura do livro** (quando for livro novo): pesquise grades de pós-graduação, conteúdo de prova de título/residência, competências da profissão e sumários dos livros-texto de referência. Proponha partes → capítulos → tópicos com **o tratamento escrito nos tópicos** (o usuário rejeitou estruturas que só listavam doenças). Mostre a estrutura num PDF curto antes de produzir capítulos.
3. **Escrever o capítulo** como fragmento HTML seguindo `references/padrao-capitulo.md`. Use `assets/exemplo-capitulo-joelho.html` como modelo de todos os componentes (é o capítulo aprovado). Leia `references/ciencia-e-referencias.md` antes de escrever.
4. **Plano visual:** antes de gerar qualquer imagem, faça o plano de imagens e diagramas do capítulo seguindo `references/imagens-e-diagramas.md`. Regra do usuário: **alternar estilos de imagem (não só 3D) e ter diagramas** em todo capítulo.
5. **Gerar imagens no Gamma em paralelo**, baixar, redimensionar e conferir cada uma (contact sheet). Refaça a que estiver anatomicamente ou tecnicamente errada.
6. **Montar e renderizar:**
   ```bash
   # projeto: pasta com livro.json, fragmentos capNN.html e img/
   python3 scripts/refs_fix.py capNN.html          # numera as citações na ordem de aparição
   python3 scripts/build_ebook.py livro.json --capitulos NN   # capa + sumário + capítulo(s)
   PW_PATH=<caminho do playwright> node scripts/render.js livro.html livro.pdf
   ```
   `render.js` imprime, por página, quantos pixels o conteúdo passou do limite (`overflowPx` > 0 = texto cortado). Corrija enxugando texto, dividindo a página ou reduzindo a tabela; nunca entregue com overflow. Se `build_ebook.py` avisar que o sumário mudou de tamanho, ajuste `paginas_sumario` no JSON e rode de novo (a numeração das páginas depende disso).
7. **Conferir:** gere miniaturas (`pdftoppm -r 50`) e olhe todas as páginas novas; confira em texto que não há nome de pessoa nem ano errado (`pdftotext livro.pdf - | grep`).
8. **Entregar** o PDF com `SendUserFile` e um resumo curto: o que entrou, créditos gastos/restantes do Gamma, e o que precisa de checagem (referências recentes, números clínicos).

## Arquivos

- `scripts/build_ebook.py` — monta capa, sumário (paginação automática, com página inicial de cada capítulo) e capítulos a partir de `livro.json`. Copia `assets/style.css` para o projeto.
- `scripts/render.js` — HTML → PDF A4 (Playwright/Chromium), espera as fontes e mede overflow por página.
- `scripts/refs_fix.py` — renumera citações (Vancouver por ordem de aparição) e divide a lista de referências em páginas.
- `assets/style.css` — todo o CSS dos componentes.
- `assets/exemplo-capitulo-joelho.html` — capítulo modelo completo (28 páginas) com todos os componentes.
- `assets/livro.exemplo.json` — configuração do e-book Fisioterapia Desportiva (19 capítulos, 7 partes).
- `assets/logo-health-drops.svg` — logo para usos fora do PDF.
- `references/padrao-capitulo.md` — estrutura do capítulo, componentes e regras de diagramação.
- `references/imagens-e-diagramas.md` — alternância de estilos, prompts do Gamma, download e catálogo de diagramas SVG.
- `references/ciencia-e-referencias.md` — regras de conteúdo científico, linguagem e referências.

## Armadilhas já vividas

- **Download do Gamma bloqueado:** se `curl` para `cdn.gamma.app` der 403, a rede do ambiente não libera o domínio. Peça ao usuário para adicionar `*.gamma.app` em Allowed domains (rede Custom) nas configurações do ambiente e abrir sessão nova; enquanto isso, ofereça que ele baixe a imagem e anexe no chat. Não monte o livro dentro do Gamma: a diagramação de lá sobrepõe cabeçalho e título e o usuário rejeitou.
- **"Capa" no prompt gera mockup** (livro sobre a mesa). Descreva só a cena, "full-bleed", "no text".
- **Imagens de exercício erradas** acontecem (ex.: perna fora do banco no Copenhagen). Confira cada uma e refaça com descrição mais literal.
- **Gradiente em linha horizontal some** no SVG se não usar `gradientUnits="userSpaceOnUse"` com x1/x2 reais.
- **Células com rowspan** mudam o "primeiro filho" da linha: use a tabela `tt ex` com `td.es` para a coluna agrupada (ver exemplo de testes clínicos).
- Cada imagem custa ~70 créditos no Gamma; informe o saldo que vem na resposta.
