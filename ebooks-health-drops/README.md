# E-books Health Drops

- `skill/health-drops-ebooks/` — skill com o padrão completo (instruções, CSS, scripts e capítulo modelo). `skill/health-drops-ebooks.skill` é o pacote para instalar.
- `fisioterapia-desportiva/` — projeto do e-book Fisioterapia Desportiva:
  - `livro.json` — estrutura (7 partes, 19 capítulos) e configuração da capa;
  - `capNN.html` — capítulos prontos (fragmentos);
  - `img/` — imagens usadas (geradas no Gamma, versões otimizadas);
  - `pdf/` — estrutura, logos/capas e o PDF de teste mais recente.

Para montar o PDF:

```bash
cd fisioterapia-desportiva
python3 ../skill/health-drops-ebooks/scripts/refs_fix.py cap12.html
python3 ../skill/health-drops-ebooks/scripts/build_ebook.py livro.json
PW_PATH=<caminho do playwright> node ../skill/health-drops-ebooks/scripts/render.js livro.html livro.pdf
```
