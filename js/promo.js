/* Franja de Black Friday Veloce. Se muestra sola según la fecha (hora de Colombia).
   Expectativa: jue 26 nov 5:00 PM  ->  vie 27 nov 12:00 AM
   Campaña:     vie 27 nov 12:00 AM ->  lun 30 nov 11:59 PM
   Después del 30 no se muestra nada. */
(function () {
  var INICIO_EXPECTATIVA = new Date("2026-11-26T17:00:00-05:00").getTime();
  var INICIO_CAMPANA = new Date("2026-11-27T00:00:00-05:00").getTime();
  var FIN_CAMPANA = new Date("2026-12-01T00:00:00-05:00").getTime();
  var WA = "573052451204";
  var prueba = /[?&]bf=(\w+)/.exec(location.search);
  function ahora() {
    if (prueba && prueba[1] === "expectativa") return INICIO_EXPECTATIVA + 1000 + (Date.now() % 1000);
    if (prueba && prueba[1] === "campana") return INICIO_CAMPANA + 1000;
    return Date.now();
  }
  function enCampana() { var t = ahora(); return t >= INICIO_CAMPANA && t < FIN_CAMPANA; }
  if (enCampana()) document.documentElement.className += " bf-on";
  function precios() {
    var camp = enCampana();
    var post = prueba ? prueba[1] === "despues" : Date.now() >= FIN_CAMPANA;
    if (!camp && !post) return;
    var els = document.querySelectorAll(camp ? ".prod-price[data-bf]" : ".prod-price[data-bf-sigue]");
    for (var i = 0; i < els.length; i++) {
      var e = els[i];
      if (e.getAttribute("data-bf-ok")) continue;
      e.setAttribute("data-bf-ok", "1");
      e.innerHTML = "<s>" + e.getAttribute("data-normal") + "</s> " + e.getAttribute("data-bf");
      if (!camp) continue;
      var n = document.createElement("div");
      n.className = "bf-nota";
      n.textContent = "Precio Black Friday pagando en efectivo o transferencia";
      e.insertAdjacentElement("afterend", n);
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", precios); else precios();
  function dos(n) { return (n < 10 ? "0" : "") + n; }
  function montar() {
    var t = ahora();
    if (t < INICIO_EXPECTATIVA || t >= FIN_CAMPANA) return;
    var header = document.querySelector("header");
    if (!header || document.getElementById("bf-franja")) return;
    var f = document.createElement("div");
    f.id = "bf-franja";
    f.className = "bf-franja";
    header.insertAdjacentElement("afterend", f);
    var enHome = location.pathname === "/" || /index\.html$/.test(location.pathname);
    function pintar() {
      var n = ahora();
      if (n >= FIN_CAMPANA) { f.remove(); clearInterval(reloj); return; }
      if (n < INICIO_CAMPANA) {
        var s = Math.max(0, Math.floor((INICIO_CAMPANA - n) / 1000));
        var h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = s % 60;
        var msg = encodeURIComponent("Hola Veloce, quiero ser de los primeros en conocer los precios de Black Friday");
        f.innerHTML =
          '<div class="bf-in">' +
          '<div class="bf-txt"><strong>Black Friday Veloce</strong><span>Del viernes 27 al lunes 30 de noviembre · Precios especiales pagando en efectivo o transferencia</span></div>' +
          '<div class="bf-reloj" aria-label="Tiempo para que empiece"><small>Empieza en</small><b>' + dos(h) + "</b><i>h</i><b>" + dos(m) + "</b><i>min</i><b>" + dos(x) + "</b><i>s</i></div>" +
          '<a class="bf-btn" href="https://wa.me/' + WA + "?text=" + msg + '">Avísame primero</a>' +
          "</div>";
      } else {
        var msg2 = encodeURIComponent("Hola Veloce, quiero conocer los precios de Black Friday");
        f.innerHTML =
          '<div class="bf-in">' +
          '<div class="bf-txt"><strong>Black Friday Veloce</strong><span>Hasta el lunes 30 de noviembre · Precios especiales pagando en efectivo o transferencia · Hasta agotar existencias</span></div>' +
          '<a class="bf-btn" href="' + (enHome ? "#productos/ofertas" : "/#productos/ofertas") + '">Ver ofertas</a>' +
          '<a class="bf-btn bf-btn2" href="https://wa.me/' + WA + "?text=" + msg2 + '">Preguntar por WhatsApp</a>' +
          "</div>";
        clearInterval(reloj);
      }
    }
    var reloj = setInterval(pintar, 1000);
    pintar();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", montar);
  else montar();
  // Si la página queda abierta antes de las 5:00 PM, aparece sola al llegar la hora.
  var espera = INICIO_EXPECTATIVA - Date.now();
  if (espera > 0 && espera < 12 * 3600 * 1000) setTimeout(montar, espera + 500);
})();
