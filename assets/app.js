(function(){
  var BASE = document.body.getAttribute('data-base') || '';
  var INDEX = window.SEARCH_INDEX || [];

  // Menú móvil
  var burger = document.querySelector('.burger');
  var menu = document.querySelector('nav.menu');
  if (burger && menu) burger.addEventListener('click', function(){
    var open = menu.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
    burger.textContent = open ? '✕' : '☰';
  });

  // Menú desplegable
  document.querySelectorAll('.drop > button').forEach(function(b){
    b.addEventListener('click', function(){
      var d = b.parentElement, open = d.classList.toggle('open');
      b.setAttribute('aria-expanded', open);
    });
  });
  document.addEventListener('click', function(e){
    document.querySelectorAll('.drop.open').forEach(function(d){
      if (!d.contains(e.target)) { d.classList.remove('open'); d.querySelector('button').setAttribute('aria-expanded', false); }
    });
  });

  // Buscador
  function norm(s){ return (s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,''); }
  function buscar(q){
    var terms = norm(q).split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    return INDEX.map(function(it){
      var t = norm(it.t), all = t + ' ' + norm(it.k) + ' ' + norm(it.r), score = 0;
      for (var i=0;i<terms.length;i++){
        if (all.indexOf(terms[i]) === -1) return null;
        score += t.indexOf(terms[i]) !== -1 ? 3 : 1;
      }
      return {it:it, s:score};
    }).filter(Boolean).sort(function(a,b){return b.s-a.s;}).slice(0,7).map(function(x){return x.it;});
  }
  document.querySelectorAll('[data-search]').forEach(function(box){
    var input = box.querySelector('input'), out = box.querySelector('.results'), sel = -1;
    function render(){
      var q = input.value.trim(), res = buscar(q); sel = -1;
      if (!q) { out.classList.remove('show'); out.innerHTML=''; return; }
      out.innerHTML = res.length ? res.map(function(it){
        return '<a href="'+BASE+it.u+'"><b>'+it.i+' '+it.t+'</b><small>'+it.r+'</small></a>';
      }).join('') : '<div class="vacio">No encontramos fichas para “'+q.replace(/</g,'&lt;')+'”. Probá con otra palabra (por ejemplo: rótulo, PUPAA, carnet).</div>';
      out.classList.add('show');
    }
    input.addEventListener('input', render);
    input.addEventListener('focus', render);
    input.addEventListener('keydown', function(e){
      var links = out.querySelectorAll('a');
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp'){
        e.preventDefault(); if (!links.length) return;
        sel = (sel + (e.key==='ArrowDown'?1:-1) + links.length) % links.length;
        links.forEach(function(l,i){ l.classList.toggle('sel', i===sel); });
      } else if (e.key === 'Enter'){
        var go = links[sel>=0?sel:0]; if (go) { e.preventDefault(); location.href = go.href; }
      } else if (e.key === 'Escape'){ out.classList.remove('show'); input.blur(); }
    });
    document.addEventListener('click', function(e){ if (!box.contains(e.target)) out.classList.remove('show'); });
  });

  // Filtro en la página de guías
  var filtro = document.getElementById('filtro');
  if (filtro) filtro.addEventListener('input', function(){
    var q = norm(filtro.value);
    document.querySelectorAll('[data-ficha]').forEach(function(c){
      c.style.display = norm(c.getAttribute('data-ficha')).indexOf(q) !== -1 ? '' : 'none';
    });
    document.querySelectorAll('[data-bloque]').forEach(function(b){
      var vis = b.querySelectorAll('[data-ficha]:not([style*="none"])').length;
      b.style.display = vis ? '' : 'none';
    });
  });

  // Ruta guiada
  var quiz = document.getElementById('quiz');
  if (quiz) {
    var F = {}; INDEX.forEach(function(it){ F[it.s] = it; });
    function v(name){ var el = quiz.querySelector('input[name="'+name+'"]:checked'); return el ? el.value : null; }
    function paso(slug, nota){ var it = F[slug]; return '<li><a href="'+BASE+it.u+'">'+it.i+' '+it.t+'</a><small>'+(nota||it.r)+'</small></li>'; }
    quiz.addEventListener('change', function(){
      var escala=v('escala'), venta=v('venta'), local=v('local'), especial=v('especial');
      var out = document.getElementById('ruta');
      if (!escala || !venta || !local || !especial) return;
      var pasos = [];
      if (local === 'no') pasos.push(paso('habilitacion-municipal','Primero: el local. Consultá la zonificación antes de alquilar o invertir.'));
      pasos.push(paso('carnet-manipulador','Para vos y para todos los que manipulen alimentos.'));
      var artesanal = (escala === 'artesanal' && venta === 'local');
      if (artesanal) {
        pasos.push(paso('pupaa','Tu camino más probable: registro provincial gratuito.'));
      } else {
        if (escala === 'artesanal') pasos.push(paso('cual-me-corresponde','Querés vender más allá de tu zona: revisá si PUPAA te alcanza o necesitás RNE + RNPA.'));
        pasos.push(paso('rne','Registrá el establecimiento (o verificá el RNE de la planta que te elabora).'));
        pasos.push(paso('rnpa','Después, cada producto.'));
      }
      pasos.push(paso('rotulado','Diseñá la etiqueta antes de imprimir.'));
      pasos.push(paso('etiquetado-frontal','Verificá si tu producto lleva sellos.'));
      if (especial === 'si') pasos.push(paso('matricula-direccion-tecnica','Tu rubro puede exigir un director técnico.'));
      if (venta === 'exporta' ) pasos.push(paso('decreto-697-2026','La reforma de 2026 cambia la importación y la exportación. (Ficha de exportación: próximamente.)'));
      else pasos.push(paso('decreto-697-2026','Novedades que pueden afectar tus trámites.'));
      out.innerHTML = '<h3>Tu ruta sugerida</h3><ol>'+pasos.join('')+'</ol>'+
        '<p class="nota">Esta ruta es orientativa y no reemplaza la consulta con la autoridad sanitaria.</p>'+
        '<div class="guia-cta" style="margin-top:18px"><div><h3>¿Querés hacerlo acompañado?</h3><p>Un ingeniero en alimentos puede revisar tu caso y gestionar los trámites con vos.</p></div><a class="btn btn-verde" href="'+out.getAttribute('data-asesoria')+'" target="_blank" rel="noopener">Pedir asesoría →</a></div>';
      if (!out.classList.contains('show')) { out.classList.add('show'); out.scrollIntoView({behavior:'smooth', block:'start'}); }
    });
  }
})();
