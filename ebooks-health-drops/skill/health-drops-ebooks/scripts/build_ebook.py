#!/usr/bin/env python3
"""Monta um e-book Health Drops (capa + sumário + capítulos) em um único HTML.

Uso:
    python3 build_ebook.py livro.json [--capitulos 12,13] [--saida livro.html]

livro.json fica na pasta do projeto; caminhos de imagem e de fragmentos são
relativos a essa pasta. Veja assets/livro.exemplo.json.

Cada fragmento de capítulo é HTML com uma <section class="page"> por página e
os marcadores:
    <!--RUN-->   cabeçalho (nome do e-book à esquerda, tema à direita)
    <!--FOOT-->  rodapé (nome do e-book + número da página); um por página
    [[MINI]]     ícone da gota (marca)
    [[ICON_DICA]] [[ICON_PEG]] [[ICON_ATEN]]  ícones das caixas
O número de páginas do capítulo é a contagem de <!--FOOT--> do fragmento.
"""
import argparse, html, json, os, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(AQUI, '..', 'assets')

GOTA = ('<svg width="{w}" height="{h}" viewBox="0 0 100 120"><path d="M50 4 C50 4 12 50 12 76 A38 38 0 0 0 88 76 '
        'C88 50 50 4 50 4 Z" fill="none" stroke="{c}" stroke-width="8" stroke-linejoin="round"/>'
        '<polyline points="20,80 38,80 45,64 53,96 60,72 66,80 80,80" fill="none" stroke="#b8923f" stroke-width="7" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')
MINI = GOTA.format(w=15, h=18, c='#1d2b3a')
ICON = {
 'DICA': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2V16h5v-.1c0-.8.4-1.5 1-2A6 6 0 0 0 12 3z"/></svg>',
 'PEG': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/></svg>',
 'ATEN': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l9.5 17h-19z"/><path d="M12 10v4M12 17.5v.1"/></svg>',
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('config')
    ap.add_argument('--capitulos', help='números a incluir, ex.: 12 ou 01,02 (padrão: todos com fragmento)')
    ap.add_argument('--saida')
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.config))
    cfg = json.load(open(a.config, encoding='utf-8'))
    titulo = cfg['titulo']
    l1, l2 = cfg.get('titulo_linha1', titulo), cfg.get('titulo_linha2', '')
    tema_cor = cfg.get('cor_tema', '#2d4a7a')
    shutil.copy(os.path.join(ASSETS, 'style.css'), os.path.join(base, 'style.css'))

    caps = [(p, c) for p in cfg['partes'] for c in p['capitulos']]
    def frag_path(c):
        f = c.get('fragmento')
        return os.path.join(base, f) if f and os.path.exists(os.path.join(base, f)) else None
    # páginas: capa (1) + sumário (reservado) e depois capítulos
    n_sum = cfg.get('paginas_sumario', 5)
    pg = 2 + n_sum
    inicio = {}
    for p, c in caps:
        fp = frag_path(c)
        n = open(fp, encoding='utf-8').read().count('<!--FOOT-->') if fp else c.get('paginas', 10)
        inicio[c['n']] = pg; pg += n

    def run(tema):
        return f'<div class="run"><div class="brand">{MINI}{html.escape(titulo)}</div><div class="tema">{html.escape(tema)}</div></div>'
    def foot(n):
        return f'<div class="foot"><span class="ft">{html.escape(titulo)}</span><span class="n">{n}</span></div>'

    pages = []
    # CAPA: microscopia no topo, faixa escura com título; só logo, edição e título
    pages.append(f'''<section class="page cover" style="isolation:isolate;background:#0d1622">
<div style="position:absolute;z-index:-1;left:0;right:0;top:0;height:215mm;background:url({cfg['capa_imagem']}) {cfg.get('capa_posicao','center 40%')}/cover"></div>
<div style="position:absolute;z-index:-1;left:0;right:0;top:165mm;height:52mm;background:linear-gradient(180deg,rgba(13,22,34,0),#0d1622)"></div>
<div style="position:absolute;top:16mm;left:18mm;display:flex;align-items:center;gap:2.5mm;line-height:1;color:#fff">{GOTA.format(w=30,h=36,c='#fff')}
<span style="font-family:Inter;font-weight:300;font-size:17pt">health</span><span style="font-family:Fraunces,serif;font-weight:700;font-size:17pt;color:#d9b56a;margin-left:-2mm">drops</span></div>
<div style="position:absolute;top:19mm;right:18mm;font-family:Inter;font-size:9pt;font-weight:700;letter-spacing:.28em;color:#d9b56a">EDIÇÃO {cfg.get('edicao','2027')}</div>
<div style="position:absolute;left:18mm;right:18mm;bottom:30mm">
<div class="serif" style="font-size:48pt;font-weight:700;line-height:1;letter-spacing:-.01em">{html.escape(l1)} <span style="color:#d9b56a">{html.escape(l2)}</span></div>
<div style="width:40mm;height:1.3mm;background:#d9b56a;margin-top:6mm;border-radius:1mm"></div></div></section>''')

    # SUMÁRIO: paginação por orçamento de linhas
    blocos, atual, uso, cap_pag = [], "", 0, 37
    for p in cfg['partes']:
        for k, c in enumerate(p['capitulos']):
            custo = 2.2 + len(c.get('topicos', [])) + (2.2 if k == 0 else 0)
            if uso + custo > cap_pag and atual:
                blocos.append(atual); atual, uso, cap_pag = "", 0, 44
                if k > 0:
                    atual += f'<div class="part">{html.escape(p["nome"])} (continuação)</div>\n'; uso += 2.2
            if k == 0:
                atual += f'<div class="part">{html.escape(p["nome"])}</div>\n'
            atual += (f'<div class="chap"><span class="cn">{c["n"]}</span>{html.escape(c["titulo"])}'
                      f'<span class="dots"></span><span class="pg">{inicio[c["n"]]}</span></div>\n')
            atual += ''.join(f'<div class="sub">{html.escape(t)}</div>\n' for t in c.get('topicos', []))
            uso += custo
    blocos.append(atual)
    if len(blocos) != n_sum:
        print(f'AVISO: o sumário ocupou {len(blocos)} páginas; ajuste "paginas_sumario" para {len(blocos)} e rode de novo.', file=sys.stderr)
    for i, b in enumerate(blocos):
        if i == 0:
            top = (f'<div class="inner" style="top:14mm"><div style="display:flex;justify-content:space-between;align-items:center">'
                   f'<div class="brand" style="font-size:12pt">{MINI}{html.escape(titulo)}</div><div class="tema">Sumário</div></div>'
                   f'<h1 class="serif" style="font-size:24pt;font-weight:700;margin:3mm 0 0">O que você vai estudar</h1>')
            pages.append(f'<section class="page" style="--tema:{tema_cor}">{top}{b}</div>{foot(2)}</section>')
        else:
            b = b.replace('<div class="part">', '<div class="part" style="margin-top:0">', 1)
            pages.append(f'<section class="page">{run("Sumário")}<div class="inner">{b}</div>{foot(2+i)}</section>')

    # CAPÍTULOS
    escolhidos = set(x.strip() for x in a.capitulos.split(',')) if a.capitulos else None
    corpo = ''
    for p, c in caps:
        fp = frag_path(c)
        if not fp or (escolhidos and c['n'] not in escolhidos):
            continue
        fr = open(fp, encoding='utf-8').read()
        for k, v in ICON.items():
            fr = fr.replace(f'[[ICON_{k}]]', v)
        fr = fr.replace('[[MINI]]', MINI).replace('[[TITULO]]', html.escape(titulo)).replace('<!--RUN-->', run(c.get('tema', c['titulo'])))
        partes = fr.split('<!--FOOT-->'); n = inicio[c['n']]; out = []
        for i, parte in enumerate(partes):
            out.append(parte)
            if i < len(partes) - 1:
                out.append(foot(n)); n += 1
        corpo += ''.join(out)

    head = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{html.escape(titulo)}</title>'
            '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700'
            '&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">'
            f'<link rel="stylesheet" href="style.css"><style>:root{{--tema:{tema_cor}}}</style></head><body>\n')
    saida = a.saida or os.path.join(base, 'livro.html')
    open(saida, 'w', encoding='utf-8').write(head + '\n'.join(pages) + corpo + '</body></html>')
    print(f'ok: {saida} | último capítulo termina na página {pg-1}')

if __name__ == '__main__':
    main()
