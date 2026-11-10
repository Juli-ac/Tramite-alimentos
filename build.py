# -*- coding: utf-8 -*-
"""Genera el sitio estático en ./sitio. Uso: python3 build.py"""
import json, os, shutil, html
from fichas import FICHAS, BLOQUES, NOVEDADES, REVISION, MARVIA

NOMBRE = "TrámiteAlimentos"
LEMA = "Trámites de alimentos de la Provincia de Buenos Aires, en un solo lugar"
OUT = "sitio"
E = html.escape
F = {f["slug"]: f for f in FICHAS}

def chip(estado):
    return ('<span class="chip ok">✅ Verificada</span>' if estado == "ok"
            else '<span class="chip rev">⚠️ En revisión</span>')

def header(base, activo=""):
    grupos = ""
    for b, nombre, _ in BLOQUES:
        links = "".join(f'<a href="{base}guias/{f["slug"]}.html">{f["icono"]} {E(f["titulo"].split(":")[0])}</a>'
                        for f in FICHAS if f["bloque"] == b)
        grupos += f'<div><h4>{E(nombre)}</h4>{links}</div>'
    return f'''<header class="top"><div class="wrap">
<a class="logo" href="{base}index.html"><span>TA</span>{NOMBRE}</a>
<button class="burger" aria-label="Abrir menú" aria-expanded="false">☰</button>
<nav class="menu" aria-label="Principal">
  <div class="search" data-search><input type="search" placeholder="Buscar trámite…" aria-label="Buscar trámite"><div class="results"></div></div>
  <div class="drop"><button aria-expanded="false" aria-haspopup="true">Trámites</button><div class="drop-panel">{grupos}<div style="grid-column:1/-1;border-top:1px solid var(--borde);padding-top:8px"><a href="{base}guias/index.html"><b>Ver todas las fichas →</b></a></div></div></div>
  <a href="{base}que-necesito.html">¿Qué necesito?</a>
  <a href="{base}novedades.html">Novedades</a>
  <a class="cta" href="{MARVIA}" target="_blank" rel="noopener">Asesoría</a>
</nav></div></header>'''

def footer(base):
    return f'''<footer><div class="wrap">
<div><h4>{NOMBRE}</h4><p>{E(LEMA)}. Información práctica y actualizada para emprendedores, PyMEs e ingenieros en alimentos.</p></div>
<div><h4>Secciones</h4><ul><li><a href="{base}guias/index.html">Fichas de trámites</a></li><li><a href="{base}que-necesito.html">¿Qué necesito?</a></li><li><a href="{base}novedades.html">Novedades</a></li></ul></div>
<div><h4>¿Necesitás ayuda?</h4><ul><li><a href="{MARVIA}" target="_blank" rel="noopener">Asesoría profesional (MARVIA)</a></li></ul></div>
<p class="aviso">La información de este sitio es orientativa y se revisa periódicamente. No reemplaza la consulta con la autoridad sanitaria ni el asesoramiento profesional. Verificá siempre los requisitos vigentes en las fuentes oficiales enlazadas en cada ficha. Última revisión general: {REVISION}.</p>
</div></footer>'''

def page(base, title, desc, body, activo=""):
    return f'''<!DOCTYPE html>
<html lang="es-AR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<link rel="stylesheet" href="{base}assets/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='22' fill='%230e5a47'/><text x='50' y='66' font-size='48' text-anchor='middle' fill='white' font-family='Arial' font-weight='bold'>TA</text></svg>">
</head><body data-base="{base}">
{header(base, activo)}
<main>{body}</main>
{footer(base)}
<script src="{base}assets/search-index.js"></script>
<script src="{base}assets/app.js"></script>
</body></html>'''

def card(f, base):
    key = f'{f["titulo"]} {f["palabras"]} {f["resumen"]}'
    return (f'<a class="card" href="{base}guias/{f["slug"]}.html" data-ficha="{E(key)}">'
            f'<span class="ico">{f["icono"]}</span><h3>{E(f["titulo"])}</h3><p>{E(f["resumen"])}</p>{chip(f["estado"])}</a>')

def bloques_html(base):
    s = ""
    for b, nombre, desc in BLOQUES:
        cards = "".join(card(f, base) for f in FICHAS if f["bloque"] == b)
        s += f'<div data-bloque="{b}"><div class="bloque-tit"><h3>{E(nombre)}</h3><span>{E(desc)}</span></div><div class="grid">{cards}</div></div>'
    return s

def novedades_html(base, n=None):
    items = NOVEDADES[:n] if n else NOVEDADES
    return '<div class="nov">' + "".join(
        f'<a href="{base}guias/{slug}.html"><time>{E(fecha)}</time><div><b>{E(t)}</b><small>{E(d)}</small></div></a>'
        for fecha, t, d, slug in items) + '</div>'

def asesoria_box():
    return f'''<div class="asesoria"><div><h3>¿Preferís que lo hagamos juntos?</h3><p>Asesoría profesional de un ingeniero en alimentos para PUPAA, RNE, RNPA y rotulado.</p></div>
<a class="btn btn-ambar" href="{MARVIA}" target="_blank" rel="noopener">Pedir asesoría →</a></div>'''

# ---------- Inicio
def build_index():
    base = ""
    body = f'''
<section class="hero"><div class="wrap">
  <div class="eyebrow">Guía práctica · Provincia de Buenos Aires</div>
  <h1>Todos los trámites de alimentos, en un solo lugar y actualizados.</h1>
  <p>Fichas claras sobre PUPAA, RNE, RNPA, rotulado y más: qué pide cada trámite, dónde se hace, cuánto tarda y en qué se equivoca la mayoría.</p>
  <div class="hero-search" data-search><input type="search" placeholder="¿Qué trámite buscás? Ej: registrar un producto" aria-label="Buscar trámite"><div class="results"></div></div>
  <div class="acciones"><a class="btn btn-ambar" href="que-necesito.html">Quiero vender un alimento → ¿qué necesito?</a></div>
</div></section>

<section class="blk"><div class="wrap">
  <h2 class="tit">Fichas de trámites</h2>
  <p class="sub">Cada ficha indica su fecha de revisión y si está ✅ verificada o ⚠️ en revisión.</p>
  {bloques_html(base)}
</div></section>

<section class="blk" style="padding-top:0"><div class="wrap">
  <div class="guia-cta"><div><h3>🧭 ¿No sabés por dónde empezar?</h3><p>Respondé 4 preguntas y te mostramos los trámites en el orden en que te conviene hacerlos.</p></div><a class="btn btn-verde" href="que-necesito.html">Armar mi ruta →</a></div>
</div></section>

<section class="blk" style="padding-top:0"><div class="wrap">
  <h2 class="tit">Novedades</h2>
  <p class="sub">Cambios normativos explicados en simple.</p>
  {novedades_html(base, 3)}
  <p style="margin-top:14px"><a href="novedades.html">Ver todas las novedades →</a></p>
</div></section>

<section class="blk" style="padding-top:0"><div class="wrap">{asesoria_box()}</div></section>
'''
    return page(base, f"{NOMBRE} | {LEMA}",
                "Guía práctica y actualizada de trámites alimentarios en la Provincia de Buenos Aires: PUPAA, RNE, RNPA, rotulado, carnet de manipulador y más.", body)

# ---------- Listado de fichas
def build_guias():
    base = "../"
    body = f'''<section class="blk"><div class="wrap">
<h1 class="tit" style="font-size:2rem;margin:0 0 6px">Fichas de trámites</h1>
<p class="sub">Provincia de Buenos Aires · Última revisión general: {REVISION}</p>
<div class="filtro"><input id="filtro" type="search" placeholder="Filtrar fichas (ej: etiqueta, carnet, DIPA)…" aria-label="Filtrar fichas"></div>
{bloques_html(base)}
</div></section>
<section class="blk" style="padding-top:0"><div class="wrap">{asesoria_box()}</div></section>'''
    return page(base, f"Fichas de trámites | {NOMBRE}", "Todas las fichas de trámites alimentarios de la Provincia de Buenos Aires.", body)

# ---------- Ficha
def lista(items, cls=""):
    return f'<ul class="{cls}">' + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul>"

def build_ficha(f):
    base = "../"
    bloque = dict((b, n) for b, n, _ in BLOQUES)[f["bloque"]]
    filas = "".join(f"<tr><th>{E(k)}</th><td>{E(v)}</td></tr>" for k, v in f["ante"])
    nota = f'<p class="nota">{E(f["requisitos_nota"])}</p>' if f["requisitos_nota"] else ""
    pasos = "<ol>" + "".join(f"<li>{E(p)}</li>" for p in f["pasos"]) + "</ol>"
    fuentes = "<ul class='fuentes'>" + "".join(
        f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a></li>' for t, u in f["fuentes"]) + "</ul>"
    rel = "".join(card(F[s], base) for s in f["relacionadas"] if s in F)
    is_cmp = f["slug"] == "cual-me-corresponde"
    t_quien = "¿Para quién es?"
    t_ante = "Las tres opciones" if is_cmp else "¿Ante quién se hace?"
    t_req = "Preguntas para decidir" if is_cmp else "Qué tener listo"
    t_pasos = "El recorrido típico" if is_cmp else "Paso a paso"
    secciones = [
        ("quien", "👥", t_quien, lista(f["quien"])),
        ("ante", "🏛️", t_ante, f'<table class="datos">{filas}</table>'),
        ("requisitos", "📋", t_req, lista(f["requisitos"], "" if is_cmp else "check") + nota),
        ("pasos", "🪜", t_pasos, pasos),
    ]
    toc = "".join(f'<a href="#{i}">{ic} {E(t)}</a>' for i, ic, t, _ in secciones)
    toc += '<a href="#costos">💲 Costos y plazos</a><a href="#errores">⚠️ Errores frecuentes</a><a href="#normativa">📚 Normativa y fuentes</a>'
    secs = "".join(f'<div class="sec" id="{i}"><h2>{ic} {E(t)}</h2>{c}</div>' for i, ic, t, c in secciones)
    body = f'''<div class="wrap">
<div class="migas"><a href="../index.html">Inicio</a> › <a href="index.html">Fichas</a> › {E(bloque)}</div>
<div class="ficha-head">
  <div class="meta">{chip(f["estado"])}<span>Última revisión: <b>{REVISION}</b></span><span>· Provincia de Buenos Aires</span></div>
  <h1>{f["icono"]} {E(f["titulo"])}</h1>
</div>
<div class="resumen">{E(f["resumen"])}</div>
<p class="leyenda">✅ = verificado en fuente oficial · ⚠️ = a confirmar con la autoridad o el documento oficial vigente</p>
<div class="ficha-layout">
<article>
{secs}
<div class="dos" id="costos" style="scroll-margin-top:84px;margin:18px 0">
  <div class="sec"><h2>💲 Costos</h2><p style="margin:0">{E(f["costos"])}</p></div>
  <div class="sec"><h2>⏱️ Plazos</h2><p style="margin:0">{E(f["plazos"])}</p></div>
</div>
<div class="sec" id="errores"><h2>⚠️ Errores frecuentes</h2>{lista(f["errores"], "err")}</div>
<div class="sec" id="normativa"><h2>📚 Normativa</h2>{lista(f["normativa"])}<h2 style="margin-top:18px">🔗 Fuentes oficiales</h2>{fuentes}</div>
{asesoria_box()}
<h2 class="tit" style="margin-top:36px;font-size:1.3rem">Fichas relacionadas</h2>
<div class="grid" style="margin-top:12px">{rel}</div>
</article>
<aside class="toc"><b>En esta ficha</b>{toc}</aside>
</div></div>'''
    return page(base, f'{f["titulo"]} en PBA | {NOMBRE}', f["resumen"], body)

# ---------- ¿Qué necesito?
def opt(name, value, label):
    return f'<label><input type="radio" name="{name}" value="{value}">{E(label)}</label>'

def build_que_necesito():
    base = ""
    body = f'''<section class="blk"><div class="wrap">
<h1 class="tit" style="font-size:2rem;margin:0 0 6px">🧭 ¿Qué necesito para vender mi alimento?</h1>
<p class="sub">Respondé 4 preguntas y te mostramos qué trámites hacer y en qué orden.</p>
<form class="quiz" id="quiz" onsubmit="return false">
  <div class="q"><b>1. ¿Cómo es tu producción?</b><div class="opts">
    {opt("escala","artesanal","Artesanal, de pequeña escala")}{opt("escala","pyme","PyME o industrial")}{opt("escala","terceros","Lo elabora otra planta por mí")}</div></div>
  <div class="q"><b>2. ¿Dónde querés vender?</b><div class="opts">
    {opt("venta","local","En mi zona o en la provincia")}{opt("venta","pais","En todo el país, cadenas o distribuidores")}{opt("venta","exporta","También quiero exportar")}</div></div>
  <div class="q"><b>3. ¿Ya tenés el local habilitado por el municipio?</b><div class="opts">
    {opt("local","si","Sí")}{opt("local","no","No / no sé")}</div></div>
  <div class="q"><b>4. ¿Tu producto es sin TACC, suplemento dietario o bebida hídrica (agua, hielo, etc.)?</b><div class="opts">
    {opt("especial","si","Sí")}{opt("especial","no","No")}</div></div>
  <div class="ruta" id="ruta" data-asesoria="{MARVIA}"></div>
</form>
</div></section>'''
    return page(base, f"¿Qué necesito? | {NOMBRE}", "Ruta guiada: qué trámites necesitás para vender tu alimento en la Provincia de Buenos Aires.", body)

def build_novedades():
    base = ""
    body = f'''<section class="blk"><div class="wrap">
<h1 class="tit" style="font-size:2rem;margin:0 0 6px">📰 Novedades</h1>
<p class="sub">Cambios normativos que afectan a los trámites alimentarios, explicados en simple.</p>
{novedades_html(base)}
</div></section>
<section class="blk" style="padding-top:0"><div class="wrap">{asesoria_box()}</div></section>'''
    return page(base, f"Novedades | {NOMBRE}", "Novedades normativas sobre trámites alimentarios en Argentina y la Provincia de Buenos Aires.", body)

def build_404():
    body = '''<section class="blk"><div class="wrap" style="text-align:center">
<h1 class="tit">No encontramos esa página</h1><p class="sub">Probá con el buscador o volvé al inicio.</p>
<a class="btn btn-verde" href="index.html">Ir al inicio</a></div></section>'''
    return page("", f"Página no encontrada | {NOMBRE}", "", body)

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(f"{OUT}/guias"); os.makedirs(f"{OUT}/assets")
    for a in ("style.css", "app.js"):
        shutil.copy(f"assets/{a}", f"{OUT}/assets/{a}")
    idx = [dict(s=f["slug"], t=f["titulo"], i=f["icono"], u=f"guias/{f['slug']}.html", r=f["resumen"], k=f["palabras"]) for f in FICHAS]
    idx += [dict(s="_ruta", t="¿Qué necesito? Ruta guiada", i="🧭", u="que-necesito.html", r="Respondé 4 preguntas y te mostramos qué trámites hacer.", k="empezar ruta guiada que necesito vender alimento"),
            dict(s="_nov", t="Novedades normativas", i="📰", u="novedades.html", r="Cambios normativos explicados en simple.", k="novedades cambios normativa"),]
    with open(f"{OUT}/assets/search-index.js", "w", encoding="utf-8") as fh:
        fh.write("window.SEARCH_INDEX=" + json.dumps(idx, ensure_ascii=False) + ";")
    pages = {"index.html": build_index(), "guias/index.html": build_guias(),
             "que-necesito.html": build_que_necesito(), "novedades.html": build_novedades(), "404.html": build_404()}
    for f in FICHAS: pages[f"guias/{f['slug']}.html"] = build_ficha(f)
    for p, c in pages.items():
        with open(f"{OUT}/{p}", "w", encoding="utf-8") as fh: fh.write(c)
    print(f"OK: {len(pages)} páginas")

if __name__ == "__main__":
    main()
