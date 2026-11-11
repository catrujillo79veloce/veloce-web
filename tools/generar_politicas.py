"""Genera la página de envíos, cambios y devoluciones.
Uso (desde la carpeta del sitio): python3 tools/generar_politicas.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from generar_paginas import HEADER, FOOTER, WA_FLOAT, FONTS, SITE, wa

SLUG = "envios-y-devoluciones"
TITLE = "Envíos, cambios y devoluciones | Veloce"
DESC = "Envío gratis a toda Colombia en compras desde $399.000. Entrega de 2 a 6 días hábiles. Cambios hasta 30 días y derecho de retracto de 5 días hábiles."

cuerpo = """      <h2>Envíos a toda Colombia</h2>
      <ul>
        <li><b>Envío gratis</b> en compras desde <b>$399.000</b>.</li>
        <li>En compras de menos de $399.000, el envío se paga <b>contra entrega</b> a la transportadora, según la ciudad de destino y el tamaño del paquete.</li>
        <li>Una vez confirmes tu compra, preparamos tu pedido y te enviamos la guía de la transportadora.</li>
      </ul>
      <h3>Tiempos de entrega</h3>
      <ul>
        <li><b>Ciudades principales:</b> de 2 a 4 días hábiles.</li>
        <li><b>Municipios y otras ciudades:</b> de 3 a 6 días hábiles.</li>
        <li><b>Zonas rurales o de difícil acceso:</b> pueden tardar algunos días más según la cobertura de la transportadora.</li>
      </ul>
      <p>Te enviamos la guía de rastreo por WhatsApp para que sigas tu pedido. Los tiempos pueden variar por temporadas altas, clima o situaciones de la transportadora; si hay un retraso te avisamos.</p>
      <p>En Medellín también puedes recoger tu compra en nuestra tienda del Mall Campestre Drive Inn, El Poblado.</p>

      <h2>Cambios</h2>
      <p>Si el producto no te sirvió (por ejemplo la talla o el color de un casco, unas zapatillas o unas gafas), puedes cambiarlo dentro de los <b>30 días calendario</b> siguientes a la entrega, siempre que:</p>
      <ul>
        <li>El producto esté <b>sin uso</b>, en perfecto estado.</li>
        <li>Venga con <b>todos sus empaques</b>, etiquetas, accesorios y manuales originales.</li>
        <li>Presentes la factura o el número de tu pedido.</li>
      </ul>
      <p>Puedes hacer el cambio en la tienda o enviándonos el producto. Si lo envías, el costo del envío de vuelta corre por tu cuenta.</p>

      <h2>Devoluciones y derecho de retracto</h2>
      <p>Si compraste a distancia (por WhatsApp, teléfono o en línea), tienes <b>derecho de retracto</b> según el artículo 47 de la Ley 1480 de 2011 (Estatuto del Consumidor):</p>
      <ul>
        <li>Puedes retractarte de tu compra dentro de los <b>5 días hábiles</b> siguientes a la entrega del producto.</li>
        <li>El producto debe devolverse sin uso, en las mismas condiciones en que lo recibiste y con todos sus empaques.</li>
        <li>Los costos de transporte de la devolución corren por cuenta del cliente.</li>
        <li>Te devolvemos el dinero en un plazo máximo de 30 días calendario desde que ejerces el retracto.</li>
      </ul>
      <p>Para iniciar un cambio o una devolución, escríbenos por WhatsApp al +57 305 245 1204 con tu número de pedido.</p>

      <h2>Productos que no tienen cambio ni devolución</h2>
      <ul>
        <li>Bicicletas armadas o configuradas a la medida del cliente (por ejemplo con grupo, ruedas o talla elegidos para ti).</li>
        <li>Productos usados, ajustados o con señales de uso.</li>
        <li>Servicios ya prestados, como bike fit o taller.</li>
      </ul>

      <h2>Garantía</h2>
      <p>Todos nuestros productos tienen la garantía legal del fabricante. Si un producto presenta un defecto de fábrica, escríbenos y te ayudamos con el proceso de garantía ante la marca.</p>"""

lateral = """      <h3>¿Tienes dudas?</h3>
      <p><b>Envío gratis</b> a toda Colombia en compras desde $399.000.</p>
      <p><b>Cambios:</b> hasta 30 días, producto sin uso y con empaques.</p>
      <p><b>Retracto:</b> 5 días hábiles desde la entrega.</p>"""

ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
          {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
          {"@type": "ListItem", "position": 2, "name": "Envíos y devoluciones", "item": f"{SITE}/{SLUG}"}]}]

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-BCTKZM82SJ"></script>
<script src="/js/analytics.js"></script>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{SITE}/{SLUG}">
{FONTS}
<link rel="stylesheet" href="/css/estilos.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
{HEADER}

<section class="page-hero">
  <div class="wrap">
    <div class="crumbs"><a href="/">Inicio</a> / Envíos y devoluciones</div>
    <div class="tri on-dark"><i></i><i></i><i></i></div>
    <h1 class="display">Envíos, cambios<br>y devoluciones.</h1>
    <p>Envío gratis a toda Colombia en compras desde $399.000. Cambios hasta 30 días con el producto sin uso y en su empaque.</p>
    <div class="hero-ctas"><a class="btn btn-light" href="{wa('Hola Veloce, tengo una pregunta sobre envíos o devoluciones')}">Preguntar por WhatsApp</a></div>
  </div>
</section>

<section>
  <div class="wrap page-grid">
    <article class="prose">
{cuerpo}
    </article>
    <aside class="side-card">
{lateral}
      <a class="btn btn-solid" href="{wa('Hola Veloce, tengo una pregunta sobre envíos o devoluciones')}">Escríbenos por WhatsApp</a>
    </aside>
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
open(f"{SLUG}.html", "w", encoding="utf-8").write(html)
print("ok", SLUG)
