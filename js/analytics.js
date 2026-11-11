/* Google Analytics 4 + Google Ads · Veloce */
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-BCTKZM82SJ');
gtag('config', 'AW-11029871865'); /* Google Ads */

/* Mide cada clic a WhatsApp con el producto o la sección de donde viene */
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('a[href*="wa.me"]');
  if (a) {
    var card = a.closest('.prod'), modal = a.closest('.m-box'), slide = a.closest('.slide'), feature = a.closest('.feature');
    var producto = '', marca = '', origen = '';
    if (card) {
      marca = (card.querySelector('.prod-brand') || {}).textContent || '';
      producto = (card.querySelector('.prod-name') || {}).textContent || '';
      origen = 'tarjeta_producto';
    } else if (modal) {
      marca = (modal.querySelector('.prod-brand') || {}).textContent || '';
      producto = (modal.querySelector('h3') || {}).textContent || '';
      origen = 'detalle_producto';
    } else if (slide) {
      origen = 'banner_' + (((slide.querySelector('.slide-tag') || {}).textContent || 'principal').split('·')[0].trim().toLowerCase());
    } else if (feature) {
      origen = 'servicio_' + (((feature.querySelector('h3') || {}).textContent || '').replace(/\s+/g, ' ').trim().toLowerCase());
    } else if (a.classList.contains('wa')) {
      origen = 'boton_flotante';
    } else {
      origen = 'otro';
    }
    gtag('event', 'generate_lead', {
      metodo: 'whatsapp',
      producto: (marca + ' ' + producto).trim() || '(sin producto)',
      marca: marca.trim() || '(sin marca)',
      origen: origen,
      pagina: location.pathname
    });
    return;
  }
  var det = e.target.closest && e.target.closest('.prod-more');
  if (det) {
    var c = det.closest('.prod');
    if (c) gtag('event', 'select_item', {
      item_name: (((c.querySelector('.prod-brand') || {}).textContent || '') + ' ' + ((c.querySelector('.prod-name') || {}).textContent || '')).trim()
    });
  }
});
