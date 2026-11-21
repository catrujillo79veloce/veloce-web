"""Genera las páginas por marca (Colnago, Pinarello, Kask, KOO, Sidi) con los productos de index.html.
Uso (desde la carpeta del sitio): python3 tools/generar_marcas.py
Vuelve a correrlo cada vez que agregues o cambies productos en index.html.
"""
import json, re, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from generar_paginas import HEADER, FOOTER, WA_FLOAT, FONTS, NEGOCIO, SITE, wa

productos = json.loads(subprocess.check_output(["node", "tools/productos.js", "index.html"]))

import unicodedata
def slug_prod(p):
    """Mismo slug que usa index.html: marca + nombre, sin tildes, en minúsculas y con guiones."""
    t = unicodedata.normalize("NFD", f'{p["marca"]} {p["nombre"]}')
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")

def url_prod(p):
    return f"/producto/{slug_prod(p)}"

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
      <a class="prod-img" href="{url_prod(p)}" aria-label="Ver {nombre}"><img src="/{foto}" alt="{nombre} en Veloce Medellín" loading="lazy">{badges}</a>
      <div class="prod-body">
        <div class="prod-brand">{p["marca"]}</div>
        <h3 class="prod-name"><a href="{url_prod(p)}">{p["nombre"]}</a></h3>
        {f'<p class="prod-res">{p["resumen"]}</p>' if p.get("resumen") else ""}{colores}{tallas}
        <div class="prod-price {'' if precio else 'consultar'}">{precio_html}</div>
        <a class="prod-more" href="{url_prod(p)}">Ver detalles</a>
        <a class="btn btn-solid" href="{wa(msg)}">{'Lo quiero' if precio else 'Cotizar'} · WhatsApp</a>
        {test}
      </div></article>"""

def ld_producto(p, url):
    lo, hi = valor(p.get("precio")), valor(p.get("hasta"))
    desde = (p.get("precio") or "").lower().startswith("desde")
    extra = {"hasMerchantReturnPolicy": {"@type": "MerchantReturnPolicy", "applicableCountry": "CO",
        "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow", "merchantReturnDays": 30,
        "returnMethod": ["https://schema.org/ReturnInStore", "https://schema.org/ReturnByMail"],
        "returnFees": "https://schema.org/ReturnFeesCustomerResponsibility",
        "merchantReturnLink": f"{SITE}/envios-y-devoluciones"}}
    if lo and lo >= 399000:
        extra["shippingDetails"] = {"@type": "OfferShippingDetails",
            "shippingRate": {"@type": "MonetaryAmount", "value": 0, "currency": "COP"},
            "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "CO"},
            "deliveryTime": {"@type": "ShippingDeliveryTime",
                "handlingTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY"},
                "transitTime": {"@type": "QuantitativeValue", "minValue": 2, "maxValue": 6, "unitCode": "DAY"}}}
    if desde and hi:
        offers = {"@type": "AggregateOffer", "lowPrice": lo, "highPrice": hi, "offerCount": len(p.get("variantes") or [1]),
                  "priceCurrency": "COP", "availability": "https://schema.org/InStock"}
    else:
        offers = {"@type": "Offer", "price": lo, "priceCurrency": "COP", "availability": "https://schema.org/InStock",
                  "itemCondition": "https://schema.org/NewCondition", "url": url,
                  "seller": {"@type": "BicycleStore", "name": "Veloce"}}
    offers.update(extra)
    return {"@type": "Product", "name": f'{p["marca"]} {p["nombre"]}', "brand": {"@type": "Brand", "name": p["marca"]},
            "category": p["cat"], "image": f'{SITE}/{p.get("foto","")}', "description": p.get("resumen") or p.get("desc", ""),
            "url": url, "offers": offers}

def detalle_modelos(m, prods):
    """Un bloque de texto por modelo, con sus datos clave y enlace a su página."""
    if not prods: return ""
    out = [f'      <h2>{m["titulo_det"]}</h2>']
    for p in prods:
        precio = p.get("precio") or ""
        linea = (f'<b>{precio}</b>' + (f' (antes {p["antes"]})' if p.get("antes") else "")) if precio else "Precio según la configuración que elijas"
        datos = "".join(f"<li>{x}</li>" for x in (p.get("specs") or [])[:3])
        extras = []
        if p.get("variantes"): extras.append(f'{len(p["variantes"])} colores')
        if p.get("tallas"): extras.append(f'tallas {p["tallas"][0]} a {p["tallas"][-1]}')
        if p.get("test"): extras.append("disponible para test ride")
        if p.get("fit"): extras.append("incluye bike fit Retül gratis")
        extra = (" · " + ", ".join(extras)) if extras else ""
        out.append(f"""      <h3><a href="{url_prod(p)}">{p["marca"]} {p["nombre"]}</a></h3>
      <p>{p.get("resumen","")} {linea}{extra}.</p>
      <ul>{datos}</ul>
      <p><a href="{url_prod(p)}">Ver fotos, características y disponibilidad: {p["marca"]} {p["nombre"]} →</a></p>""")
    return "\n".join(out)

def faqs_precio(prods):
    out = []
    for p in prods:
        if not valor(p.get("precio")): continue
        r = f'{p["marca"]} {p["nombre"]}: {p["precio"]}' + (f' (antes {p["antes"]})' if p.get("antes") else "") + " en Veloce, Medellín."
        if (valor(p["precio"]) or 0) >= 399000: r += " Envío gratis a toda Colombia."
        out.append((f'¿Cuánto cuesta {p["marca"]} {p["nombre"]} en Colombia?', r))
    return out

def pagina(m):
    prods = [p for p in productos if p["marca"] == m["marca"]]
    m = dict(m, faqs=list(m["faqs"]) + faqs_precio(prods))
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
    con_precio = [p for p in prods if valor(p.get("precio"))]
    if con_precio:
        ld.append({"@context": "https://schema.org", "@type": "ItemList", "name": m["miga"],
                   "itemListElement": [{"@type": "ListItem", "position": k + 1, "item": ld_producto(p, SITE + url_prod(p))} for k, p in enumerate(con_precio)]})
    hero = "" if m.get("sin_foto") else f'<img class="ph-img" src="/{m["og"]}" alt="{m["miga"]} en Veloce, Medellín" style="object-fit:contain;object-position:center;background:#fff">'
    otras = "".join(f'<a href="/{o["slug"]}"><b>{o["miga"]}</b><span>{o["corto"]}</span></a>' for o in MARCAS if o["slug"] != m["slug"])
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{m["title"]}</title>
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-BCTKZM82SJ"></script>
<script src="/js/analytics.js"></script>
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
{detalle_modelos(m, prods)}
      <h2>¿Por qué comprar en Veloce?</h2>
      <ul>
{m["porque"]}
        <li><b>Asesoría de ciclistas:</b> te ayudamos a elegir según cómo y dónde montas.</li>
        <li><b>Taller propio</b> en la misma tienda para el armado, ajustes y mantenimiento.</li>
        <li><b>Tienda física en El Poblado</b>, en el Mall Campestre Drive Inn: ven a ver y probar antes de comprar.</li>
        <li><b>Envío gratis a toda Colombia</b> en compras desde $399.000. <a href="/envios-y-devoluciones">Ver envíos y devoluciones</a>.</li>
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
       title="Bicicletas Colnago en Medellín · V5Rs, Y1Rs y V3 con precios | Veloce",
       desc="Compra tu bicicleta de ruta Colnago en Medellín: V5Rs, Y1Rs y V3 con precios en pesos. Bike fit Retül gratis con tu bici. Tienda en El Poblado. Cotiza por WhatsApp.",
       h1="Bicicletas Colnago<br>en Medellín.", og="img/productos/v5rs-3.jpg",
       intro="La marca italiana con la que Tadej Pogačar ha ganado el Tour de Francia. Ven a conocer la V5Rs, la Y1Rs y la V3 en nuestra tienda de El Poblado.",
       cta="Cotizar mi Colnago", cta_msg="Hola Veloce, quiero cotizar una bicicleta Colnago",
       titulo_prod="Modelos Colnago.", titulo_det="Las Colnago que tenemos, una por una",
       cuerpo="""      <h2>Colnago: el ciclismo a la italiana</h2>
      <p>Colnago nació en 1954 en Cambiago, cerca de Milán, de la mano de Ernesto Colnago. Desde entonces sus bicicletas han ganado Grandes Vueltas, clásicas y campeonatos del mundo, y hoy son la bici de Tadej Pogačar y del UAE Team Emirates.</p>
      <h3>¿Qué Colnago es para ti?</h3>
      <ul>
        <li><b>V5Rs:</b> la Colnago de competencia más liviana, para quien quiere lo máximo en montaña y en carrera.</li>
        <li><b>Y1Rs:</b> la aero de Colnago, hecha para ir rápido en el plano y en los finales.</li>
        <li><b>V3:</b> una Colnago de carbono para entrenar y hacer gran fondos, con un precio más accesible.</li>
      </ul>
      <p>Si no sabes cuál te conviene, escríbenos o ven a la tienda: te asesoramos según cómo montas, y con el bike fit Retül elegimos la talla exacta.</p>
      <h3>¿V5Rs o Y1Rs?</h3>
      <p>Las dos son bicis de WorldTour, pero buscan cosas distintas. La <b>V5Rs</b> es la todoterreno: tiene el cuadro más liviano que ha hecho Colnago, de unos 685 g sin pintar, y por eso es la que más rinde cuando la ruta tiene mucha montaña, como casi todas las de Antioquia. La <b>Y1Rs</b> es la aero: necesita unos 20 vatios menos que la V4Rs para rodar a 50 km/h, y se nota en el plano, en los relevos y en los finales rápidos.</p>
      <h3>Colnago V3: tu primera Colnago de carbono</h3>
      <p>La V3 lleva un cuadro y una horquilla de carbono monocasco con la geometría de la serie V, pero a un precio mucho más cercano. En Veloce la tenemos en dos montajes: con Shimano 105 Di2 de 12 velocidades y con Shimano Ultegra Di2 en la Black Edition, de manubrio integrado. Las dos llevan cambios electrónicos y frenos de disco.</p>
      <h3>Una Colnago para subir en Antioquia</h3>
      <p>Las Palmas, Santa Elena, el Alto de Minas o La Unión: aquí se monta subiendo. Por eso al cotizar tu Colnago miramos contigo la relación de cambios, las ruedas y las llantas que mejor le van a las rutas que haces, y no solo el modelo.</p>""",
       porque=FIT_BICI, sin_prod="",
       faqs=[("¿Dónde comprar una Colnago en Medellín?", "En Veloce, en el Mall Campestre Drive Inn, El Poblado (Calle 16A Sur #32B-38, Local 101). Escríbenos por WhatsApp al +57 305 245 1204."),
             ("¿Cuánto cuesta una Colnago en Colombia?", "Depende del modelo y la configuración. En esta página ves los precios de los modelos que tenemos; para la V5Rs y la Y1Rs te cotizamos según el grupo y las ruedas que quieras."),
             ("¿La bicicleta incluye bike fit?", "Sí. Toda bicicleta de más de $8.000.000 que compres en Veloce incluye bike fit Retül gratis."),
             ("¿Qué talla de Colnago necesito?", "Con el bike fit Retül medimos tu cuerpo y tu posición para elegir la talla exacta antes de comprar."),
             ("¿Cuál es la diferencia entre la Colnago V5Rs y la Y1Rs?", "La V5Rs es la todoterreno liviana, con el cuadro más liviano de Colnago, ideal para rutas con mucha montaña. La Y1Rs es la aerodinámica, hecha para ir más rápido en el plano y en los finales."),
             ("¿Puedo ver las Colnago en la tienda?", "Sí. Ven a Veloce, en el Mall Campestre Drive Inn de El Poblado, de lunes a viernes de 10:00 AM a 7:00 PM y los sábados de 11:00 AM a 5:00 PM."),
             ("¿Envían bicicletas Colnago a otras ciudades?", "Sí. Hacemos envíos a toda Colombia, gratis en compras desde $399.000.")]),
  dict(slug="pinarello-medellin", marca="Pinarello", miga="Pinarello", corto="Bicicletas de ruta de Treviso.",
       title="Bicicletas Pinarello en Medellín · F7, Grevil gravel y Nytro eléctrica | Veloce",
       desc="Pinarello en Medellín: F7 Ultegra Di2 a $24.900.000 (antes $34.900.000) Grevil gravel con Campagnolo Record 13v y Nytro E5 eléctrica de ruta. Bike fit Retül gratis con tu bici. Tienda en El Poblado. Cotiza por WhatsApp.",
       h1="Bicicletas Pinarello<br>en Medellín.", og="img/productos/pinarello-f7-roja-1.jpg",
       intro="Desde Treviso, Italia, las bicicletas que han ganado las carreras más grandes del mundo. Llévate la F7 Ultegra Di2 con $10 millones de descuento o la Grevil de gravel con Campagnolo Record 13v en nuestra tienda de El Poblado.",
       cta="Cotizar mi Pinarello", cta_msg="Hola Veloce, quiero cotizar una bicicleta Pinarello",
       titulo_prod="Modelos Pinarello.", titulo_det="Las Pinarello que tenemos, una por una",
       sin_prod="Te cotizamos el modelo y la configuración de Pinarello que quieras, desde la Dogma hasta las opciones de gravel. Escríbenos y te contamos disponibilidad, tiempos de entrega y precio.",
       cuerpo="""      <h2>Pinarello: diseño y velocidad desde 1952</h2>
      <p>Pinarello nació en Treviso, Italia, en 1952, fundada por Giovanni Pinarello. Sus bicicletas han ganado el Tour de Francia muchas veces y su modelo insignia, la Dogma, es una de las bicis de ruta más reconocidas del mundo.</p>
      <p>Una Pinarello se distingue por su diseño asimétrico, su rigidez y su manejo preciso en las bajadas. Es una bici para quien quiere sentir el ciclismo de alto nivel en cada salida.</p>
      <h3>Pinarello F7: el ADN de la Dogma</h3>
      <p>La F7 hereda de la Dogma F el diseño asimétrico, la geometría de competencia y la horquilla Onda. Con cuadro de carbono T900, Shimano Ultegra Di2 de 12 velocidades y frenos de disco, es la forma más directa de tener una Pinarello de carreras, y ahora está a <b>$24.900.000</b> (antes $34.900.000) en rojo y negro, azul y negro o negro mate.</p>
      <h3>Pinarello Grevil: gravel de carreras</h3>
      <p>La Grevil es la bici de gravel de Pinarello, para destapado rápido, aventura y fondos largos. Cuadro de carbono TorayCa T700, horquilla Onda Grevil, el nuevo Campagnolo Record de 13 velocidades con frenos hidráulicos, rines de carbono Princeton Grit 4540 y cockpit MOST con cables ocultos. Está a <b>$29.990.000</b>.</p>
      <h3>¿F7 de ruta o Grevil de gravel?</h3>
      <p>Si tu plan es el asfalto, los puertos y rodar rápido en grupo, la <b>F7</b> es tu Pinarello. Si quieres mezclar carretera con destapado, vías terciarias y aventuras de todo el día, la <b>Grevil</b> te da espacio para llantas anchas y una posición pensada para el terreno suelto, sin perder el carácter de carreras de la marca.</p>
      <h3>Te ayudamos a elegir</h3>
      <p>Cuéntanos cómo montas, qué rutas haces y qué presupuesto tienes, y te recomendamos el modelo y la configuración. Con el bike fit Retül elegimos la talla exacta antes de pedirla.</p>""",
       porque=FIT_BICI,
       faqs=[("¿Dónde comprar una Pinarello en Medellín?", "En Veloce, en el Mall Campestre Drive Inn, El Poblado (Calle 16A Sur #32B-38, Local 101). Escríbenos por WhatsApp al +57 305 245 1204."),
             ("¿Cuánto cuesta una Pinarello en Colombia?", "Depende del modelo y la configuración. La Pinarello F7 Ultegra Di2 está en $24.900.000 (antes $34.900.000) y la Grevil Record 13v de gravel en $29.990.000. Para otros modelos, escríbenos y te cotizamos."),
             ("¿La bicicleta incluye bike fit?", "Sí. Toda bicicleta de más de $8.000.000 que compres en Veloce incluye bike fit Retül gratis."),
             ("¿Qué talla de Pinarello necesito?", "Con el bike fit Retül medimos tu cuerpo y tu posición para elegir la talla exacta antes de pedir tu bici."),
             ("¿Tienen la Pinarello Dogma?", "Te cotizamos la Dogma y otros modelos de Pinarello según la configuración que quieras. Escríbenos por WhatsApp y te contamos disponibilidad, tiempos de entrega y precio."),
             ("¿Envían bicicletas Pinarello a otras ciudades?", "Sí. Hacemos envíos a toda Colombia, gratis en compras desde $399.000.")]),
  dict(slug="cascos-kask-medellin", marca="Kask", miga="Cascos Kask", corto="Cascos italianos de ruta y aero.",
       title="Cascos Kask en Medellín · Protone Icon, Elemento y Mojito³ | Veloce",
       desc="Cascos de bicicleta Kask en Medellín con precios en pesos: Protone Icon, Elemento, Mojito³, Sintesi, Utopia Y y Bambino Pro Evo. Varios colores y tallas. Tienda en El Poblado. Pide el tuyo por WhatsApp.",
       h1="Cascos Kask<br>en Medellín.", og="img/productos/kask-protone-1.jpg",
       intro="Los cascos italianos que usa el INEOS Grenadiers. Protone Icon, Elemento, Mojito³, Sintesi, Utopia Y y el Bambino Pro Evo de contrarreloj.",
       cta="Pedir mi casco Kask", cta_msg="Hola Veloce, me interesa un casco Kask. ¿Qué modelos, colores y tallas tienen?",
       titulo_prod="Cascos Kask.", titulo_det="Cada casco Kask en detalle", sin_prod="",
       cuerpo="""      <h2>¿Por qué un casco de bicicleta Kask?</h2>
      <p>Kask es una marca italiana de cascos que trabaja de la mano con equipos profesionales como el INEOS Grenadiers. Sus cascos combinan seguridad, ventilación y su ajuste Octo Fit, que se adapta a casi cualquier forma de cabeza.</p>
      <h3>¿Cuál elegir?</h3>
      <ul>
        <li><b>Protone Icon:</b> aero y ventilado a la vez, el casco todoterreno de los profesionales.</li>
        <li><b>Elemento:</b> el tope de gama de Kask, el más liviano y avanzado.</li>
        <li><b>Mojito³:</b> liviano, fresco y versátil para ruta, gravel o el día a día.</li>
        <li><b>Sintesi:</b> un Kask de calidad a un precio de entrada.</li>
        <li><b>Utopia Y:</b> el casco aerodinámico para ir lo más rápido posible.</li>
        <li><b>Bambino Pro Evo:</b> el casco de contrarreloj y triatlón con visor magnético, el mismo con el que Filippo Ganna batió el récord de la hora.</li>
      </ul>
      <h3>Elige según cómo montas</h3>
      <ul>
        <li><b>Subes mucho y hace calor:</b> Protone Icon, Elemento o Mojito³, los más ventilados.</li>
        <li><b>Ruedas rápido en el plano o compites:</b> Utopia Y, el aero de ruta.</li>
        <li><b>Contrarreloj o triatlón:</b> Bambino Pro Evo.</li>
        <li><b>Un solo casco para ruta, gravel y ciudad:</b> Sintesi o Mojito³.</li>
      </ul>
      <h3>Seguridad</h3>
      <p>Los cascos Kask cumplen el protocolo WG11 de impactos rotacionales, que evalúa cómo protege el casco en una caída con giro. Recuerda que un casco se debe cambiar después de un golpe fuerte, aunque por fuera se vea bien.</p>
      <h3>Combínalo con tus gafas</h3>
      <p>Las <a href="/gafas-koo-medellin">gafas KOO</a> son de la misma casa que Kask y están diseñadas para encajar con sus cascos.</p>""",
       porque=FIT_EQUIPO,
       faqs=[("¿Dónde comprar cascos Kask en Medellín?", "En Veloce, en el Mall Campestre Drive Inn, El Poblado. También puedes pedirlo por WhatsApp al +57 305 245 1204."),
             ("¿Qué talla de casco Kask necesito?", "Se mide el contorno de la cabeza un poco por encima de las cejas. Lo mejor es venir a la tienda y probártelo, o escríbenos y te ayudamos."),
             ("¿Tienen todos los colores?", "Cada modelo tiene varios colores. Escríbenos por WhatsApp y te confirmamos cuáles tenemos disponibles en tu talla."),
             ("¿Cuál es el mejor casco Kask para ruta?", "Depende de cómo montes. El Protone Icon es el más equilibrado entre aerodinámica y ventilación, el Elemento es el tope de gama y el Utopia Y es el más rápido en el plano."),
             ("¿Cada cuánto se cambia un casco de ciclismo?", "Siempre después de un golpe fuerte. Si no ha tenido golpes, conviene revisarlo cada cierto tiempo y cambiarlo cuando las espumas o las correas estén desgastadas."),
             ("¿Envían cascos Kask a otras ciudades?", "Sí. Hacemos envíos a toda Colombia, gratis en compras desde $399.000.")]),
  dict(slug="gafas-koo-medellin", marca="KOO", miga="Gafas KOO", corto="Gafas de ciclismo de Kask.",
       title="Veloce | Gafas KOO en Medellín · Gafas de ciclismo fotocromáticas",
       desc="Gafas de ciclismo KOO, la marca de gafas de Kask, en Medellín: Supernova, Alibi Photochromic, Alibi, Hype y Demos con precios en pesos. Tienda en El Poblado.",
       h1="Gafas KOO<br>en Medellín.", og="img/productos/koo-alibi-1.jpg",
       intro="Las gafas de ciclismo de Kask con diseño italiano. Supernova, Alibi Photochromic, Alibi, Hype y Demos.",
       cta="Pedir mis gafas KOO", cta_msg="Hola Veloce, me interesan unas gafas KOO. ¿Qué modelos tienen?",
       titulo_prod="Gafas KOO.", titulo_det="Cada modelo KOO en detalle", sin_prod="",
       cuerpo="""      <h2>KOO: gafas de ciclismo de Kask</h2>
      <p>KOO es la marca de gafas de Kask. Lleva al ciclismo el mismo diseño y la misma calidad italiana de sus cascos, y sus gafas están pensadas para encajar perfecto con un casco Kask.</p>
      <h3>¿Cuáles elegir?</h3>
      <ul>
        <li><b>Alibi Photochromic:</b> el lente se oscurece o aclara solo según la luz, ideal para salir temprano o rodar entre sol y nubes.</li>
        <li><b>Alibi:</b> gran campo de visión con un diseño limpio.</li>
        <li><b>Supernova:</b> sin marco y de solo 21 g, con lente panorámico Zeiss. En oferta a $699.000.</li>
        <li><b>Hype y Demos:</b> gafas KOO con gran relación calidad-precio.</li>
      </ul>""",
       porque=FIT_EQUIPO,
       faqs=[("¿Dónde comprar gafas KOO en Medellín?", "En Veloce, en el Mall Campestre Drive Inn, El Poblado. También puedes pedirlas por WhatsApp al +57 305 245 1204."),
             ("¿Qué son unas gafas fotocromáticas?", "Son gafas cuyo lente se oscurece con el sol y se aclara cuando hay poca luz, así no tienes que cambiar de lente durante la salida."),
             ("¿KOO es de Kask?", "Sí. KOO es la marca de gafas de Kask y sus gafas están diseñadas para usarse con cascos Kask.")]),
  dict(slug="zapatillas-sidi-medellin", marca="Sidi", miga="Zapatillas Sidi", corto="Zapatillas de ruta y MTB italianas.",
       title="Zapatillas Sidi en Medellín · Ruta y MTB | Veloce",
       desc="Zapatillas de ciclismo Sidi en Medellín: Shot 3, Wire 3 y Prima para ruta; Aeron, Dominator X y MTB Speed para MTB, desde $699.000. Tallas 37 a 46. Tienda en El Poblado. Pide las tuyas por WhatsApp.",
       h1="Zapatillas Sidi<br>en Medellín.", og="img/productos/sidi-shot3-blanco-1.jpg",
       intro="Zapatillas de ciclismo italianas hechas para durar. Shot 3, Wire 3 y Prima para ruta, y Aeron, Dominator X y MTB Speed para montaña, en tallas 37 a 46.",
       cta="Pedir mis Sidi", cta_msg="Hola Veloce, me interesan unas zapatillas Sidi. ¿Qué tallas y colores tienen?",
       titulo_prod="Zapatillas Sidi.", titulo_det="Cada zapatilla Sidi en detalle", sin_prod="",
       cuerpo="""      <h2>Sidi: zapatillas de ciclismo italianas desde 1960</h2>
      <p>Sidi fabrica zapatillas de ciclismo en Italia desde 1960. Son conocidas por su ajuste firme, su durabilidad y porque casi todas sus piezas se pueden reemplazar, así que te duran muchos años.</p>
      <h3>¿Cuáles elegir?</h3>
      <ul>
        <li><b>Shot 3:</b> la zapatilla de competencia de Sidi, rígida, liviana y con ajuste preciso.</li>
        <li><b>Wire 3:</b> la Sidi más técnica, con capellada ventilada y suela de carbono con rigidez 11.</li>
        <li><b>Prima:</b> la Sidi de ruta para empezar o rodar todo el día, con dial Tecno-3, velcro y suela de carbono y nylon, en 5 colores a $799.000.</li>
        <li><b>Aeron:</b> la Sidi de cross country, con suela full carbono rigidez 11 y doble dial NUUN.</li>
        <li><b>Dominator X:</b> la Sidi de MTB para rodar todo el día, con doble dial NUUN y suela de carbono compuesto, en Ice White y arena.</li>
        <li><b>MTB Speed:</b> zapatilla de MTB y gravel con dial Tecno-3 y suela reforzada con carbono, ahora en $699.000 (antes $899.000).</li>
      </ul>
      <h3>¿Zapatilla de ruta o de MTB?</h3>
      <p>La diferencia está en la suela. Las de <b>ruta</b> (Shot 3, Wire 3 y Prima) usan calas de tres tornillos y una suela lisa y muy rígida, para pasar toda la fuerza al pedal. Las de <b>MTB</b> (Aeron, Dominator X y MTB Speed) usan calas de dos tornillos y tienen tacos de caucho para caminar, así que también sirven para gravel y para quien se baja seguido de la bici.</p>
      <h3>La rigidez de la suela</h3>
      <p>Sidi mide la rigidez de sus suelas con un índice: entre más alto, más directa se siente la pedalada. La Shot 3 llega a 12, la Wire 3 y la Aeron a 11, y la Dominator X a 8, más cómoda para rodar todo el día.</p>
      <p>Si cambias de zapatillas, revisar la posición de las calas es clave. En Veloce podemos ajustarlas con el <a href="/bike-fit-retul-medellin">bike fit Retül</a>.</p>""",
       porque=FIT_EQUIPO,
       faqs=[("¿Dónde comprar zapatillas Sidi en Medellín?", "En Veloce, en el Mall Campestre Drive Inn, El Poblado. También puedes pedirlas por WhatsApp al +57 305 245 1204."),
             ("¿Qué tallas tienen?", "Ruta: Shot 3 y Wire 3 en tallas 39 a 46, y Prima en 38 a 45. MTB: Aeron y Dominator X en 38 a 45, y MTB Speed en 37 a 46 (tallas EU). Escríbenos y te confirmamos disponibilidad en tu talla y color."),
             ("¿Tienen zapatillas Sidi de MTB?", "Sí. La Sidi Aeron, de cross country con suela full carbono, a $1.890.000 (tallas 38 a 45); la Dominator X, en Ice White y arena, a $1.190.000 (tallas 38 a 45), y la MTB Speed, en negro y en blanco con negro, a $699.000 (tallas 37 a 46)."),
             ("¿Las Sidi son anchas o angostas?", "La horma de Sidi es más bien ajustada. Lo mejor es venir a probártelas a la tienda."),
             ("¿Las zapatillas de MTB sirven para gravel?", "Sí. Usan calas de dos tornillos y tienen tacos para caminar, por eso son las más usadas en gravel."),
             ("¿Envían zapatillas Sidi a otras ciudades?", "Sí. Hacemos envíos a toda Colombia, gratis en compras desde $399.000.")]),
  dict(slug="orbea-medellin", marca="Orbea", miga="Orbea", corto="MTB, ruta y eléctricas de montaña.",
       title="Bicicletas Orbea en Medellín · MTB, ruta y eléctricas | Veloce",
       desc="Bicicletas Orbea en Medellín con precios en pesos: Oiz y Alma de MTB, Orca de ruta y las eléctricas de montaña Rise y Wild, con test ride. Orbea en Veloce, El Poblado. Cotiza por WhatsApp.",
       h1="Bicicletas Orbea<br>en Medellín.", og="img/productos/orbea-oiz-h30-azul-v2.jpg",
       intro="Montaña, ruta y eléctricas de la marca vasca. Oiz y Alma para cross country, Orca para la carretera y las e-MTB Rise y Wild, que puedes probar en un test ride.",
       cta="Cotizar mi Orbea", cta_msg="Hola Veloce, quiero cotizar una bicicleta Orbea",
       titulo_prod="Modelos Orbea.", titulo_det="Las Orbea que tenemos, una por una", sin_prod="",
       cuerpo="""      <h2>Orbea: más de 180 años de historia</h2>
      <p>Orbea nació en 1840 en Eibar, en el País Vasco, y hoy es una de las marcas de bicicletas más reconocidas de España. Fabrica bicis de montaña, de ruta y eléctricas, y compite al más alto nivel en cross country con su equipo de fábrica. Encuentra Orbea en Veloce, en El Poblado, Medellín.</p>
      <h3>¿Qué Orbea es para ti?</h3>
      <ul>
        <li><b>Alma:</b> la rígida de cross country. Liviana, directa y la forma más accesible de empezar en el MTB en serio.</li>
        <li><b>Oiz:</b> la doble suspensión de cross country, con 120 mm de recorrido para ir rápido en subida y con control en la bajada.</li>
        <li><b>Orca:</b> la bici de ruta escaladora de Orbea, en carbono.</li>
        <li><b>Rise:</b> la eléctrica de montaña liviana, que se siente como una MTB normal con un empujón extra.</li>
        <li><b>Wild:</b> la eléctrica de enduro, con 170 mm de recorrido y motor Bosch para subir lo que antes no se podía.</li>
      </ul>
      <h3>Bicicletas eléctricas de montaña con test ride</h3>
      <p>Una e-MTB hay que montarla para entenderla. Por eso tenemos la Rise SL y la Wild disponibles para test ride: agendas tu prueba por WhatsApp, vienes a la tienda y la montas antes de decidir.</p>
      <h3>Tallas Orbea</h3>
      <p>En la página de cada modelo encuentras la guía de tallas con las medidas del cuadro y la estatura recomendada. Si estás entre dos tallas, te ayudamos a elegir en la tienda.</p>""",
       porque=FIT_BICI,
       faqs=[("¿Dónde comprar una bicicleta Orbea en Medellín?", "En Veloce, en el Mall Campestre Drive Inn, El Poblado (Calle 16A Sur #32B-38, Local 101). Escríbenos por WhatsApp al +57 305 245 1204."),
             ("¿Puedo probar una Orbea eléctrica antes de comprarla?", "Sí. Tenemos la Orbea Rise SL y la Wild disponibles para test ride. Escríbenos por WhatsApp para agendar tu prueba."),
             ("¿La bicicleta incluye bike fit?", "Sí. Toda bicicleta de más de $8.000.000 que compres en Veloce incluye bike fit Retül gratis."),
             ("¿Qué talla de Orbea necesito?", "Cada modelo tiene su guía de tallas según tu estatura. Si estás entre dos tallas, ven a la tienda o escríbenos y te ayudamos a elegir."),
             ("¿Hacen mantenimiento a bicicletas Orbea eléctricas?", "Sí. En nuestro taller atendemos bicicletas de ruta, MTB y eléctricas, incluido el mantenimiento de suspensiones."),
             ("¿Envían bicicletas Orbea a otras ciudades?", "Sí. Hacemos envíos a toda Colombia, gratis en compras desde $399.000.")]),
  dict(slug="look-medellin", marca="Look", miga="Look", corto="Gravel de carbono francesa.",
       title="Bicicletas Look en Medellín · Gravel 765 Optimum+ de carbono | Veloce",
       desc="Bicicleta Look 765 Optimum+ en Medellín: gravel de carbono con Shimano GRX, con precio en pesos y bike fit Retül gratis. Tienda en El Poblado. Cotiza por WhatsApp.",
       h1="Bicicletas Look<br>en Medellín.", og="img/productos/look765-1.jpg",
       intro="La marca francesa que inventó el pedal automático y fue pionera del carbono. Conoce la 765 Optimum+ de gravel en nuestra tienda de El Poblado.",
       cta="Cotizar mi Look", cta_msg="Hola Veloce, quiero cotizar una bicicleta Look",
       titulo_prod="Modelos Look.", titulo_det="La Look que tenemos", sin_prod="",
       cuerpo="""      <h2>Look: innovación francesa</h2>
      <p>Look es una marca francesa con sede en Nevers. En los años ochenta cambió el ciclismo dos veces: primero con el pedal automático, que reemplazó las correas, y después con los primeros cuadros de carbono que ganaron en el pelotón profesional. Hoy sigue haciendo bicicletas de carbono y pedales para ruta, gravel y pista.</p>
      <h3>Look 765 Optimum+: gravel para las vías de Antioquia</h3>
      <p>La 765 Optimum+ es una bici de carbono para salir de la carretera sin miedo: destapados, vías terciarias y rutas largas de aventura. Su cuadro usa la tecnología 3D Wave en las vainas para absorber vibraciones, tiene una geometría estable y admite llantas de gravel de hasta 42 mm.</p>
      <h3>¿Buscas otro modelo o pedales Look?</h3>
      <p>Escríbenos por WhatsApp y te contamos qué podemos conseguirte y en cuánto tiempo.</p>""",
       porque=FIT_BICI,
       faqs=[("¿Dónde comprar una bicicleta Look en Medellín?", "En Veloce, en el Mall Campestre Drive Inn, El Poblado (Calle 16A Sur #32B-38, Local 101). Escríbenos por WhatsApp al +57 305 245 1204."),
             ("¿La Look 765 Optimum+ sirve para carretera y destapado?", "Sí. Es una bici de gravel de carbono: rueda bien en asfalto y admite llantas de hasta 42 mm para destapado."),
             ("¿La bicicleta incluye bike fit?", "Sí. Toda bicicleta de más de $8.000.000 que compres en Veloce incluye bike fit Retül gratis."),
             ("¿Envían bicicletas Look a otras ciudades?", "Sí. Hacemos envíos a toda Colombia, gratis en compras desde $399.000.")]),
  dict(slug="zapatillas-fizik-medellin", marca="Fizik", miga="Zapatillas Fizik", corto="Zapatillas de ruta italianas con BOA.",
       title="Zapatillas Fizik en Medellín · Tempo R5 de ruta con BOA | Veloce",
       desc="Zapatillas de ciclismo Fizik en Medellín: Tempo Overcurve R5 de ruta con dial BOA, en 3 colores y tallas 38 a 45, con precio en pesos. Tienda en El Poblado. Pide las tuyas por WhatsApp.",
       h1="Zapatillas Fizik<br>en Medellín.", og="img/productos/fizik-tempo-r5-negro-1.jpg",
       intro="Zapatillas de ruta italianas con dial BOA. Conoce la Tempo Overcurve R5 en 3 colores y tallas 38 a 45.",
       cta="Pedir mis Fizik", cta_msg="Hola Veloce, me interesan unas zapatillas Fizik. ¿Qué tallas y colores tienen?",
       titulo_prod="Zapatillas Fizik.", titulo_det="La Fizik que tenemos", sin_prod="",
       cuerpo="""      <h2>Fizik: zapatillas y sillines italianos</h2>
      <p>Fizik es una marca italiana de sillines y zapatillas de ciclismo, muy usada en el pelotón profesional. Sus zapatillas se reconocen por su diseño limpio y por un ajuste pensado para muchas horas sobre la bici.</p>
      <h3>Tempo Overcurve R5: para rodar cómodo</h3>
      <p>La Tempo R5 es una zapatilla de ruta versátil. Su diseño Overcurve es asimétrico y sigue la forma del tobillo, se ajusta con un dial BOA y una correa de velcro, y su suela de nylon reforzado con carbono combina rigidez con comodidad para las salidas largas.</p>
      <h3>¿Fizik o Sidi?</h3>
      <p>La Tempo R5 es una gran opción para empezar con zapatillas de ruta o para rodar todo el día. Si buscas una suela full carbono y más rigidez, mira las <a href="/zapatillas-sidi-medellin">zapatillas Sidi</a>. Lo mejor es probarte las dos en la tienda.</p>
      <p>Si cambias de zapatillas, revisar la posición de las calas es clave. En Veloce podemos ajustarlas con el <a href="/bike-fit-retul-medellin">bike fit Retül</a>.</p>""",
       porque=FIT_EQUIPO,
       faqs=[("¿Dónde comprar zapatillas Fizik en Medellín?", "En Veloce, en el Mall Campestre Drive Inn, El Poblado. También puedes pedirlas por WhatsApp al +57 305 245 1204."),
             ("¿Qué tallas tienen?", "La Fizik Tempo R5 viene en tallas 38 a 45 (EU). Escríbenos y te confirmamos disponibilidad en tu talla y color."),
             ("¿Qué calas usan las Fizik Tempo R5?", "Son zapatillas de ruta, para calas de tres tornillos."),
             ("¿Envían zapatillas Fizik a otras ciudades?", "Sí. Hacemos envíos a toda Colombia, gratis en compras desde $399.000.")]),
  dict(slug="wilier-medellin", marca="Wilier", miga="Wilier", corto="Bicicletas de ruta italianas desde 1906.",
       title="Bicicletas Wilier en Medellín · Garda 105 de ruta en carbono | Veloce",
       desc="Bicicletas Wilier en Medellín: Garda 105 de ruta endurance en carbono, con Shimano 105 de 12v, 4 colores y tallas XS a XXL, con precio en pesos y bike fit Retül gratis. Tienda en El Poblado.",
       h1="Bicicletas Wilier<br>en Medellín.", og="img/productos/wilier-garda-roja-1.jpg",
       intro="Carbono italiano con más de un siglo de historia. Conoce la Wilier Garda, la bici de ruta para fondos largos, en nuestra tienda de El Poblado.",
       cta="Cotizar mi Wilier", cta_msg="Hola Veloce, quiero cotizar una bicicleta Wilier",
       titulo_prod="Modelos Wilier.", titulo_det="La Wilier que tenemos", sin_prod="",
       cuerpo="""      <h2>Wilier: ciclismo italiano desde 1906</h2>
      <p>Wilier Triestina es una marca italiana fundada en 1906, una de las más antiguas del ciclismo. Sus bicicletas de ruta se reconocen por el trabajo en carbono, el cuidado en los acabados y un diseño muy italiano.</p>
      <h3>Wilier Garda: carbono para rodar muchas horas</h3>
      <p>La Garda es la bici de ruta endurance de Wilier. Su geometría es un poco más alta y relajada que la de una bici de carreras, así que cargas menos la espalda y el cuello en los fondos largos, sin perder eficiencia. El cuadro y la horquilla son de carbono monocasco, el cableado va oculto y le caben llantas de 28 a 32 mm para más comodidad y agarre.</p>
      <h3>¿Para quién es?</h3>
      <p>Para quien quiere su primera bici de carbono, para entrenar entre semana y para los gran fondos y las salidas largas del fin de semana. Si buscas una posición más agresiva de competencia, mira también <a href="/colnago-medellin">Colnago</a> y <a href="/pinarello-medellin">Pinarello</a>.</p>
      <h3>Tallas Wilier</h3>
      <p>La Garda viene en seis tallas, de XS a XXL. En la página del modelo encuentras la guía de tallas según tu estatura, y con el bike fit Retül elegimos la talla exacta.</p>""",
       porque=FIT_BICI,
       faqs=[("¿Dónde comprar una bicicleta Wilier en Medellín?", "En Veloce, en el Mall Campestre Drive Inn, El Poblado (Calle 16A Sur #32B-38, Local 101). Escríbenos por WhatsApp al +57 305 245 1204."),
             ("¿Qué talla de Wilier necesito?", "La Wilier Garda viene en tallas XS a XXL. En la página del modelo está la guía de tallas según tu estatura, y con el bike fit Retül elegimos la talla exacta."),
             ("¿La bicicleta incluye bike fit?", "Sí. Toda bicicleta de más de $8.000.000 que compres en Veloce incluye bike fit Retül gratis."),
             ("¿Envían bicicletas Wilier a otras ciudades?", "Sí. Hacemos envíos a toda Colombia, gratis en compras desde $399.000.")]),
  dict(slug="magene-medellin", marca="Magene", miga="Magene", corto="Ciclocomputadores y pedales de potencia.",
       title="Magene en Medellín · Ciclocomputador C706 y pedales de potencia P715 | Veloce",
       desc="Magene en Medellín: ciclocomputador GPS C706 y pedales de potencia P715 para entrenar por vatios, con precios en pesos. Instalación en nuestro taller. Tienda en El Poblado. Pídelos por WhatsApp.",
       h1="Magene<br>en Medellín.", og="img/productos/magene-p715-1.jpg",
       intro="Tecnología para entrenar por potencia: el ciclocomputador GPS C706 y los pedales de potencia P715, en nuestra tienda de El Poblado.",
       cta="Preguntar por Magene", cta_msg="Hola Veloce, me interesan los productos Magene. ¿Qué tienen disponible?",
       titulo_prod="Productos Magene.", titulo_det="Cada producto Magene en detalle", sin_prod="",
       cuerpo="""      <h2>Magene: entrenar con datos</h2>
      <p>Magene hace ciclocomputadores, potenciómetros y sensores para ciclismo, y equipa al equipo WorldTour Astana. Su propuesta es tecnología de gama alta a un precio muy competitivo.</p>
      <h3>¿Qué necesitas para entrenar por potencia?</h3>
      <ul>
        <li><b>Un potenciómetro:</b> los pedales P715 miden la potencia de cada pierna por separado y se instalan como cualquier pedal.</li>
        <li><b>Un ciclocomputador:</b> el C706 muestra tus vatios en vivo, guarda tus salidas y te guía con GPS e indicaciones por voz.</li>
      </ul>
      <p>La potencia, medida en vatios, no depende del viento ni de la pendiente, y por eso es la forma más confiable de saber si estás mejorando.</p>
      <h3>Entrena con nosotros</h3>
      <p>Si quieres sacarle provecho a tus datos, en nuestro <a href="/centro-de-entrenamiento-ciclismo-medellin">centro de entrenamiento</a> hacemos clases por potencia en simulador.</p>""",
       porque='        <li><b>Instalación en nuestro taller:</b> instalamos tu potenciómetro y lo configuramos con tu ciclocomputador. <a href="/taller-de-bicicletas-medellin">Ver el taller</a>.</li>',
       faqs=[("¿Dónde comprar productos Magene en Medellín?", "En Veloce, en el Mall Campestre Drive Inn, El Poblado. También puedes pedirlos por WhatsApp al +57 305 245 1204."),
             ("¿Los pedales Magene P715 sirven para mi bicicleta?", "Se instalan como cualquier pedal y hay versiones para calas Shimano SPD-SL y Look KEO. Escríbenos y te confirmamos cuál tenemos disponible."),
             ("¿El Magene C706 funciona con otros potenciómetros y sensores?", "Sí. Es compatible con potenciómetros y sensores, y también con los segmentos de Strava."),
             ("¿Instalan el potenciómetro?", "Sí. En nuestro taller instalamos potenciómetros y los configuramos con tu ciclocomputador."),
             ("¿Envían productos Magene a otras ciudades?", "Sí. Hacemos envíos a toda Colombia, gratis en compras desde $399.000.")]),
]

if __name__ == "__main__":
    for m in MARCAS:
        open(f'{m["slug"]}.html', "w", encoding="utf-8").write(pagina(m))
        print("ok", m["slug"], len([p for p in productos if p["marca"] == m["marca"]]), "productos")
