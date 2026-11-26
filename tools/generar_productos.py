"""Genera una página por cada producto de index.html en la carpeta producto/ y actualiza sitemap.xml.
Uso (desde la carpeta del sitio): python3 tools/generar_productos.py
Vuelve a correrlo cada vez que agregues o cambies productos en index.html.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from generar_paginas import HEADER, FOOTER, WA_FLOAT, FONTS, SITE, wa
from generar_marcas import productos, MARCAS, slug_prod, url_prod, valor, ld_producto

# Las páginas de producto viven en /producto/, así que las rutas relativas del encabezado y el pie pasan a absolutas
HEADER, FOOTER = (re.sub(r'(src|href)="img/', r'\1="/img/', h) for h in (HEADER, FOOTER))

PAG_MARCA = {m["marca"]: m for m in MARCAS}

FITBOX = '<a class="fit-incl" href="/bike-fit-retul-medellin"><b>Bike fit Retül GRATIS con esta bicicleta</b><span>Te la entregamos ajustada a tu cuerpo con medición 3D. Ver cómo funciona</span></a>'

def bf_attr(p):
    """Precio de Black Friday: lo activa js/promo.js solo durante la campaña."""
    return f' data-bf="{p["bf"]}" data-normal="{p.get("antes") or p.get("precio")}"{" data-bf-sigue" if p.get("bfSigue") else ""}' if p.get("bf") else ""

TIPO = {"Ruta": "Bicicleta de ruta", "Gravel": "Bicicleta gravel", "MTB": "Bicicleta MTB",
        "E-MTB": "Bicicleta eléctrica de montaña", "E-Ruta": "Bicicleta eléctrica de ruta", "Casco": "Casco", "Casco aero": "Casco aero",
        "Gafas": "Gafas", "Zapatillas": "Zapatillas", "Ciclocomputador": "Ciclocomputador", "Pedales": "Pedales de ruta", "Sillines": "Sillín"}

def nombre_largo(p):
    """'Bicicleta de ruta Colnago V3 Black Edition', 'Casco Kask Mojito³', 'Zapatillas Sidi MTB Speed'..."""
    base = f'{p["marca"]} {p["nombre"]}'
    t = TIPO.get(p["cat"], "")
    return f"{t} {base}" if t else base

def articulo(p):
    return "la" if p["cat"] in ("Ruta", "Gravel", "MTB", "E-MTB", "E-Ruta") else ""

def fotos_de(p):
    if p.get("variantes"):
        return [f for v in p["variantes"] for f in v["fotos"]]
    return [f for f in (p.get("fotos") or [p.get("foto")]) if f]

def guia_html(p):
    g = p.get("guia")
    if not g: return ""
    head = "".join(f"<th>{c}</th>" for c in g["cols"])
    filas = "".join('<tr%s><th>%s</th>%s</tr>' % (' class="g-alt"' if f[0].startswith("Estatura") else "", f[0],
                    "".join(f"<td>{v}</td>" for v in f[1:])) for f in g["filas"])
    nota = f'<p class="g-nota">{g["nota"]}</p>' if g.get("nota") else ""
    return f'<details class="m-guia" open><summary>Guía de tallas</summary><div class="g-wrap"><table><thead><tr><th></th>{head}</tr></thead><tbody>{filas}</tbody></table></div>{nota}</details>'

def tarjeta_mini(p):
    precio = p.get("precio") or "Precio según configuración"
    return f"""<a class="prod" href="{url_prod(p)}">
      <div class="prod-img"><img src="/{p.get("foto","")}" alt="{p["marca"]} {p["nombre"]}" loading="lazy"><span class="prod-cat">{p["cat"]}</span></div>
      <div class="prod-body"><div class="prod-brand">{p["marca"]}</div><div class="prod-name">{p["nombre"]}</div>
      <div class="prod-price {'' if p.get("precio") else 'consultar'}"{bf_attr(p)}>{precio}</div></div></a>"""

def relacionados(p):
    misma = [x for x in productos if x is not p and x["marca"] == p["marca"]]
    otros = [x for x in productos if x is not p and x["marca"] != p["marca"] and x["cat"] == p["cat"]]
    return (misma + otros)[:4]

def pagina(p):
    slug, url = slug_prod(p), SITE + url_prod(p)
    nombre, largo = f'{p["marca"]} {p["nombre"]}', nombre_largo(p)
    precio, antes = p.get("precio") or "", p.get("antes") or ""
    fotos = fotos_de(p) or ["img/logo-negro.png"]
    marca = PAG_MARCA.get(p["marca"])

    title = f"{largo} en Medellín" + (f" · {precio}" if precio else "") + " | Veloce"
    desc = (p.get("resumen") or "").rstrip(".") + "."
    desc += f" {precio} en Veloce, El Poblado, Medellín." if precio else " Cotízala en Veloce, El Poblado, Medellín."
    if p.get("fit"): desc += " Incluye bike fit Retül gratis."
    desc += " Envío a toda Colombia."

    msg = p.get("wa") or (f"Hola Veloce, me interesa {articulo(p)} {nombre} ({precio})".replace("  ", " ") if precio
                          else f"Hola Veloce, quiero cotizar {articulo(p)} {nombre}. ¿Qué configuraciones tienen?".replace("  ", " "))
    test_msg = f"Hola Veloce, quiero agendar un test ride de la {nombre}. ¿Qué días tienen disponibles?"

    # ----- datos estructurados -----
    prod_ld = ld_producto(p, url) if valor(precio) else {
        "@type": "Product", "name": nombre, "brand": {"@type": "Brand", "name": p["marca"]}, "category": p["cat"], "url": url}
    prod_ld = {"@context": "https://schema.org", **prod_ld, "sku": slug.upper(),
               "image": [f"{SITE}/{f}" for f in fotos[:8]], "description": p.get("desc") or p.get("resumen", "")}
    migas = [("Inicio", SITE + "/")]
    if marca: migas.append((marca["miga"], f'{SITE}/{marca["slug"]}'))
    migas.append((nombre, url))
    ld = [prod_ld, {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": n, "item": u} for k, (n, u) in enumerate(migas)]}]

    # ----- bloques -----
    crumbs = '<a href="/">Inicio</a> / ' + (f'<a href="/{marca["slug"]}">{marca["miga"]}</a> / ' if marca
             else '<a href="/#productos">Productos</a> / ') + p["nombre"]
    thumbs = "".join(f'<img src="/{f}" data-f="/{f}" class="{"" if k else "on"}" alt="{nombre}, foto {k+1}" loading="lazy">'
                     for k, f in enumerate(p["variantes"][0]["fotos"] if p.get("variantes") else fotos))
    colores = ""
    if p.get("variantes"):
        sw = "".join(f'<button class="sw sw-lg {"" if k else "on"}" title="{v["color"]}" aria-label="{v["color"]}" style="background:{v["hex"]}" data-k="{k}"></button>'
                     for k, v in enumerate(p["variantes"]))
        colores = f'<div class="m-opt"><h4>Color: <span id="pp-color">{p["variantes"][0]["color"]}</span></h4><div class="sw-row">{sw}</div></div>'
    tallas = ""
    if p.get("tallas"):
        tb = "".join(f'<button class="t-btn" data-t="{t}">{t}</button>' for t in p["tallas"])
        tallas = f'<div class="m-opt"><h4>{"Ancho" if p["cat"] == "Sillines" else "Talla"}{" (EU)" if p["cat"] == "Zapatillas" else ""}</h4><div class="t-row">{tb}</div></div>'
    specs = "".join(f"<li>{x}</li>" for x in p.get("specs") or [])
    if p.get("fit"): specs += '<li><b style="color:#1e9be0">Incluye bike fit Retül GRATIS</b></li>'
    precio_html = (f"<s>{antes}</s> " if antes else "") + (precio or "Precio según configuración")
    test_btn = f'<a class="btn btn-test" href="{wa(test_msg)}">Agendar test ride</a>' if p.get("test") else ""
    test_txt = '<p class="m-test">🚵 Tenemos esta bici disponible para test ride. Agenda tu prueba, ven a montarla y llévate una nueva.</p>' if p.get("test") else ""
    ref = '<p class="m-ref">*Imagen de referencia</p>' if p.get("ref") else ""

    ventajas = []
    if p.get("fit"):
        ventajas.append('<li><b>Bike fit Retül gratis:</b> tu bici nueva queda ajustada a tu cuerpo desde el primer día. <a href="/bike-fit-retul-medellin">Ver cómo funciona</a>.</li>')
    if (valor(precio) or 0) >= 399000:
        ventajas.append('<li><b>Envío gratis a toda Colombia.</b> <a href="/envios-y-devoluciones">Ver envíos y devoluciones</a>.</li>')
    else:
        ventajas.append('<li><b>Envíos a toda Colombia.</b> <a href="/envios-y-devoluciones">Ver envíos y devoluciones</a>.</li>')
    ventajas.append('<li><b>Paga como prefieras:</b> efectivo, transferencia y tarjetas de crédito o débito.</li>')
    ventajas.append('<li><b>Tienda física en El Poblado:</b> Mall Campestre Drive Inn, Calle 16A Sur #32B-38, Local 101. Ven a verlo y probarlo antes de comprar.</li>')
    ventajas.append('<li><b>Taller propio</b> en la misma tienda para el armado, los ajustes y el mantenimiento. <a href="/taller-de-bicicletas-medellin">Ver el taller</a>.</li>')

    rel = relacionados(p)
    rel_html = ""
    if rel:
        mas = f'<a class="btn btn-outline" href="/{marca["slug"]}">Ver todo {marca["miga"]}</a>' if marca else '<a class="btn btn-outline" href="/#productos">Ver todos los productos</a>'
        rel_html = f"""<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><div><div class="tri"><i></i><i></i><i></i></div><h2 class="display">También te puede interesar.</h2></div>{mas}</div>
    <div class="prod-grid">{"".join(tarjeta_mini(x) for x in rel)}</div>
  </div>
</section>"""

    datos_js = json.dumps({"nombre": nombre, "variantes": [{"color": v["color"], "fotos": ["/" + f for f in v["fotos"]]} for v in p.get("variantes") or []],
                           "wa": "573052451204"}, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-BCTKZM82SJ"></script>
<script src="/js/analytics.js"></script>
<script src="/js/promo.js"></script>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="product">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{fotos[0]}">
<meta property="og:locale" content="es_CO">
{FONTS}
<link rel="stylesheet" href="/css/estilos.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
{HEADER}

<section class="pp">
  <div class="wrap">
    <div class="pp-crumbs">{crumbs}</div>
    <div class="pp-grid">
      <div class="m-gal"><img id="m-main" src="/{fotos[0]}" alt="{largo} en Veloce, Medellín">{ref}<div class="m-thumbs">{thumbs}</div></div>
      <div class="m-info">
        <div class="prod-brand">{p["marca"]} · {p["cat"]}</div>
        <h1 class="display">{p["nombre"]}</h1>
        <div class="prod-price {'' if precio else 'consultar'}"{bf_attr(p)}>{precio_html}</div>{FITBOX if p.get("fit") else ""}
        <p>{p.get("desc") or p.get("resumen", "")}</p>
        {colores}{tallas}{guia_html(p)}
        <div class="m-ctas"><a class="btn btn-solid" id="m-wa" href="{wa(msg)}">{'Lo quiero · WhatsApp' if precio else 'Cotizar mi configuración'}</a>{test_btn}</div>{test_txt}
      </div>
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap page-grid">
    <article class="prose">
      <h2>Características</h2>
      <ul class="pp-specs">{specs}</ul>
      <h2>¿Por qué comprar en Veloce?</h2>
      <ul>
        {"".join(ventajas)}
      </ul>
    </article>
    <aside class="side-card">
      <h3>¿Dudas? Escríbenos</h3>
      <p>Te respondemos por WhatsApp con disponibilidad, tallas y colores.</p>
      <p><b>Dirección:</b> Calle 16A Sur #32B-38, Local 101, Mall Campestre Drive Inn, El Poblado, Medellín.</p>
      <p><b>Tienda:</b> lunes a viernes 10:00 AM – 7:00 PM · sábados 11:00 AM – 5:00 PM.</p>
      <a class="btn btn-solid" href="{wa(msg)}">Escribir por WhatsApp</a>
      <a class="btn btn-outline" href="https://www.google.com/maps/search/?api=1&query=Veloce+Mall+Campestre+Drive+Inn+Calle+16A+Sur+32B-38+Medell%C3%ADn">Abrir en Google Maps</a>
    </aside>
  </div>
</section>

{rel_html}

{FOOTER}
{WA_FLOAT}
<script>
(function(){{
  var P={datos_js}, vk=0, talla=null, main=document.getElementById('m-main'), box=document.querySelector('.m-thumbs');
  function thumbs(){{box.querySelectorAll('img').forEach(function(t){{t.onclick=function(){{main.src=t.dataset.f;box.querySelectorAll('img').forEach(function(x){{x.classList.remove('on')}});t.classList.add('on')}}}})}}
  function updWA(){{ if(!P.variantes.length&&!talla) return;
    var txt='Hola Veloce, me interesa: '+P.nombre+(P.variantes.length?' · color '+P.variantes[vk].color:'')+(talla?' · talla '+talla:'')+'. ¿Está disponible?';
    document.getElementById('m-wa').href='https://wa.me/'+P.wa+'?text='+encodeURIComponent(txt); }}
  document.querySelectorAll('.pp .sw').forEach(function(b){{b.onclick=function(){{ vk=+b.dataset.k; var f=P.variantes[vk].fotos;
    document.querySelectorAll('.pp .sw').forEach(function(x){{x.classList.toggle('on',x===b)}});
    document.getElementById('pp-color').textContent=P.variantes[vk].color; main.src=f[0];
    box.innerHTML=f.map(function(x,j){{return '<img src="'+x+'" data-f="'+x+'" class="'+(j?'':'on')+'" alt="">'}}).join(''); thumbs(); updWA(); }}}});
  document.querySelectorAll('.pp .t-btn').forEach(function(b){{b.onclick=function(){{ talla=b.dataset.t; document.querySelectorAll('.pp .t-btn').forEach(function(x){{x.classList.toggle('on',x===b)}}); updWA(); }}}});
  thumbs();
  document.querySelectorAll('#menu a').forEach(function(a){{a.addEventListener('click',function(){{document.getElementById('menu').classList.remove('open')}})}});
}})();
</script>
</body>
</html>
"""

def sitemap():
    """Reescribe sitemap.xml con las páginas fijas, las de marca y las de producto."""
    fijas = [("", "weekly", "1.0"), ("outlet", "daily", "0.9")]
    fijas += [(m["slug"], "weekly", "0.9") for m in MARCAS]
    fijas += [("bike-fit-retul-medellin", "monthly", "0.8"), ("taller-de-bicicletas-medellin", "monthly", "0.8"),
              ("centro-de-entrenamiento-ciclismo-medellin", "monthly", "0.7")]
    fijas += [(url_prod(p).lstrip("/"), "weekly", "0.8") for p in productos]
    fijas += [("envios-y-devoluciones", "yearly", "0.4"), ("como-comprar", "yearly", "0.4"), ("terminos", "yearly", "0.4"), ("privacidad", "yearly", "0.4")]
    filas = "\n".join(f"  <url><loc>{SITE}/{s}</loc><changefreq>{c}</changefreq><priority>{pr}</priority></url>" for s, c, pr in fijas)
    open("sitemap.xml", "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{filas}\n</urlset>\n')
    return len(fijas)

if __name__ == "__main__":
    os.makedirs("producto", exist_ok=True)
    vistos = set()
    for p in productos:
        s = slug_prod(p)
        assert s not in vistos, f"slug repetido: {s}"
        vistos.add(s)
        open(f"producto/{s}.html", "w", encoding="utf-8").write(pagina(p))
    for f in os.listdir("producto"):  # borra páginas de productos que ya no existen
        if f.endswith(".html") and f[:-5] not in vistos:
            os.remove(os.path.join("producto", f))
    print("ok", len(vistos), "páginas de producto ·", sitemap(), "URLs en sitemap.xml")
