"""Genera las páginas de servicio de Veloce a partir del header/footer de index.html.
Uso: python3 tools/generar_paginas.py  (desde la carpeta del sitio)
"""
import json, re

SITE = "https://www.bicicletasveloce.com"
WA = "573052451204"
idx = open("index.html", encoding="utf-8").read()

def bloque(tag):
    m = re.search(rf"<{tag}>.*?</{tag}>", idx, re.S)
    return m.group(0)

def rutas(html):
    html = re.sub(r'href="#inicio"', 'href="/"', html)
    return re.sub(r'href="#([a-z/]+)"', r'href="/#\1"', html)

HEADER = rutas(bloque("header"))
FOOTER = rutas(bloque("footer"))
WA_FLOAT = re.search(r'<a class="wa".*?</a>', idx, re.S).group(0)
FONTS = re.search(r'<link rel="preconnect" href="https://fonts.googleapis.com">.*?display=swap" rel="stylesheet">', idx, re.S).group(0)

NEGOCIO = {
    "@type": "BicycleStore", "name": "Veloce", "url": SITE + "/",
    "telephone": "+57 305 245 1204",
    "address": {"@type": "PostalAddress", "streetAddress": "Calle 16A Sur #32B-38, Local 101, Mall Campestre Drive Inn",
                "addressLocality": "Medellín", "addressRegion": "Antioquia", "addressCountry": "CO"},
}

def wa(txt):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(txt)}"

OTRAS = {
    "bike-fit-retul-medellin": ("Bike fit Retül", "Medición 3D de tu posición en la bici."),
    "taller-de-bicicletas-medellin": ("Taller", "Ruta, MTB y eléctricas."),
    "centro-de-entrenamiento-ciclismo-medellin": ("Centro de entrenamiento", "Clases por potencia en simulador."),
}

def pagina(slug, title, desc, kicker, h1, intro, cta_txt, cta_msg, cuerpo, faqs, lateral, servicio, foto=None, foto_alt=""):
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    ld = [
        {"@context": "https://schema.org", "@type": "Service", "name": servicio, "serviceType": servicio,
         "areaServed": {"@type": "City", "name": "Medellín"}, "provider": NEGOCIO, "url": f"{SITE}/{slug}"},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": kicker, "item": f"{SITE}/{slug}"}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faqs]},
    ]
    otras = "".join(f'<a href="/{s}"><b>{n}</b><span>{d}</span></a>' for s, (n, d) in OTRAS.items() if s != slug)
    otras += '<a href="/#productos"><b>Productos</b><span>Bicicletas, cascos, gafas y más.</span></a>'
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{slug}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/{slug}">
<meta property="og:image" content="{SITE}/img/hero-colnago.jpg">
<meta property="og:locale" content="es_CO">
{FONTS}
<link rel="stylesheet" href="/css/estilos.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
{HEADER}

<section class="page-hero">{f'<img class="ph-img" src="/{foto}" alt="{foto_alt}">' if foto else ""}
  <div class="wrap">
    <div class="crumbs"><a href="/">Inicio</a> / {kicker}</div>
    <div class="tri on-dark"><i></i><i></i><i></i></div>
    <h1 class="display">{h1}</h1>
    <p>{intro}</p>
    <div class="hero-ctas"><a class="btn btn-light" href="{wa(cta_msg)}">{cta_txt}</a><a class="btn btn-ghost" href="/#visitanos">Cómo llegar</a></div>
  </div>
</section>

<section>
  <div class="wrap page-grid">
    <article class="prose">
{cuerpo}
      <h2>Preguntas frecuentes</h2>
      <div class="faq">{faq_html}</div>
    </article>
    <aside class="side-card">
{lateral}
      <a class="btn btn-solid" href="{wa(cta_msg)}">{cta_txt} · WhatsApp</a>
      <a class="btn btn-outline" href="https://www.google.com/maps/search/?api=1&query=Veloce+Mall+Campestre+Drive+Inn+Calle+16A+Sur+32B-38+Medell%C3%ADn">Abrir en Google Maps</a>
    </aside>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><div><div class="tri"><i></i><i></i><i></i></div><h2 class="display">También en Veloce.</h2></div></div>
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

DIR = """      <p><b>Dirección:</b> Calle 16A Sur #32B-38, Local 101, Mall Campestre Drive Inn, El Poblado, Medellín.</p>"""

# ---------- BIKE FIT ----------
bf_cuerpo = """      <h2>¿Qué es un bike fit Retül?</h2>
      <p>Un bike fit es el ajuste de tu bicicleta a tu cuerpo. Con el sistema <b>Retül</b> lo hacemos con datos y no a ojo: ponemos marcadores LED en 8 puntos de tu cuerpo y una cámara de captura 3D registra cada pedalada en tiempo real. Así vemos ángulos y movimientos que no se notan a simple vista y ajustamos tu posición con precisión milimétrica.</p>
      <p>En Veloce hacemos el bike fit Retül en nuestra tienda de El Poblado, Medellín, con ciclistas que entienden lo que sientes en la bici.</p>

      <h2>Beneficios</h2>
      <ul>
        <li><b>Más comodidad:</b> menos molestias en espalda, cuello, manos y sillín para rodar más horas.</li>
        <li><b>Menos lesiones:</b> una buena alineación ayuda a prevenir dolor de rodilla, espalda baja y adormecimiento en manos y pies.</li>
        <li><b>Más potencia:</b> una posición óptima aprovecha mejor tu fuerza, con más vatios y más resistencia con el mismo esfuerzo.</li>
        <li><b>Compra acertada:</b> si vas a comprar bici, el bike fit te dice qué talla y geometría te sirven antes de pagar.</li>
      </ul>

      <h2>Así es el proceso</h2>
      <h3>1. Entrevista y evaluación física</h3>
      <p>Revisamos tu flexibilidad, lesiones anteriores, molestias y tus objetivos en la bici.</p>
      <h3>2. Captura 3D en movimiento</h3>
      <p>Con los marcadores LED puestos, pedaleas en tu propia bicicleta y el sistema Retül registra tu movimiento real.</p>
      <h3>3. Ajustes con datos</h3>
      <p>Ajustamos sillín, manubrio y calas según la información del software y, si hace falta, te recomendamos cambios de componentes.</p>
      <h3>4. Medición final y reporte</h3>
      <p>Medimos tu bici con la herramienta Zin de Retül y te entregamos un reporte con tus medidas, para que siempre puedas volver a tu posición o replicarla en una bici nueva.</p>

      <h2>Bike fit gratis con tu bicicleta nueva</h2>
      <p>Si compras en Veloce una bicicleta de más de <b>$8.000.000</b>, el bike fit Retül va incluido sin costo. Puedes ver las bicicletas disponibles en la sección de <a href="/#productos/bicicletas">productos</a>.</p>"""
bf_faq = [
    ("¿Cuánto cuesta un bike fit Retül en Medellín?", "Escríbenos por WhatsApp y te damos el precio actualizado. Si compras en Veloce una bicicleta de más de $8.000.000, el bike fit Retül es gratis."),
    ("¿Necesito llevar mi bicicleta?", "Sí. El bike fit se hace sobre tu propia bicicleta, con tus zapatillas y tu ropa de montar, para que el ajuste sea real."),
    ("¿El bike fit sirve si no compito?", "Sí. Cualquier ciclista que monte seguido se beneficia: más comodidad y menos molestias, sin importar tu nivel."),
    ("¿Qué me entregan al final?", "Un reporte con todas tus medidas tomadas con la herramienta Zin de Retül, para que puedas volver a tu posición cuando lo necesites."),
    ("¿Conviene hacer el bike fit antes de comprar bici?", "Sí. Es la mejor forma de acertar con la talla y el modelo. Escríbenos y te asesoramos."),
]
bf_lat = f"""      <h3>Agenda tu bike fit</h3>
      <p>Sistema Retül con captura 3D.</p>
      <p><b style="color:var(--rojo)">Gratis con tu bici de más de $8.000.000.</b></p>
{DIR}
      <p><b>Tienda:</b> lunes a viernes 10:00 AM – 7:00 PM · sábados 11:00 AM – 5:00 PM.</p>"""

# ---------- TALLER ----------
t_cuerpo = """      <h2>Taller especializado en Medellín</h2>
      <p>En el taller de Veloce, en El Poblado, Medellín, atendemos bicicletas de <b>ruta, MTB y eléctricas</b> con mecánicos que conocen las bicis de alto nivel. Sabemos que tu bici es una inversión y la tratamos así: con las herramientas correctas y el cuidado que necesitan el carbono, los grupos electrónicos y las suspensiones.</p>

      <h2>Servicios del taller</h2>
      <ul>
        <li><b>Mantenimiento</b> general y preventivo para que tu bici ruede siempre como nueva.</li>
        <li><b>Alistada:</b> ajuste completo de cambios, frenos y componentes antes de una salida, una carrera o un viaje.</li>
        <li><b>Lavada</b> de tu bicicleta.</li>
        <li><b>Mantenimiento de suspensiones</b> para MTB.</li>
        <li><b>Sangrada de frenos de disco</b> hidráulicos para que frenen firme y parejo.</li>
        <li><b>Tubelizada de ruedas:</b> montaje de llantas sin neumático, con menos pinchazos y mejor agarre.</li>
        <li><b>Encerada de cadena:</b> menos fricción, una transmisión más limpia y más duración de la cadena.</li>
        <li><b>Grupos electrónicos:</b> instalación y actualización de Shimano Di2, SRAM AXS y Campagnolo.</li>
        <li><b>Armada de bicicletas:</b> armamos tu bici nueva o el proyecto que elijas, pieza por pieza.</li>
        <li><b>Instalación de potenciómetros</b> y configuración con tu ciclocomputador.</li>
        <li><b>Mantenimiento de simuladores</b> (rodillos inteligentes).</li>
      </ul>

      <h2>Ruta, MTB y bicicletas eléctricas</h2>
      <p>Trabajamos con bicicletas de ruta, de montaña y eléctricas. Cada tipo tiene sus necesidades: desde la sincronización de un grupo electrónico en una bici de ruta hasta el mantenimiento de suspensiones en una MTB.</p>

      <h2>¿Por qué traer tu bici a Veloce?</h2>
      <p>Somos ciclistas atendiendo ciclistas. Además del taller tenemos <a href="/bike-fit-retul-medellin">bike fit Retül</a>, así que si cambias un componente que afecta tu posición, como el sillín, el manubrio o las calas, podemos dejarte bien ajustado en el mismo lugar.</p>"""
t_faq = [
    ("¿Cómo agendo mi bici en el taller?", "Escríbenos por WhatsApp al +57 305 245 1204 y te damos la disponibilidad."),
    ("¿Trabajan con grupos electrónicos?", "Sí. Instalamos y actualizamos grupos Shimano Di2, SRAM AXS y Campagnolo."),
    ("¿Hacen sangrada de frenos de disco?", "Sí. Sangramos frenos de disco hidráulicos para que vuelvan a frenar firme y parejo."),
    ("¿Tubelizan ruedas?", "Sí. Tubelizamos tus ruedas para que ruedes con menos pinchazos y mejor agarre."),
    ("¿Arman bicicletas?", "Sí. Armamos tu bicicleta nueva o el proyecto que quieras, e instalamos potenciómetros."),
    ("¿Hacen mantenimiento a bicicletas eléctricas y MTB?", "Sí. Atendemos bicicletas de ruta, MTB y eléctricas, incluido el mantenimiento de suspensiones."),
    ("¿Qué es la encerada de cadena?", "Es reemplazar el lubricante tradicional por cera. La transmisión queda más limpia, con menos fricción, y la cadena dura más."),
    ("¿Hacen mantenimiento a simuladores?", "Sí. También hacemos mantenimiento a simuladores de entrenamiento."),
    ("¿Cada cuánto debo hacerle mantenimiento a mi bicicleta?", "Depende de cuánto montes y en qué condiciones. Si ruedas varias veces por semana, una revisión periódica evita desgastes y daños más caros. Escríbenos y te orientamos según tu caso."),
    ("¿Dónde queda el taller?", "En nuestra tienda: Calle 16A Sur #32B-38, Local 101, Mall Campestre Drive Inn, El Poblado, Medellín."),
]
t_lat = f"""      <h3>Agenda tu taller</h3>
      <p>Mecánicos especializados en bicicletas de alta gama.</p>
{DIR}
      <p><b>Horario:</b> lunes a viernes 10:00 AM – 7:00 PM · sábados 11:00 AM – 5:00 PM.</p>"""

# ---------- CENTRO DE ENTRENAMIENTO ----------
c_cuerpo = """      <h2>Clases de ciclismo indoor por potencia</h2>
      <p>En el centro de entrenamiento de Veloce, en El Poblado, Medellín, entrenas en simulador inteligente con clases guiadas de una hora, llueva o truene. Entrenamos por potencia, la forma más precisa de medir tu esfuerzo y ver tu progreso semana a semana.</p>

      <figure class="fig"><img src="/img/centro-clase.jpg" alt="Clase de ciclismo indoor por potencia en Veloce, Medellín" loading="lazy"><figcaption>Una clase en el centro de entrenamiento de Veloce.</figcaption></figure>

      <h2>Horario de clases</h2>
      <ul>
        <li><b>Lunes:</b> 6:00, 7:00 y 8:00 AM</li>
        <li><b>Martes a viernes:</b> 5:00, 6:00, 7:00 y 8:00 AM</li>
      </ul>
      <p>Cada clase dura una hora, así que entrenas temprano y llegas a tiempo a tus actividades.</p>

      <h2>¿Por qué entrenar por potencia?</h2>
      <p>La potencia, medida en vatios, no depende del viento, la pendiente ni el cansancio del día. Por eso es la forma más confiable de saber si estás mejorando y de entrenar en las zonas correctas para tu objetivo, ya sea una gran fondo, una carrera o simplemente rodar más fuerte con tus amigos.</p>

      <h2>Planes con seguimiento</h2>
      <p>Si quieres ir más allá de las clases, también ofrecemos planes de entrenamiento con seguimiento en <b>TrainingPeaks</b>, ajustados a tu tiempo disponible y tus metas.</p>"""
c_faq = [
    ("¿Necesito llevar mi bicicleta?", "Escríbenos por WhatsApp y te contamos qué necesitas para tu primera clase."),
    ("¿Las clases sirven para principiantes?", "Sí. Al entrenar por potencia cada persona trabaja según su propio nivel, así que puedes compartir la clase con ciclistas más avanzados."),
    ("¿Cómo reservo una clase?", "Escríbenos por WhatsApp al +57 305 245 1204 y te reservamos tu cupo."),
    ("¿Qué horarios tienen?", "Lunes a las 6:00, 7:00 y 8:00 AM, y de martes a viernes a las 5:00, 6:00, 7:00 y 8:00 AM. Cada clase dura una hora."),
]
c_lat = f"""      <h3>Reserva tu clase</h3>
      <p><b>Lunes:</b> 6, 7 y 8 AM<br><b>Martes a viernes:</b> 5, 6, 7 y 8 AM</p>
      <p>Clases de 1 hora en simulador inteligente.</p>
{DIR}"""

paginas = [
    ("bike-fit-retul-medellin",
     "Bike fit Retül en Medellín | Veloce, El Poblado",
     "Bike fit Retül con captura 3D en El Poblado, Medellín. Más comodidad, menos lesiones y más potencia. Gratis con tu bicicleta de más de $8.000.000.",
     "Bike fit Retül", "Bike fit Retül<br>en Medellín.",
     "Ajustamos tu bicicleta a tu cuerpo con captura de movimiento 3D. Más comodidad, menos lesiones y más potencia, con datos y no a ojo.",
     "Agendar bike fit", "Hola Veloce, quiero agendar un bike fit Retül",
     bf_cuerpo, bf_faq, bf_lat, "Bike fit Retül", "img/retul-fit.jpg", "Bike fit Retül con captura de movimiento 3D en Veloce, Medellín"),
    ("taller-de-bicicletas-medellin",
     "Taller de bicicletas en Medellín | Veloce, El Poblado",
     "Taller de bicicletas en El Poblado, Medellín: mantenimiento, alistada y lavada de ruta, MTB y eléctricas, suspensiones, sangrada de frenos, tubelizada, armada y Shimano Di2, SRAM AXS y Campagnolo.",
     "Taller de bicicletas", "Taller de bicicletas<br>en Medellín.",
     "Mantenimiento, alistada y lavada para bicicletas de ruta, MTB y eléctricas. Suspensiones, frenos de disco, tubeless, armado, potenciómetros y grupos electrónicos Di2, AXS y Campagnolo.",
     "Agendar taller", "Hola Veloce, quiero agendar mi bici en el taller",
     t_cuerpo, t_faq, t_lat, "Taller de bicicletas", "img/taller.jpg", "Mecánicos trabajando en el taller de bicicletas de Veloce en Medellín"),
    ("centro-de-entrenamiento-ciclismo-medellin",
     "Centro de entrenamiento de ciclismo en Medellín | Clases por potencia · Veloce",
     "Clases de ciclismo indoor por potencia en simulador inteligente, en El Poblado, Medellín. Lunes a viernes desde las 5:00 AM. Planes con seguimiento en TrainingPeaks.",
     "Centro de entrenamiento", "Centro de<br>entrenamiento.",
     "Clases de ciclismo indoor de una hora en simulador inteligente, entrenando por potencia. Lunes a viernes desde las 5:00 AM en El Poblado, Medellín.",
     "Reservar clase", "Hola Veloce, quiero reservar una clase en el centro de entrenamiento",
     c_cuerpo, c_faq, c_lat, "Clases de ciclismo indoor", "img/centro-entrenamiento.jpg", "Centro de entrenamiento de ciclismo indoor de Veloce en Medellín"),
]

if __name__ == "__main__":
  for p in paginas:
    open(f"{p[0]}.html", "w", encoding="utf-8").write(pagina(*p))
    print("ok", p[0])
