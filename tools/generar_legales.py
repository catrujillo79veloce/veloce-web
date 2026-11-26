"""Genera las páginas legales: cómo comprar, política de datos personales y términos y condiciones.
Uso (desde la carpeta del sitio): python3 tools/generar_legales.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from generar_paginas import HEADER, FOOTER, WA_FLOAT, FONTS, SITE, wa

EMPRESA = "Bicicletas Veloce S.A.S."
NIT = "900167958-2"
CORREO = "ventas@veloce.com.co"
MAIL = f'<a href="mailto:{CORREO}">{CORREO}</a>'
WHATS = '<a href="https://wa.me/573052451204">+57 305 245 1204</a>'
DIRECCION = "Calle 16A Sur #32B-38, Local 101, Mall Campestre Drive Inn, El Poblado, Medellín, Antioquia, Colombia"
HORARIO = "lunes a viernes de 10:00 a. m. a 7:00 p. m. y sábados de 11:00 a. m. a 5:00 p. m. Domingos y festivos cerrado"
VIGENCIA = "25 de noviembre de 2026"

PAGINAS = [
  {
    "slug": "como-comprar",
    "nombre": "Cómo comprar",
    "title": "Veloce | Cómo comprar y medios de pago",
    "desc": "Compra en Veloce con asesoría por WhatsApp o en la tienda de El Poblado. Pagas con efectivo, transferencia o tarjeta. Envío gratis desde $399.000.",
    "h1": "Cómo comprar<br>y pagar.",
    "intro": "Eliges tu producto en la web y cierras la compra con nosotros por WhatsApp o en la tienda, con asesoría personal.",
    "wa": "Hola Veloce, quiero comprar y tengo una pregunta",
    "cuerpo": f"""      <h2>Paso a paso</h2>
      <ol>
        <li>Elige el producto en bicicletasveloce.com y toca <b>“Lo quiero · WhatsApp”</b>.</li>
        <li>Te confirmamos disponibilidad, talla y color, y te asesoramos si tienes dudas.</li>
        <li>Te enviamos el resumen del pedido con el precio final, el costo de envío si aplica y los datos para pagar.</li>
        <li>Haces el pago por el medio que prefieras.</li>
        <li>Te enviamos la factura electrónica a tu correo.</li>
        <li>Despachamos tu pedido y te mandamos la guía de rastreo por WhatsApp, o lo recoges en la tienda.</li>
      </ol>

      <h2>Medios de pago</h2>
      <ul>
        <li><b>Efectivo</b> en la tienda.</li>
        <li><b>Transferencia bancaria.</b></li>
        <li><b>Tarjetas de crédito o débito.</b></li>
      </ul>
      <p>Todos los precios de la web están en pesos colombianos (COP) e incluyen IVA.</p>
      <p>Veloce nunca te va a pedir claves, códigos de verificación ni datos de tu tarjeta por WhatsApp. Si te escriben desde otro número diciendo ser Veloce, confírmalo antes con nosotros al {WHATS}.</p>

      <h2>Envíos y entregas</h2>
      <ul>
        <li><b>Envío gratis</b> a toda Colombia en compras desde <b>$399.000</b>.</li>
        <li>En compras de menos de $399.000, el envío cuesta <b>$15.000</b>.</li>
        <li>Tiempos: de 2 a 4 días hábiles en ciudades principales y de 3 a 6 días hábiles en municipios y otras ciudades.</li>
        <li>En Medellín también puedes recoger tu compra en la tienda: {DIRECCION}.</li>
      </ul>
      <p>Los cambios, devoluciones y garantías están explicados en <a href="/envios-y-devoluciones">Envíos y devoluciones</a>.</p>

      <h2>Atención</h2>
      <p>WhatsApp {WHATS} · {MAIL}<br>Horario: {HORARIO}.</p>""",
    "lateral": """      <h3>¿Listo para comprar?</h3>
      <p><b>Pagas como prefieras:</b> efectivo, transferencia o tarjeta.</p>
      <p><b>Envío gratis</b> a toda Colombia desde $399.000.</p>
      <p><b>Factura electrónica</b> en todas las compras.</p>""",
  },
  {
    "slug": "privacidad",
    "nombre": "Política de datos personales",
    "title": "Veloce | Política de tratamiento de datos personales",
    "desc": "Cómo Bicicletas Veloce S.A.S. recoge, usa y protege tus datos personales, y cómo ejercer tus derechos según la Ley 1581 de 2012.",
    "h1": "Política de<br>datos personales.",
    "intro": f"Cómo {EMPRESA} recoge, usa y protege tus datos personales, conforme a la Ley 1581 de 2012 y el Decreto 1074 de 2015.",
    "wa": "Hola Veloce, tengo una pregunta sobre mis datos personales",
    "cuerpo": f"""      <h2>1. Responsable del tratamiento</h2>
      <p>{EMPRESA}, NIT {NIT}, con domicilio en la {DIRECCION}. Contacto: {MAIL} y WhatsApp {WHATS}.</p>

      <h2>2. Qué datos recogemos</h2>
      <ul>
        <li><b>Identificación y contacto:</b> nombre, documento, teléfono, correo y dirección de entrega.</li>
        <li><b>Compras:</b> productos, pagos, facturas y garantías.</li>
        <li><b>Servicios:</b> medidas corporales, flexibilidad y molestias o lesiones que nos cuentes para el bike fit o el entrenamiento.</li>
        <li><b>Navegación:</b> cookies e información de uso de la web, a través de herramientas como Google Analytics y Google Ads.</li>
      </ul>
      <p>Los datos de salud que compartes para el bike fit son datos sensibles. No estás obligado a darlos, y solo los usamos con tu autorización expresa para prestarte ese servicio.</p>

      <h2>3. Para qué usamos tus datos</h2>
      <ul>
        <li>Atender tus consultas y asesorarte por WhatsApp, teléfono, correo o en la tienda.</li>
        <li>Procesar pedidos, pagos, facturación electrónica, envíos, cambios, devoluciones y garantías.</li>
        <li>Prestar servicios de taller, bike fit y entrenamiento.</li>
        <li>Enviarte novedades, ofertas e invitaciones a eventos, solo si lo autorizas. Puedes pedir que dejemos de hacerlo en cualquier momento.</li>
        <li>Medir y mejorar la web y nuestra publicidad.</li>
        <li>Cumplir obligaciones legales, contables y tributarias.</li>
      </ul>

      <h2>4. Con quién compartimos tus datos</h2>
      <p>No vendemos tus datos. Solo los compartimos con proveedores que nos ayudan a prestar el servicio, como transportadoras, plataformas de pago y facturación, WhatsApp y Google, y con autoridades cuando la ley lo exige. Algunos de estos proveedores pueden guardar datos fuera de Colombia, con niveles adecuados de protección.</p>

      <h2>5. Tus derechos</h2>
      <p>Como titular de los datos tienes derecho a:</p>
      <ul>
        <li>Conocer, actualizar y corregir tus datos.</li>
        <li>Pedir prueba de la autorización que nos diste.</li>
        <li>Saber cómo hemos usado tus datos.</li>
        <li>Revocar la autorización o pedir que borremos tus datos, cuando no haya un deber legal de conservarlos.</li>
        <li>Acceder gratis a tus datos.</li>
        <li>Presentar quejas ante la Superintendencia de Industria y Comercio.</li>
      </ul>

      <h2>6. Cómo ejercer tus derechos</h2>
      <p>Escríbenos a {MAIL} con tu nombre, documento, lo que pides y un dato de contacto para responderte.</p>
      <ul>
        <li><b>Consultas:</b> respondemos en máximo 10 días hábiles, prorrogables 5 días hábiles más avisándote el motivo.</li>
        <li><b>Reclamos</b> (corregir, actualizar, borrar o revocar): respondemos en máximo 15 días hábiles, prorrogables 8 días hábiles más avisándote el motivo.</li>
      </ul>
      <p>El área responsable de atender estas solicitudes es Servicio al Cliente de {EMPRESA}, en {MAIL} y por WhatsApp al {WHATS}.</p>

      <h2>7. Menores de edad</h2>
      <p>Solo tratamos datos de menores con autorización de sus padres o representantes, y respetando siempre su interés superior.</p>

      <h2>8. Seguridad y conservación</h2>
      <p>Protegemos tus datos con medidas técnicas y administrativas razonables. Los guardamos mientras sean necesarios para las finalidades descritas o mientras la ley lo exija.</p>

      <h2>9. Vigencia</h2>
      <p>Esta política rige desde el {VIGENCIA}. Si la cambiamos, publicaremos la nueva versión en esta página.</p>""",
    "lateral": f"""      <h3>¿Preguntas sobre tus datos?</h3>
      <p>Escríbenos a {MAIL}.</p>
      <p><b>Consultas:</b> respuesta en máximo 10 días hábiles.</p>
      <p><b>Reclamos:</b> respuesta en máximo 15 días hábiles.</p>""",
  },
  {
    "slug": "terminos",
    "nombre": "Términos y condiciones",
    "title": "Veloce | Términos y condiciones",
    "desc": "Términos y condiciones de compra en Bicicletas Veloce S.A.S.: precios, pagos, envíos, derecho de retracto, reversión del pago y garantías.",
    "h1": "Términos y<br>condiciones.",
    "intro": f"Aplican a las compras de productos y servicios de {EMPRESA} hechas por bicicletasveloce.com, WhatsApp o en la tienda. Al comprar, aceptas estos términos.",
    "wa": "Hola Veloce, tengo una pregunta sobre los términos de compra",
    "cuerpo": f"""      <h2>1. Quiénes somos</h2>
      <p>{EMPRESA}, NIT {NIT}. {DIRECCION}. WhatsApp {WHATS} · {MAIL}.</p>

      <h2>2. Precios</h2>
      <p>Los precios están en pesos colombianos (COP) e incluyen IVA. Pueden cambiar sin previo aviso, pero respetamos el precio que te confirmamos en el resumen de tu pedido. Si hay un error evidente de precio en la web, te avisamos antes de cobrar y puedes cancelar sin costo.</p>

      <h2>3. Disponibilidad</h2>
      <p>Las fotos son de referencia y los colores pueden variar levemente según la pantalla. Antes de cobrar te confirmamos disponibilidad, talla y color. Si un producto se agota después de pagar, te ofrecemos otro similar o te devolvemos el dinero completo.</p>

      <h2>4. Cómo se hace la compra</h2>
      <p>Tu pedido queda confirmado cuando recibimos el pago y te enviamos la confirmación por WhatsApp o correo. Después te enviamos la factura electrónica. El paso a paso y los medios de pago están en <a href="/como-comprar">Cómo comprar</a>.</p>

      <h2>5. Envíos</h2>
      <p>Los costos, tiempos y condiciones de envío están en <a href="/envios-y-devoluciones">Envíos y devoluciones</a>. El riesgo del producto pasa a ti cuando lo recibes.</p>

      <h2>6. Derecho de retracto</h2>
      <p>Si compraste a distancia (por la web, WhatsApp o teléfono), puedes retractarte dentro de los <b>5 días hábiles</b> siguientes a la entrega, como dice el artículo 47 de la Ley 1480 de 2011. El producto debe estar sin uso y con sus empaques. El transporte de vuelta corre por tu cuenta, y te devolvemos el 100 % de lo pagado en máximo 15 días calendario.</p>
      <p>El retracto no aplica a bicicletas armadas o configuradas a tu medida, ni a servicios ya prestados como bike fit o taller.</p>

      <h2>7. Reversión del pago</h2>
      <p>Si pagaste con tarjeta u otro medio electrónico en una compra a distancia, puedes pedir la reversión del pago, según el artículo 51 de la Ley 1480 de 2011, cuando:</p>
      <ul>
        <li>fuiste víctima de fraude;</li>
        <li>la compra no fue solicitada por ti;</li>
        <li>no recibiste el producto;</li>
        <li>el producto no corresponde a lo pedido o tiene defectos.</li>
      </ul>
      <p>Debes avisarnos y avisar a tu banco dentro de los 5 días hábiles siguientes a cuando conociste el problema, y devolver el producto si lo recibiste.</p>

      <h2>8. Cambios, devoluciones y garantía</h2>
      <p>Puedes pedir el cambio o la devolución de un producto sin uso dentro de los 10 días calendario siguientes a la entrega. Las condiciones completas están en <a href="/envios-y-devoluciones">Envíos y devoluciones</a>. Todos los productos tienen la garantía del fabricante; si la marca no indica otro plazo, es de 1 año desde la compra. Si un producto tiene un defecto de fábrica, escríbenos y te acompañamos en el proceso ante la marca. La garantía no cubre el desgaste normal, golpes, caídas, mal uso ni arreglos hechos por terceros.</p>

      <h2>9. Servicios: taller, bike fit y entrenamiento</h2>
      <p>Los servicios se agendan con cita previa. El precio de cada servicio te lo confirmamos antes de agendar. Si no puedes asistir, avísanos con al menos 24 horas de anticipación para reprogramar.</p>

      <h2>10. Promociones</h2>
      <p>Cada promoción tiene sus propias condiciones y vigencia, publicadas junto a ella. Por ejemplo, el bike fit Retül gratis aplica solo en las bicicletas que lo indican en su ficha del catálogo. Las promociones no se acumulan, salvo que se diga lo contrario.</p>

      <h2>11. Propiedad intelectual</h2>
      <p>Los textos, fotos y logos de esta web son de {EMPRESA} o de las marcas que representamos. No se pueden usar sin autorización.</p>

      <h2>12. Datos personales</h2>
      <p>Tratamos tus datos según nuestra <a href="/privacidad">Política de tratamiento de datos personales</a>.</p>

      <h2>13. Peticiones, quejas y reclamos</h2>
      <p>Escríbenos a {MAIL} o por WhatsApp al {WHATS}. Respondemos en máximo 15 días hábiles. También puedes acudir a la Superintendencia de Industria y Comercio.</p>

      <h2>14. Ley aplicable</h2>
      <p>Estos términos se rigen por las leyes de Colombia. Rigen desde el {VIGENCIA}.</p>""",
    "lateral": f"""      <h3>¿Tienes dudas?</h3>
      <p><b>Retracto:</b> 5 días hábiles desde la entrega.</p>
      <p><b>Garantía:</b> legal y del fabricante.</p>
      <p><b>Contacto:</b> {MAIL}</p>""",
  },
]

for p in PAGINAS:
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
              {"@type": "ListItem", "position": 2, "name": p["nombre"], "item": f"{SITE}/{p['slug']}"}]}]
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p['title']}</title>
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-BCTKZM82SJ"></script>
<script src="/js/analytics.js"></script>
<script src="/js/promo.js"></script>
<meta name="description" content="{p['desc']}">
<link rel="canonical" href="{SITE}/{p['slug']}">
{FONTS}
<link rel="stylesheet" href="/css/estilos.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
{HEADER}

<section class="page-hero">
  <div class="wrap">
    <div class="crumbs"><a href="/">Inicio</a> / {p['nombre']}</div>
    <div class="tri on-dark"><i></i><i></i><i></i></div>
    <h1 class="display">{p['h1']}</h1>
    <p>{p['intro']}</p>
    <div class="hero-ctas"><a class="btn btn-light" href="{wa(p['wa'])}">Preguntar por WhatsApp</a></div>
  </div>
</section>

<section>
  <div class="wrap page-grid">
    <article class="prose">
{p['cuerpo']}
    </article>
    <aside class="side-card">
{p['lateral']}
      <a class="btn btn-solid" href="{wa(p['wa'])}">Escríbenos por WhatsApp</a>
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
    open(f"{p['slug']}.html", "w", encoding="utf-8").write(html)
    print("ok", p["slug"])
