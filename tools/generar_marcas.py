"""Genera las páginas por marca (Colnago, Pinarello, Kask, KOO, Sidi) con los productos de index.html.
Uso (desde la carpeta del sitio): python3 tools/generar_marcas.py
Vuelve a correrlo cada vez que agregues o cambies productos en index.html.
"""
import json, re, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from generar_paginas import HEADER, FOOTER, WA_FLOAT, FONTS, NEGOCIO, SITE, wa

productos = json.loads(subprocess.check_output(["node", "tools/productos.js", "index.html"]))

def valor(precio):
    d = re.sub(r"\D", "", precio or "")
    return int(d) if d else None

def tarjeta(p):
    nombre = f'{p["marca"]} {p["nombre"]}'
    foto = p.get("foto", "")
    badges = '<span class="prod-cat">%s</span>' % p["cat"]
    if p.get("antes"): badges += '<span class="prod-oferta">Oferta</span>'
    if p.get("test"): badges += '<span class="prod-test">Test ride</span>'
    if p.get("fit"): badges += '<span class="prod-fit">+ Bike fit gratis</span>'
    if p.get("ref"): badges += '<span class="prod-ref">*Imagen de referencia</span>'
    precio = p.get("precio") or ""
    precio_html = (f'<s>{p["antes"]}</s> ' if p.get("antes") else "") + (precio or "Precio según configuración")
    colores = f'<p class="prod-res">{len(p["variantes"])} colores disponibles</p>' if p.get("variantes") else ""
    tallas = f'<p class="prod-res">Tallas {p["tallas"][0]} a {p["tallas"][-1]}</p>' if p.get("tallas") else ""
    msg = p.get("wa") or (f"Hola Veloce, me interesa: {nombre}" + (f" ({precio})" if precio else ". ¿Qué configuraciones tienen?"))
    test = (f'<a class="btn btn-test" href="{wa(f"Hola Veloce, quiero agendar un test ride de la {nombre}. ¿Qué días tienen disponibles?")}">Agendar test ride</a>'
            if p.get("test") else "")
    return f"""<article class="prod">
      <div class="prod-img"><img src="/{foto}" alt="{nombre} en Veloce Medellín" loading="lazy">{badges}</div>
      <div class="prod-body">
        <div class="prod-brand">{p["marca"]}</div>
        <h3 class="prod-name">{p["nombre"]}</h3>
        {f'<p class="prod-res">{p["resumen"]}</p>' if p.get("resumen") else ""}{colores}{tallas}
        <div class="prod-price {'' if precio else 'consultar'}">{precio_html}</div>
        <a class="btn btn-solid" href="{wa(msg)}">{'Lo quiero' if precio else 'Cotizar'} · WhatsApp</a>
        {test}
      </div></article>"""

def ld_producto(p):
    it = {"@type": "Product", "name": f'{p["marca"]} {p["nombre"]}', "brand": {"@type": "Brand", "name": p["marca"]},
          "category": p["cat"], "image": f'{SITE}/{p.get("foto","")}', "description": p.get("resumen") or p.get("desc", "")}
    v = valor(p.get("precio"))
    if v:
        tipo_desde = (p.get("precio") or "").lower().startswith("desde")
        it["offers"] = ({"@type": "AggregateOffer", "lowPrice": v, "priceCurrency": "COP", "availability": "https://schema.org/InStock"}
                        if tipo_desde else
                        {"@type": "Offer", "price": v, "priceCurrency": "COP", "availability": "https://schema.org/InStock",
                         "seller": {"@type": "BicycleStore", "name": "Veloce"}})
    return it

def pagina(m):
    prods = [p for p in productos if p["marca"] == m["marca"]]
    grid = "".join(tarjeta(p) for p in prods)
    if prods:
        bloque_prod = f"""<div class="sec-head"><div><div class="tri"><i></i><i></i><i></i></div><h2 class="display">{m["titulo_prod"]}</h2></div>
      <p>Precios en pesos colombianos. Escríbenos por WhatsApp para confirmar disponibilidad, tallas y colores.</p></div>
    <div class="prod-grid">{grid}</div>"""
    else:
        bloque_prod = f"""<div class="sec-head"><div><div class="tri"><i></i><i></i><i></i></div><h2 class="display">{m["titulo_prod"]}</h2></div></div>
    <div class="side-card" style="position:static;max-width:640px"><h3>Cotiza tu {m["marca"]}</h3><p>{m["sin_prod"]}</p>
      <a class="btn btn-solid" href="{wa(m['cta_msg'])}">Cotizar por WhatsApp</a></div>"""
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in m["faqs"])
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
              {"@type": "ListItem", "position": 2, "name": m["miga"], "item": f'{SITE}/{m["slug"]}'}]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
              {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in m["faqs"]]}]
    if prods:
        ld.append({"@context": "https://schema.org", "@type": "ItemList", "name": m["miga"],
                   "itemListElement": [{"@type": "ListItem", "position": k + 1, "item": ld_producto(p)} for k, p in enumerate(prods)]})
    hero = "" if m.get("sin_foto") else f'<img class="ph-img" src="/{m["og"]}" alt="{m["miga"]} en Veloce, Medellín" style="object-fit:contain;object-position:center;background:#fff">'
    otras = "".join(f'<a href="/{o["slug"]}"><b>{o["miga"]}</b><span>{o["corto"]}</span></a>' for o in MARCAS if o["slug"] != m["slug"])
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{m["title"]}</title>
<meta name="description" content="{m["desc"]}">
<link rel="canonical" href="{SITE}/{m["slug"]}">
<meta property="og:type" content="website">
<meta property="og:title" content="{m["title"]}">
<meta property="og:description" content="{m["desc"]}">
<meta property="og:url" content="{SITE}/{m["slug"]}">
<meta property="og:image" content="{SITE}/{m["og"]}">
<meta property="og:locale" content="es_CO">
{FONTS}
<link rel="stylesheet" href="/css/estilos.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
{HEADER}

<section class="page-hero">{hero}
  <div class="wrap">
    <div class="crumbs"><a href="/">Inicio</a> / <a href="/#marcas">Marcas</a> / {m["miga"]}</div>
    <div class="tri on-dark"><i></i><i></i><i></i></div>
    <h1 class="display">{m["h1"]}</h1>
    <p>{m["intro"]}</p>
    <div class="hero-ctas"><a class="btn btn-light" href="{wa(m['cta_msg'])}">{m["cta"]}</a><a class="btn btn-ghost" href="#modelos">Ver modelos y precios</a></div>
  </div>
</section>

<section id="modelos">
  <div class="wrap">
    {bloque_prod}
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap page-grid">
    <article class="prose">
{m["cuerpo"]}
      <h2>¿Por qué comprar en Veloce?</h2>
      <ul>
{m["porque"]}
        <li><b>Asesoría de ciclistas:</b> te ayudamos a elegir según cómo y dónde montas.</li>
        <li><b>Taller propio</b> en la misma tienda para el armado, ajustes y mantenimiento.</li>
        <li><b>Tienda física en El Poblado</b>, en el Mall Campestre Drive Inn: ven a ver y probar antes de comprar.</li>
      </ul>
      <h2>Preguntas frecuentes</h2>
      <div class="faq">{faq_html}</div>
    </article>
    <aside class="side-card">
      <h3>{m["cta"]}</h3>
      <p>Te respondemos por WhatsApp con disponibilidad y precio.</p>
      <p><b>Dirección:</b> Calle 16A Sur #32B-38, Local 101, Mall Campestre Drive Inn, El Poblado, Medellín.</p>
      <p><b>Tienda:</b> lunes a viernes 10:00 AM – 7:00 PM · sábados 11:00 AM – 5:00 PM.</p>
      <a class="btn btn-solid" href="{wa(m['cta_msg'])}">{m["cta"]} · WhatsApp</a>
      <a class="btn btn-outline" href="https://www.google.com/maps/search/?api=1&query=Veloce+Mall+Campestre+Drive+Inn+Calle+16A+Sur+32B-38+Medell%C3%ADn">Abrir en Google Maps</a>
    </aside>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><div><div class="tri"><i></i><i></i><i></i></div><h2 class="display">Más marcas en Veloce.</h2></div></div>
    <div class="more-links">{otras}</div>
  </div>
</section>

{FOOTER}
{WA_FLOAT}
<script>
  document.querySelectorAll('#menu a').forEach(a=>a.addEventListener('click',()=>document.getElementById('menu').classList.remove('open')));
</script>
</body>
</html>
"""

FIT_BICI = '        <li><b>Bike fit Retül gratis</b> con tu bicicleta de más de $8.000.000: tu bici nueva queda ajustada a tu cuerpo desde el primer día. <a href="/bike-fit-retul-medellin">Ver cómo funciona</a>.</li>'
FIT_EQUIPO = '        <li><b>Pruébatelo en la tienda:</b> ven y elige la talla correcta antes de comprar.</li>'

MARCAS = [
  dict(slug="colnago-medellin", marca="Colnago", miga="Colnago", corto="Bicicletas de ruta italianas.",
       title="Bicicletas Colnago en Medellín | V5Rs, Y1Rs, V3 · Veloce",
       desc="Compra tu bicicleta Colnago en Medellín: V5Rs, Y1Rs y V3 con precios en pesos. Bike fit Retül gratis con tu bici. Tienda en El Poblado. Cotiza por WhatsApp.",
       h1="Bicicletas Colnago<br>en Medellín.", og="img/productos/v5rs-3.jpg",
       intro="La marca italiana con la que Tadej Pogačar ha ganado el Tour de Francia. Ven a conocer la V5Rs, la Y1Rs y la V3 en nuestra tienda de El Poblado.",
       cta="Cotizar mi Colnago", cta_msg="Hola Veloce, quiero cotizar una bicicleta Colnago",
       titulo_prod="Modelos Colnago.",
       cuerpo="""      <h2>Colnago: el ciclismo a la italiana</h2>
      <p>Colnago nació en 1954 en Cambiago, cerca de Milán, de la mano de Ernesto Colnago. Desde entonces sus bicicletas han ganado Grandes Vueltas, clásicas y campeonatos del mundo, y hoy son la bici de Tadej Pogačar y del UAE Team Emirates.</p>
      <h3>¿Qué Colnago es para ti?</h3>
      <ul>
        <li><b>V5Rs:</b> la Colnago de competencia más liviana, para quien quiere lo máximo en montaña y en carrera.</li>
        <li><b>Y1Rs:</b> la aero de Colnago, hecha para ir rápido en el plano y en los finales.</li>
        <li><b>V3:</b> una Colnago de carbono para entrenar y hacer gran fondos, con un precio más accesible.</li>
      </ul>
      <p>Si no sabes cuál te conviene, escríbenos o ven a la tienda: te asesoramos según cómo montas, y con el bike fit Retül elegimos la talla exacta.</p>""",
       porque=FIT_BICI, sin_prod="",
       faqs=[("¿Dónde comprar una Colnago en Medellín?", "En Veloce, en el Mall Campestre Drive Inn, El Poblado (Calle 16A Sur #32B-38, Local 101). Escríbenos por WhatsApp al +57 305 245 1204."),
             ("¿Cuánto cuesta una Colnago en Colombia?", "Depende del modelo y la configuración. En esta página ves los precios de los modelos que tenemos; para la V5Rs y la Y1Rs te cotizamos según el grupo y las ruedas que quieras."),
             ("¿La bicicleta incluye bike fit?", "Sí. Toda bicicleta de más de $8.000.000 que compres en Veloce incluye bike fit Retül gratis."),
             ("¿Qué talla de Colnago necesito?", "Con el bike fit Retül medimos tu cuerpo y tu posición para elegir la talla exacta antes de comprar.")]),
  dict(slug="pinarello-medellin", marca="Pinarello", miga="Pinarello", corto="Bicicletas de ruta de Treviso.",
       title="Bicicletas Pinarello en Medellín | F7 Ultegra Di2 en oferta · Veloce",
       desc="Pinarello F7 Ultegra Di2 en Medellín: antes $34.900.000, ahora $24.900.000, en 3 colores. Bike fit Retül gratis con tu bici. Tienda en El Poblado. Cotiza por WhatsApp.",
       h1="Bicicletas Pinarello<br>en Medellín.", og="img/productos/pinarello-f7-roja-1.jpg",
       intro="Desde Treviso, Italia, las bicicletas que han ganado las carreras más grandes del mundo. Llévate la F7 Ultegra Di2 con $10 millones de descuento en nuestra tienda de El Poblado.",
       cta="Cotizar mi Pinarello", cta_msg="Hola Veloce, quiero cotizar una bicicleta Pinarello",
       titulo_prod="Modelos Pinarello.",
       sin_prod="Te cotizamos el modelo y la configuración de Pinarello que quieras, desde la Dogma hasta las opciones de gravel. Escríbenos y te contamos disponibilidad, tiempos de entrega y precio.",
       cuerpo="""      <h2>Pinarello: diseño y velocidad desde 1952</h2>
      <p>Pinarello nació en Treviso, Italia, en 1952, fundada por Giovanni Pinarello. Sus bicicletas han ganado el Tour de Francia muchas veces y su modelo insignia, la Dogma, es una de las bicis de ruta más reconocidas del mundo.</p>
      <p>Una Pinarello se distingue por su diseño asimétrico, su rigidez y su manejo preciso en las bajadas. Es una bici para quien quiere sentir el ciclismo de alto nivel en cada salida.</p>
      <h3>Pinarello F7: el ADN de la Dogma</h3>
      <p>La F7 hereda de la Dogma F el diseño asimétrico, la geometría de competencia y la horquilla Onda. Con cuadro de carbono T900, Shimano Ultegra Di2 de 12 velocidades y frenos de disco, es la forma más directa de tener una Pinarello de carreras, y ahora está a <b>$24.900.000</b> (antes $34.900.000) en rojo y negro, azul y negro o negro mate.</p>
      <h3>Te ayudamos a elegir</h3>
      <p>Cuéntanos cómo montas, qué rutas haces y qué presupuesto tienes, y te recomendamos el modelo y la configuración. Con el bike fit Retül elegimos la talla exacta antes de pedirla.</p>""",
       porque=FIT_BICI,
       faqs=[("¿Dónde comprar una Pinarello en Medellín?", "En Veloce, en el Mall Campestre Drive Inn, El Poblado (Calle 16A Sur #32B-38, Local 101). Escríbenos por WhatsApp al +57 305 245 1204."),
             ("¿Cuánto cuesta una Pinarello en Colombia?", "Depende del modelo y la configuración. La Pinarello F7 Ultegra Di2 está en $24.900.000 (antes $34.900.000). Para otros modelos, escríbenos y te cotizamos."),
             ("¿La bicicleta incluye bike fit?", "Sí. Toda bicicleta de más de $8.000.000 que compres en Veloce incluye bike fit Retül gratis."),
             ("¿Qué talla de Pinarello necesito?", "Con el bike fit Retül medimos tu cuerpo y tu posición para elegir la talla exacta antes de pedir tu bici.")]),
  dict(slug="cascos-kask-medellin", marca="Kask", miga="Cascos Kask", corto="Cascos italianos de ruta y aero.",
       title="Cascos Kask en Medellín | Protone, Elemento, Mojito, Utopia · Veloce",
       desc="Cascos Kask en Medellín con precios en pesos: Protone Icon, Elemento, Mojito³, Sintesi y Utopia Y. Varios colores y tallas. Tienda en El Poblado. Pide el tuyo por WhatsApp.",
       h1="Cascos Kask<br>en Medellín.", og="img/productos/kask-protone-1.jpg",
       intro="Los cascos italianos que usa el INEOS Grenadiers. Protone Icon, Elemento, Mojito³, Sintesi y Utopia Y en varios colores y tallas.",
       cta="Pedir mi casco Kask", cta_msg="Hola Veloce, me interesa un casco Kask. ¿Qué modelos, colores y tallas tienen?",
       titulo_prod="Cascos Kask.", sin_prod="",
       cuerpo="""      <h2>¿Por qué un casco Kask?</h2>
      <p>Kask es una marca italiana de cascos que trabaja de la mano con equipos profesionales como el INEOS Grenadiers. Sus cascos combinan seguridad, ventilación y su ajuste Octo Fit, que se adapta a casi cualquier forma de cabeza.</p>
      <h3>¿Cuál elegir?</h3>
      <ul>
        <li><b>Protone Icon:</b> aero y ventilado a la vez, el casco todoterreno de los profesionales.</li>
        <li><b>Elemento:</b> el tope de gama de Kask, el más liviano y avanzado.</li>
        <li><b>Mojito³:</b> liviano, fresco y versátil para ruta, gravel o el día a día.</li>
        <li><b>Sintesi:</b> un Kask de calidad a un precio de entrada.</li>
        <li><b>Utopia Y:</b> el casco aerodinámico para ir lo más rápido posible.</li>
      </ul>""",
       porque=FIT_EQUIPO,
       faqs=[("¿Dónde comprar cascos Kask en Medellín?", "En Veloce, en el Mall Campestre Drive Inn, El Poblado. También puedes pedirlo por WhatsApp al +57 305 245 1204."),
             ("¿Qué talla de casco Kask necesito?", "Se mide el contorno de la cabeza un poco por encima de las cejas. Lo mejor es venir a la tienda y probártelo, o escríbenos y te ayudamos."),
             ("¿Tienen todos los colores?", "Cada modelo tiene varios colores. Escríbenos por WhatsApp y te confirmamos cuáles tenemos disponibles en tu talla.")]),
  dict(slug="gafas-koo-medellin", marca="KOO", miga="Gafas KOO", corto="Gafas de ciclismo de Kask.",
       title="Gafas KOO en Medellín | Alibi, Hype, Demos · Veloce",
       desc="Gafas de ciclismo KOO, la marca de gafas de Kask, en Medellín: Alibi Photochromic, Alibi, Hype y Demos con precios en pesos. Tienda en El Poblado.",
       h1="Gafas KOO<br>en Medellín.", og="img/productos/koo-alibi-1.jpg",
       intro="Las gafas de ciclismo de Kask con diseño italiano. Alibi Photochromic, Alibi, Hype y Demos.",
       cta="Pedir mis gafas KOO", cta_msg="Hola Veloce, me interesan unas gafas KOO. ¿Qué modelos tienen?",
       titulo_prod="Gafas KOO.", sin_prod="",
       cuerpo="""      <h2>KOO: las gafas de Kask</h2>
      <p>KOO es la marca de gafas de Kask. Lleva al ciclismo el mismo diseño y la misma calidad italiana de sus cascos, y sus gafas están pensadas para encajar perfecto con un casco Kask.</p>
      <h3>¿Cuáles elegir?</h3>
      <ul>
        <li><b>Alibi Photochromic:</b> el lente se oscurece o aclara solo según la luz, ideal para salir temprano o rodar entre sol y nubes.</li>
        <li><b>Alibi:</b> gran campo de visión con un diseño limpio.</li>
        <li><b>Hype y Demos:</b> gafas KOO con gran relación calidad-precio.</li>
      </ul>""",
       porque=FIT_EQUIPO,
       faqs=[("¿Dónde comprar gafas KOO en Medellín?", "En Veloce, en el Mall Campestre Drive Inn, El Poblado. También puedes pedirlas por WhatsApp al +57 305 245 1204."),
             ("¿Qué son unas gafas fotocromáticas?", "Son gafas cuyo lente se oscurece con el sol y se aclara cuando hay poca luz, así no tienes que cambiar de lente durante la salida."),
             ("¿KOO es de Kask?", "Sí. KOO es la marca de gafas de Kask y sus gafas están diseñadas para usarse con cascos Kask.")]),
  dict(slug="zapatillas-sidi-medellin", marca="Sidi", miga="Zapatillas Sidi", corto="Zapatillas de ciclismo italianas.",
       title="Zapatillas Sidi en Medellín | Shot 3, Wire 3 · Veloce",
       desc="Zapatillas de ciclismo Sidi en Medellín: Shot 3 y Wire 3 con precios en pesos, tallas 39 a 46 y varios colores. Tienda en El Poblado. Pide las tuyas por WhatsApp.",
       h1="Zapatillas Sidi<br>en Medellín.", og="img/productos/sidi-shot3-negro-1.jpg",
       intro="Zapatillas de ciclismo italianas hechas para durar. Shot 3 y Wire 3 en tallas 39 a 46 y varios colores.",
       cta="Pedir mis Sidi", cta_msg="Hola Veloce, me interesan unas zapatillas Sidi. ¿Qué tallas y colores tienen?",
       titulo_prod="Zapatillas Sidi.", sin_prod="",
       cuerpo="""      <h2>Sidi: zapatillas italianas desde 1960</h2>
      <p>Sidi fabrica zapatillas de ciclismo en Italia desde 1960. Son conocidas por su ajuste firme, su durabilidad y porque casi todas sus piezas se pueden reemplazar, así que te duran muchos años.</p>
      <h3>¿Cuáles elegir?</h3>
      <ul>
        <li><b>Shot 3:</b> la zapatilla de competencia de Sidi, rígida, liviana y con ajuste preciso.</li>
        <li><b>Wire 3:</b> la Sidi más técnica, con capellada ventilada y suela de carbono con rigidez 11.</li>
      </ul>
      <p>Si cambias de zapatillas, revisar la posición de las calas es clave. En Veloce podemos ajustarlas con el <a href="/bike-fit-retul-medellin">bike fit Retül</a>.</p>""",
       porque=FIT_EQUIPO,
       faqs=[("¿Dónde comprar zapatillas Sidi en Medellín?", "En Veloce, en el Mall Campestre Drive Inn, El Poblado. También puedes pedirlas por WhatsApp al +57 305 245 1204."),
             ("¿Qué tallas tienen?", "Manejamos tallas 39 a 46 (EU). Escríbenos y te confirmamos disponibilidad en tu talla y color."),
             ("¿Las Sidi son anchas o angostas?", "La horma de Sidi es más bien ajustada. Lo mejor es venir a probártelas a la tienda.")]),
]

if __name__ == "__main__":
    for m in MARCAS:
        open(f'{m["slug"]}.html', "w", encoding="utf-8").write(pagina(m))
        print("ok", m["slug"], len([p for p in productos if p["marca"] == m["marca"]]), "productos")
