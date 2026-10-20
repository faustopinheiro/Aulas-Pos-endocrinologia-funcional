# Imagens e diagramas

O usuário pediu explicitamente: **alternar os estilos de imagem (não ter só imagens 3D) e ter diagramas em todos os capítulos.** Um livro só com renderizações 3D fica repetitivo e "não gera vontade de ver"; a variação dá ritmo e mostra o conteúdo de ângulos diferentes. Diagramas são o que o leitor salva e estuda.

## 0. Economia de créditos (regra do usuário, vale acima das metas abaixo)

O usuário pediu: **use o Gamma só quando a imagem for realmente necessária**, porque os créditos são limitados (~70 por imagem).

- **Padrão:** 1 imagem gerada por capítulo (a abertura). No máximo 2–3 quando uma figura não puder ser substituída (ex.: microscopia de um tecido que o texto discute, fotografia clínica de um procedimento difícil de desenhar).
- **Primeiro, reaproveite:** imagens já geradas em capítulos anteriores do mesmo e-book (pasta `img/`) servem para aberturas de parte, figuras de contexto e cartões repetidos.
- **Todo o resto em SVG:** diagramas, mapas anatômicos esquemáticos, esquemas de testes e de exercícios (biblioteca com bonecos esquemáticos: segmentos como linhas grossas arredondadas, articulações em círculos, setas e cotas em dourado), ícones e infográficos.
- A alternância de estilos continua valendo: ela passa a ser feita entre **a imagem de abertura, os diagramas, os esquemas e as imagens reaproveitadas**, e não exige novas gerações.
- Ao entregar, informe quantas imagens foram geradas e o saldo.
- **Mais diagramas e esquemas** (pedido do usuário): mínimo de **8 diagramas/esquemas SVG por capítulo**, e toda seção de conteúdo com pelo menos um elemento desenhado (fluxo, ciclo, pirâmide, matriz, linha do tempo, gráfico, mapa anatômico, esquema de teste ou exercício). Tabelas não contam como diagrama.

## 1. Plano visual do capítulo (faça antes de gerar)

Monte uma tabela rápida: posição no capítulo → tipo (imagem ou diagrama) → estilo → o que mostra. Metas por capítulo de lesão/doença:

- **Imagens:** abertura + 3 a 5 figuras de conteúdo + biblioteca de exercícios.
- **Pelo menos 3 estilos diferentes** entre abertura e figuras de conteúdo.
- **3D anatômico em no máximo ~40%** das figuras de conteúdo, e nunca duas figuras seguidas no mesmo estilo.
- **Diagramas SVG: no mínimo 4** (além das tabelas), por exemplo: fluxograma de decisão, linha do tempo das fases, gráfico com um dado da evidência, mapa mental e semáforo/escala.
- A **biblioteca de exercícios** é a exceção: use um estilo único dentro dela (coerência entre os cartões). Alterne o estilo da biblioteca entre capítulos: 3D translúcido (capítulo 12) ou **fotografia realista de estúdio, fundo grafite** (capítulo 13, aprovada). Um esquema SVG dentro de um cartão é bem-vindo quando a foto não mostra o detalhe técnico.
- **Capítulos de base** (atuação, biomecânica, reparo, dor, avaliação, carga, exercício, recursos, emergências): 4–6 imagens e 6 ou mais diagramas. **Capítulos de lesão** (tecido e região): abertura + 5 figuras + biblioteca de 6–9 exercícios.
- Referência de alternância aprovada (capítulo 13): abertura 3D → mecanismo em ilustração editorial → exame em fotografia clínica → ultrassom → microscopia → fotografia esportiva → biblioteca em fotografia de estúdio.

## 2. Estilos de imagem e quando usar

| Estilo | Melhor para | Prompt-base (sempre em inglês, sempre com "No text, letters, labels or watermarks") |
|---|---|---|
| **A · Microscopia real** | Capa, abertura de parte, biologia do tecido, reparo, inflamação | "Real confocal fluorescence microscopy photograph of [tecido], [estruturas] in [cores], black background, extremely sharp scientific micrograph, journal cover quality." Variações: histologia corada (H&E), microscopia eletrônica de varredura, luz polarizada. |
| **B · 3D anatômico translúcido** | Mecanismo de lesão, anatomia funcional, abertura de capítulo | "Cinematic 3D medical illustration of [estrutura/ação], translucent steel-blue body, [músculos] glowing warm red, golden filaments, dark navy background, volumetric light." |
| **C · Fotografia clínica realista** | Exame físico, procedimentos, atendimento, equipamentos, reabilitação em clínica | "Realistic editorial photograph, natural light, physiotherapy clinic, a physiotherapist performing [teste/técnica] on an athlete's [região], hands and knee in focus, shallow depth of field, faces out of frame or not identifiable." |
| **D · Ilustração editorial** | Conceitos, processos, educação do paciente, comparações | "Clean flat editorial medical illustration on a light warm-beige background, limited palette of navy (#1d2b3a), gold (#b8923f), steel blue (#2d4a7a) and clay red (#c23a32), [conceito], minimal shapes." |
| **E · Imagem diagnóstica estilizada** | Seções de imagem, prognóstico, achados | "Realistic knee MRI sagittal slice style image showing [achado], grayscale with subtle blue tint, clinical radiology look." Use apenas para ilustrar o tipo de exame, nunca como "caso real", e sem marcações falsas de diagnóstico. |
| **F · Fotografia esportiva** | Abertura de capítulos de esporte, prevenção, retorno | "Dramatic sports photograph of an athlete [ação] in [ambiente], motion, cinematic light, no logos, no identifiable face." Não usar modalidade que o usuário excluiu (ele pediu para "esquecer futebol" no e-book de fisioterapia desportiva). |

Exemplo de alternância para um capítulo de joelho: abertura B (3D do joelho com enxerto) → figura de mecanismo B → exame C (foto de Lachman) → menisco A (microscopia de fibrocartilagem) ou E (RM) → patelofemoral D (ilustração quadril-joelho) → futuro F ou C (sensores em clínica). Biblioteca: todo em B ou todo em C.

## 3. Gamma: gerar, baixar, conferir

1. Gere todas as imagens do capítulo **na mesma rodada, em paralelo** (`mcp__Gamma__generate_image`, `type: photo` para A/B/C/E/F e `illustration` para D; `sizePreset: banner` 16:9 para figuras e abertura, `social-portrait` 4:5 para capa). Não use as palavras "cover", "book" ou "capa": o modelo desenha um livro sobre a mesa.
2. Acompanhe com `mcp__Gamma__get_image_generation_status` até `completed`. Cada imagem custa ~70 créditos; a resposta traz o saldo.
3. Baixe e reduza para o PDF:
   ```bash
   curl -sS -o img/nome.jpg "<image.url>"
   python3 -c "from PIL import Image; im=Image.open('img/nome.jpg').convert('RGB'); im.thumbnail((1900,1900)); im.save('img/w-nome.jpg',quality=86,optimize=True)"
   ```
   Use sempre as versões `w-*.jpg` no HTML (PDF leve).
4. **Confira visualmente** montando uma folha de miniaturas com PIL e lendo a imagem. Verifique anatomia, lado, apoio e execução correta do exercício. Refaça a que estiver errada, descrevendo a posição de forma literal (qual perna, onde apoia, de que lado).
5. Títulos, rótulos e legendas **nunca** dentro da imagem: entram no HTML por cima ou na legenda (acentuação correta e editável).

Se o download der 403, ver "Armadilhas" no SKILL.md.

## 4. Diagramas SVG (custo zero)

Desenhe direto no HTML com `<svg width="100%" viewBox="0 0 680 H">` (largura útil da página). Fonte Inter 11–13 no viewBox, títulos em caixa alta com `letter-spacing`. Cores da paleta. Sempre com legenda "Figura N.x".

Catálogo (há exemplos prontos no capítulo modelo):

- **Fluxograma de decisão** (caixas + setas com `marker-end`): do sintoma/exame à conduta.
- **Linha do tempo de fases** (4 blocos coloridos com seta): fases da reabilitação com prazo de referência e critério.
- **Gráfico de barras horizontal** com um dado forte da evidência (ex.: redução de risco relativo). Prefira risco relativo quando não tiver certeza dos valores absolutos.
- **Curva** (polyline) para cinética, equilíbrio de fármaco, curva dose-resposta.
- **Eixo/processo** com nós ligados por linha em gradiente (`gradientUnits="userSpaceOnUse"`, `stroke-width` ≥ 6).
- **Semáforo/escala** (três blocos verde, âmbar, vermelho) para monitoramento de dor ou carga.
- **Mapa mental**: elipse central escura, 6–8 caixas coloridas ligadas por curvas douradas, 2–4 linhas de palavras-chave por caixa.
- **Resumo visual em blocos** (`.tiles`) com os números-chave do capítulo.
- **Mapa anatômico esquemático** simples (formas geométricas e rótulos) quando uma imagem gerada não for confiável o suficiente, como o mapa das regras de Ottawa do capítulo 13 (zonas coloridas sobre silhuetas de perna e pé, legenda embaixo com espaço próprio).
- **Esquema de exercício ou teste** em SVG (segmentos corporais como linhas grossas arredondadas, articulações como círculos, cotas em dourado) quando a fotografia gerada não mostra a execução correta.

Ao terminar o capítulo, conte: imagens por estilo e diagramas. Se faltar variedade, troque uma figura 3D por outro estilo ou converta uma tabela em diagrama.
