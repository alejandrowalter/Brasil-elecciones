**En vivo:** https://alejandrowalter.github.io/Brasil-elecciones/

# Brasil 2026 · 2ª vuelta — seguimiento en vivo

**Cómo abrirlo (Mac):** haz doble clic en `index.html` (se abre en Chrome o Safari). Se actualiza sola cada 60 s con los datos oficiales del TSE; no requiere instalar nada.
**Para probar hoy con datos reales** (1ª vuelta del 4 oct): agrega `?demo=1t` al final de la dirección en el navegador. Ej.: `.../index.html?demo=1t`.
**Si el domingo aparece "Error de conexión"**: abre Terminal en esta carpeta, ejecuta `python3 proxy.py` y entra a http://localhost:8787/?proxy=1

## Colores del mapa (3 bloques)
**Azul = derecha · Verde = centro · Rojo = izquierda · Tono pastel = aún sin definir.**
- Color fuerte = estado **definido**: gobernador ganado en 1ª vuelta, o 2ª vuelta / presidente con 100% apurado (o "Eleito" en gobernador).
- Pastel = aún sin definir: pastel del bloque que va adelante. Sin votos aún: pastel si los dos candidatos son del mismo bloque; **gris** si son de bloques distintos.
- Presidente: Lula (PT) = rojo, Flávio Bolsonaro (PL) = azul.
- **↻ / borde punteado** = cambio de **bloque** frente a 2022 (antes marcaba cualquier cambio de partido). El cambio de partido dentro del mismo bloque se indica en la tabla ("otro partido, mismo bloque").
- Bloques: **izquierda** PT, PSB, PDT, PSOL, PCdoB, PV, Rede (+ PCB, PCO, PSTU, UP). **Centro** MDB, PSD, PSDB, Podemos, Avante, Solidariedade, Cidadania, PRD, Agir, Mobiliza. **Derecha** PL, PP, Republicanos, União, Novo, DC, PRTB, Missão, Democrata.
- El detalle por partido sigue en las tablas, el resumen de gobernadores y los tooltips.

## Panel Polymarket (en vivo)
Debajo del mapa hay un panel con las probabilidades de **Polymarket** (mercado de apuestas, **no es un resultado oficial**):
- Mercado principal: [Brazil Presidential Election](https://polymarket.com/event/brazil-presidential-election): probabilidad de Flávio Bolsonaro (azul) y Lula (rojo) = punto medio del libro de órdenes (CLOB `/midpoint`; si no hay, último trade), cambio en la última hora y desde que abriste la página, gráfico de las últimas 24 h (botón Zoom / 0–100%) que se va extendiendo en vivo, volumen y liquidez.
- [Margen de victoria en 2ª vuelta](https://polymarket.com/event/brazil-presidential-election-second-round-margin-of-victory) y los mercados de **gobernador** de los 6 estados en 2ª vuelta (AC, AM, DF, ES, RN, TO), con el bloque de cada candidato.
- Se actualiza cada 30 s. Las APIs públicas de Polymarket (`gamma-api.polymarket.com`, `clob.polymarket.com`) responden con `Access-Control-Allow-Origin: *`, así que funciona abriendo el archivo directamente (doble clic), desde `proxy.py` o desde una página publicada; **no necesita proxy**.
- Si Polymarket no responde, el panel muestra "Polymarket no disponible" y el resto de la página (TSE) sigue funcionando.

## URL pública
_Pendiente de publicar_ (ver nota del asistente). La página debe servirse desde un origen https que permita conexiones a `resultados.tse.jus.br`.

## Opciones de URL
- `?demo=1t` — usa los resultados reales de la 1ª vuelta (elecciones TSE 6257 presidente / 6259 gobernador).
- `?view=gov` — abre directamente el mapa de gobernadores. `?uf=sp` — preselecciona un estado.
- `?proxy=1` — lee el TSE a través de `proxy.py` (solo si el TSE bloqueara CORS). `?refresh=30` — cambia el intervalo (s).

## Fuentes (oficiales)
- Resultados en vivo: TSE Divulgação de Resultados — `https://resultados.tse.jus.br/oficial/ele2026/<eleição>/dados/<uf>/<uf>-c<cargo>-e<eleição>-u.json`
  (2ª vuelta: 6258 presidente `c0001`, 6260 gobernador `c0003`; 1ª vuelta: 6257 / 6259). Índice: `/oficial/comum/config/ele-c.json`.
- Comparación 2022: TSE Dados Abertos (`consulta_cand_2022`, `votacao_candidato_munzona_2022`). ⚠ RR 2022: % no confiable en datos abiertos ("anulado sub judice"); ganador y partido sí.
- Mapa: `click_that_hood/brazil-states.geojson` (derivado de IBGE), simplificado y embebido en el HTML.

`src/` contiene los datos y `build.py` para regenerar `index.html` (no hace falta para usarlo).
