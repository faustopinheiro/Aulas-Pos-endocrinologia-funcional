#!/usr/bin/env python3
"""Renumera as citações de um fragmento de capítulo na ordem de aparição (Vancouver).

Uso: python3 refs_fix.py cap12.html [itens_por_pagina=14]

- Lê todas as <sup>n,m</sup> do texto e todos os <li><span class="rn">n</span>...
  das listas <ol class="bib">, renumera pela ordem da primeira citação e reescreve
  as sup e a lista. Referências nunca citadas vão para o fim (o script avisa).
- Se a lista passar de itens_por_pagina, cria/recria a página
  "Referências bibliográficas (continuação)".
Ao adicionar uma referência nova, use qualquer número provisório único (ex.: 99)
na <sup> e no <li>, e rode o script.
"""
import sys,re
f=sys.argv[1]; per=int(sys.argv[2]) if len(sys.argv)>2 else 14
s=open(f,encoding='utf-8').read()
# remove página de continuação, juntando itens
cont=s.find('<h2>Referências bibliográficas (continuação)</h2>')
items_all=re.findall(r'<li><span class="rn">(\d+)</span><span>(.*?)</span></li>',s,flags=re.S)
if cont!=-1:
    a=s.rfind('<section class="page">',0,cont); b=s.index('</section>',cont)+len('</section>')
    s=s[:a].rstrip()+'\n'+s[b:]
bi=s.index('<ol class="bib">'); be=s.index('</ol>',bi)
body=s[:bi]; tail=s[be:]
refs=dict(items_all)
order=[]
for m in re.finditer(r'<sup>([\d,\s]+)</sup>',body):
    for x in m.group(1).split(','):
        x=x.strip()
        if x and x not in order: order.append(x)
missing=[k for k in refs if k not in order]
order+=missing
mp={o:str(i+1) for i,o in enumerate(order)}
body=re.sub(r'<sup>([\d,\s]+)</sup>',lambda m:'<sup>'+','.join(mp[x.strip()] for x in m.group(1).split(','))+'</sup>',body)
lis=[f'\n      <li><span class="rn">{mp[o]}</span><span>{refs[o]}</span></li>' for o in order]
first=''.join(lis[:per]); rest=''.join(lis[per:])
if rest:
    sec_end=tail.index('</section>')+len('</section>')
    tail2=tail[:sec_end]+'\n\n<section class="page">\n  <!--RUN-->\n  <div class="inner">\n    <h2>Referências bibliográficas (continuação)</h2>\n    <ol class="bib">'+rest+'\n    </ol>\n  </div>\n  <!--FOOT-->\n</section>'+tail[sec_end:]
else: tail2=tail
s=body+'<ol class="bib">'+first+'\n    '+tail2
open(f,'w',encoding='utf-8').write(s)
print('refs',len(order),'não citadas',missing)
